import unittest
from datetime import datetime, timezone

from hoofcare.domain.clinical import (
    CanonicalClinicalRecord,
    LesionRecord,
    MaterialRecord,
    MediaRecord,
    TreatmentRecord,
)
from hoofcare.reporting.report import build_report_from_canonical_record


class CanonicalClinicalRecordTests(unittest.TestCase):
    def make_record(self):
        return CanonicalClinicalRecord(
            record_id="REC-001",
            session_id="session-123",
            animal_id="TEST-COW-001",
            committed_at=datetime(2026, 8, 22, 18, 0, tzinfo=timezone.utc),
            lesion=LesionRecord(code="DD", label="Digital dermatitis", anatomical_zone="heel-soft-tissue"),
            treatments=(TreatmentRecord(code="CLEAN", label="Cleaning"),),
            materials=(MaterialRecord(code="DRESSING", label="Protective dressing", quantity=1.0, unit="piece"),),
            media=(MediaRecord(ref="TEST-AFTER-001", kind="AFTER", captured_at=datetime(2026, 8, 22, 18, 1, tzinfo=timezone.utc), source="synthetic-test"),),
            committed=True,
            synthetic_test_only=True,
        )

    def test_canonical_record_requires_committed_identity_and_clinical_content(self):
        record = self.make_record()
        self.assertTrue(record.committed)
        self.assertEqual(record.lesion.code, "DD")
        self.assertEqual(record.treatments[0].code, "CLEAN")
        self.assertEqual(record.materials[0].quantity, 1.0)

    def test_media_has_explicit_capture_provenance(self):
        media = self.make_record().media[0]
        self.assertEqual(media.kind, "AFTER")
        self.assertEqual(media.source, "synthetic-test")
        self.assertIsNotNone(media.captured_at.tzinfo)

    def test_report_is_derived_only_from_committed_canonical_record(self):
        record = self.make_record()
        doc = build_report_from_canonical_record(
            record,
            report_id="RPT-CAN-001",
            generated_at=datetime(2026, 8, 22, 18, 2, tzinfo=timezone.utc),
        )
        pdf = doc.to_pdf_bytes()
        self.assertIn(b"Digital dermatitis", pdf)
        self.assertIn(b"Cleaning", pdf)
        self.assertIn(b"Protective dressing", pdf)
        self.assertIn(b"TEST-AFTER-001", pdf)

    def test_uncommitted_record_cannot_generate_report(self):
        record = self.make_record()
        uncommitted = CanonicalClinicalRecord(
            record_id=record.record_id,
            session_id=record.session_id,
            animal_id=record.animal_id,
            committed_at=record.committed_at,
            lesion=record.lesion,
            treatments=record.treatments,
            materials=record.materials,
            media=record.media,
            committed=False,
            synthetic_test_only=True,
        )
        with self.assertRaises(ValueError):
            build_report_from_canonical_record(
                uncommitted,
                report_id="RPT-CAN-002",
                generated_at=datetime(2026, 8, 22, 18, 3, tzinfo=timezone.utc),
            )


if __name__ == "__main__":
    unittest.main()
