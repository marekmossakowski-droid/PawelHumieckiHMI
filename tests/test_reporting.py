import unittest
from datetime import datetime, timezone

from hoofcare.reporting.report import ReportAudience, ReportInput, build_report_document


class ReportingTests(unittest.TestCase):
    def make_input(self):
        return ReportInput(
            report_id="RPT-001",
            generated_at=datetime(2026, 8, 21, 18, 20, tzinfo=timezone.utc),
            session_id="session-123",
            animal_id="TEST-COW-001",
            lesion_summary="Digital dermatitis, synthetic test record",
            treatment_summary="Cleaning and protective dressing, synthetic test record",
            material_summary="Dressing x1",
            media_refs=("TEST-BEFORE-001", "TEST-AFTER-001"),
        )

    def test_report_contains_provenance(self):
        doc = build_report_document(self.make_input())
        self.assertEqual(doc.report_id, "RPT-001")
        self.assertEqual(doc.source_session_id, "session-123")
        self.assertIn("2026-08-21", doc.generated_at_iso)

    def test_report_has_required_audience_sections(self):
        doc = build_report_document(self.make_input())
        self.assertEqual(
            set(doc.sections),
            {
                ReportAudience.FARMER,
                ReportAudience.VETERINARIAN,
                ReportAudience.ZOOTECHNICIAN,
                ReportAudience.NUTRITIONIST,
                ReportAudience.TECHNICAL_SERVICE,
            },
        )

    def test_report_is_explicitly_synthetic_and_non_diagnostic(self):
        doc = build_report_document(self.make_input())
        self.assertTrue(doc.synthetic_test_only)
        self.assertIn("does not replace veterinary examination", doc.clinical_disclaimer.lower())

    def test_report_requires_committed_canonical_record(self):
        with self.assertRaises(ValueError):
            build_report_document(self.make_input(), committed=False)

    def test_pdf_bytes_are_local_and_valid_pdf_signature(self):
        doc = build_report_document(self.make_input())
        pdf = doc.to_pdf_bytes()
        self.assertTrue(pdf.startswith(b"%PDF-"))
        self.assertIn(b"RPT-001", pdf)
        self.assertIn(b"session-123", pdf)


if __name__ == "__main__":
    unittest.main()
