import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from hoofcare.domain.session import AnimalIdentityResolution, IdentityStatus, Session, SessionState
from hoofcare.physical.prototype_validation import PhysicalPrototypeValidator


class PhysicalPrototypePersistenceReportingTests(unittest.TestCase):
    def test_round_trip_restart_recovery_and_report_from_committed_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            validator = PhysicalPrototypeValidator(Path(tmp))
            session = Session(session_id="P6-SYN-001", state=SessionState.IN_PROGRESS, identity=AnimalIdentityResolution(status=IdentityStatus.CONFIRMED, animal_id="SYN-COW-001"), animal_id="SYN-COW-001", treatment_refs=("hoof-trim",), material_refs=("dressing-1",), media_refs=("REF:synthetic-before.jpg",))
            validator.commit_session(session)
            recovered = validator.recover_session("P6-SYN-001")
            self.assertEqual(recovered, session)
            pdf = validator.generate_report("P6-SYN-001", report_id="P6-REPORT-001", generated_at=datetime(2026, 8, 21, 19, 40, 0), lesion_summary="synthetic lesion", treatment_summary="synthetic hoof trim", material_summary="1 synthetic dressing")
            self.assertTrue(pdf.startswith(b"%PDF-1.4"))
            self.assertIn(b"Source-Session-ID: P6-SYN-001", pdf)
            self.assertIn(b"Synthetic-Test-Only: true", pdf)

    def test_report_requires_committed_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            validator = PhysicalPrototypeValidator(Path(tmp))
            with self.assertRaises(KeyError):
                validator.generate_report("missing", report_id="R", generated_at=datetime(2026, 8, 21, 19, 40, 0), lesion_summary="x", treatment_summary="y", material_summary="z")

    def test_real_farm_and_kvk_paths_remain_forbidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            validator = PhysicalPrototypeValidator(Path(tmp))
            self.assertFalse(validator.kvk_connection_allowed)
            self.assertFalse(validator.real_farm_data_allowed)
            for name in ("connect_kvk", "write_kvk", "configure_kvk", "actuate", "upload_cloud"):
                self.assertFalse(hasattr(validator, name), name)


if __name__ == "__main__":
    unittest.main()
