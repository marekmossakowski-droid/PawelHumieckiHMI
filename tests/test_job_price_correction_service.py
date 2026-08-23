from datetime import datetime, timezone
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from hoofcare.application.job_service import JobService
from hoofcare.domain.jobs import PriceField
from hoofcare.persistence.job_store import LocalJobStore
from hoofcare.persistence.local_store import LocalSessionStore

try:
    from tests.job_fixtures import open_job_fixture
except ModuleNotFoundError:
    from job_fixtures import open_job_fixture


CORRECTED_AT = datetime(2026, 8, 23, 8, 30, tzinfo=timezone.utc)


def service_fixture(root: Path):
    jobs = LocalJobStore(root / "jobs")
    sessions = LocalSessionStore(root / "sessions")
    jobs.save(open_job_fixture())
    return JobService(jobs, sessions), jobs


class JobPriceCorrectionServiceTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            hasattr(JobService, "correct_price"),
            "JobService.correct_price must exist",
        )

    def test_service_persists_correction_before_returning_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            service, jobs = service_fixture(Path(tmp))

            changed = service.correct_price(
                "TEST-JOB-1",
                "TEST-CORRECTION-1",
                "TEST-PAWEL",
                CORRECTED_AT,
                "Błąd stawki",
                PriceField.COW_UNIT_PRICE,
                3600,
            )

            self.assertEqual(jobs.load("TEST-JOB-1"), changed)
            self.assertEqual(changed.pricing_version, 2)

    def test_storage_failure_does_not_change_durable_job(self):
        with tempfile.TemporaryDirectory() as tmp:
            service, jobs = service_fixture(Path(tmp))
            with mock.patch.object(
                jobs,
                "save",
                side_effect=OSError("TEST-FAIL"),
            ):
                with self.assertRaises(OSError):
                    service.correct_price(
                        "TEST-JOB-1",
                        "TEST-CORRECTION-1",
                        "TEST-PAWEL",
                        CORRECTED_AT,
                        "Błąd stawki",
                        PriceField.COW_UNIT_PRICE,
                        3600,
                    )

            self.assertEqual(jobs.load("TEST-JOB-1").pricing_version, 1)
            self.assertEqual(jobs.load("TEST-JOB-1").price_corrections, ())


if __name__ == "__main__":
    unittest.main()
