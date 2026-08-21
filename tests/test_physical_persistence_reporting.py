import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from hoofcare.domain.session import (
    AnimalIdentityResolution,
    Session,
    SessionEvent,
    SessionEventType,
)
from hoofcare.physical.persistence_reporting import PhysicalPersistenceReportingValidator


class PhysicalPersistenceReportingValidatorTests(unittest.TestCase):
    def _completed_session(self) -> Session:
        session = Session.new()
        session = session.apply(
            SessionEvent(
                event_id="identity-1",
                event_type=SessionEventType.IDENTITY_RESOLVED,
                payload=AnimalIdentityResolution.confirmed("TEST-COW-001"),
            )
        )
        return session.apply(SessionEvent(event_id="complete-1", event_type=SessionEventType.COMPLETE))

    def test_committed_session_round_trips_and_recovers_after_restart(self):
        with tempfile.TemporaryDirectory() as root:
            validator = PhysicalPersistenceReportingValidator(Path(root))
            session = self._completed_session()
            validator.commit_session(session)

            restarted = PhysicalPersistenceReportingValidator(Path(root))
            recovered = restarted.recover_session(session.session_id)

            self.assertEqual(recovered, session)
            self.assertTrue(restarted.synthetic_test_only)
            self.assertFalse(restarted.kvk_connection_allowed)
            self.assertFalse(restarted.real_farm_data_allowed)

    def test_report_is_generated_only_from_committed_session_and_preserves_provenance(self):
        with tempfile.TemporaryDirectory() as root:
            validator = PhysicalPersistenceReportingValidator(Path(root))
            session = self._completed_session()
            validator.commit_session(session)

            document = validator.build_local_report(
                session.session_id,
                report_id="REPORT-001",
                generated_at=datetime(2026, 8, 22, tzinfo=timezone.utc),
                lesion_summary="synthetic lesion",
                treatment_summary="synthetic treatment",
                material_summary="1 synthetic dressing",
            )

            self.assertEqual(document.source_session_id, session.session_id)
            self.assertEqual(document.animal_id, "TEST-COW-001")
            self.assertTrue(document.synthetic_test_only)
            self.assertIn(b"Source-Session-ID", document.to_pdf_bytes())

    def test_missing_session_fails_closed(self):
        with tempfile.TemporaryDirectory() as root:
            validator = PhysicalPersistenceReportingValidator(Path(root))
            with self.assertRaises(KeyError):
                validator.build_local_report(
                    "missing",
                    report_id="REPORT-404",
                    generated_at=datetime(2026, 8, 22, tzinfo=timezone.utc),
                    lesion_summary="synthetic lesion",
                    treatment_summary="synthetic treatment",
                    material_summary="synthetic material",
                )


if __name__ == "__main__":
    unittest.main()
