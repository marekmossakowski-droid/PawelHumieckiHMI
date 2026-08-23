from datetime import datetime, timezone
import tempfile
import unittest
from pathlib import Path

from hoofcare.application.job_service import JobService
from hoofcare.domain.jobs import PriceField
from hoofcare.persistence.job_store import LocalJobStore
from hoofcare.persistence.local_store import LocalSessionStore

try:
    from tests.job_fixtures import CLOSED, completed_session, open_job_fixture
except ModuleNotFoundError:
    from job_fixtures import CLOSED, completed_session, open_job_fixture


CORRECTED_AT = datetime(2026, 8, 23, 8, 30, tzinfo=timezone.utc)
LATER = datetime(2026, 8, 23, 9, 30, tzinfo=timezone.utc)


def durable_fixture(root: Path):
    jobs = LocalJobStore(root / "jobs")
    sessions = LocalSessionStore(root / "sessions")
    return jobs, sessions, JobService(jobs, sessions)


class JobPriceCorrectionIntegrationTests(unittest.TestCase):
    def test_open_correct_restart_complete_freeze_and_close(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            jobs, sessions, service = durable_fixture(root)
            jobs.save(open_job_fixture())
            corrected = service.correct_price(
                "TEST-JOB-1",
                "TEST-CORRECTION-1",
                "TEST-PAWEL",
                CORRECTED_AT,
                "Błąd stawki",
                PriceField.COW_UNIT_PRICE,
                3600,
            )
            self.assertEqual(corrected.pricing_version, 2)

            restarted = JobService(
                LocalJobStore(jobs.root),
                LocalSessionStore(sessions.root),
            )
            completed = restarted.commit_completed_session(
                "TEST-JOB-1",
                completed_session("TEST-COW-1", "TEST-SESSION-1"),
                "TEST-COMPLETE-1",
            )

            self.assertTrue(completed.pricing_frozen)
            self.assertEqual(completed.price_corrections, corrected.price_corrections)
            with self.assertRaisesRegex(ValueError, "pricing is frozen"):
                restarted.correct_price(
                    "TEST-JOB-1",
                    "TEST-CORRECTION-2",
                    "TEST-PAWEL",
                    LATER,
                    "Po rozpoczęciu",
                    PriceField.COW_UNIT_PRICE,
                    3700,
                )

            durable = jobs.load("TEST-JOB-1")
            closed = durable.close(CLOSED, ())
            self.assertEqual(closed.settlement().total_net_grosz, 3600)
            self.assertEqual(durable.pricing.cow_unit_price_grosz, 3600)

    def test_req_hc_002_a1_is_mapped_to_restart_evidence(self):
        matrix = Path(
            "docs/traceability/HC-REQ-TRACE-001_Requirement_Level_Matrix_v0.1.md"
        ).read_text(encoding="utf-8")

        for requirement in (
            "REQ-HC-JOB-ROLE-A1-001",
            "REQ-HC-JOB-ROLE-A1-002",
            "REQ-HC-JOB-ROLE-A1-003",
            "REQ-HC-JOB-PRICE-A1-001",
            "REQ-HC-JOB-PRICE-A1-002",
            "REQ-HC-JOB-PRICE-A1-003",
            "REQ-HC-JOB-PRICE-A1-004",
        ):
            self.assertIn(requirement, matrix)
        self.assertIn("test_open_correct_restart_complete_freeze_and_close", matrix)


if __name__ == "__main__":
    unittest.main()
