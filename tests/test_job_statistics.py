from datetime import date, datetime, timezone
from decimal import Decimal
import importlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from hoofcare.domain.jobs import Job, JobPricingSnapshot, JobState, MaterialRate
from hoofcare.persistence.job_store import LocalJobStore
from tests.job_fixtures import completed_session


def require_symbol(case: unittest.TestCase, symbol: str):
    try:
        module = importlib.import_module("hoofcare.application.job_statistics")
    except ModuleNotFoundError:
        case.fail("hoofcare.application.job_statistics must exist")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


def make_job(job_id: str, farm_id: str, operator_id: str, opened: datetime, cows: int, close: bool) -> Job:
    job = Job.open(
        job_id,
        farm_id,
        operator_id,
        opened,
        JobPricingSnapshot(3500, (MaterialRate("BLOCK", "Klocek", "szt.", 2600, 0),)),
        cows,
    )
    for index in range(cows):
        session = completed_session(f"{job_id}-COW-{index}", f"{job_id}-SESSION-{index}")
        job = job.record_completed_session(session, f"{job_id}-COMPLETE-{index}")
    if cows:
        job = job.record_material("MAT-" + job_id, job.completed_session_ids[0], "BLOCK", Decimal("1"))
    return job.close(opened.replace(hour=18), ()) if close else job


class JobStatisticsTests(unittest.TestCase):
    def setUp(self):
        self.StatisticsFilter = require_symbol(self, "StatisticsFilter")
        self.derive = require_symbol(self, "derive_job_statistics")

    def test_statistics_derive_from_jobs_reloaded_after_restart(self):
        with TemporaryDirectory() as directory:
            store = LocalJobStore(Path(directory))
            store.save(make_job("J1", "F1", "pawel", datetime(2026, 8, 22, 8, tzinfo=timezone.utc), 2, True))
            store.save(make_job("J2", "F2", "pawel", datetime(2026, 8, 23, 8, tzinfo=timezone.utc), 1, False))
            reloaded = LocalJobStore(Path(directory)).list_jobs()

        stats = self.derive(reloaded, self.StatisticsFilter(date(2026, 8, 22), date(2026, 8, 23)))
        self.assertEqual((stats.completed_cows, stats.open_jobs, stats.closed_jobs), (3, 1, 1))
        self.assertEqual(stats.total_net_grosz, 9600)
        self.assertEqual(stats.additional_material_quantities[0].code, "BLOCK")
        self.assertEqual(stats.additional_material_quantities[0].quantity, Decimal("2"))

    def test_filters_are_inclusive_and_composable(self):
        jobs = (
            make_job("J1", "F1", "pawel", datetime(2026, 8, 22, 8, tzinfo=timezone.utc), 2, True),
            make_job("J2", "F1", "other", datetime(2026, 8, 23, 8, tzinfo=timezone.utc), 3, True),
            make_job("J3", "F2", "pawel", datetime(2026, 8, 24, 8, tzinfo=timezone.utc), 4, True),
        )
        query = self.StatisticsFilter(date(2026, 8, 22), date(2026, 8, 23), operator_id="pawel", farm_id="F1", state=JobState.CLOSED)
        stats = self.derive(jobs, query)
        self.assertEqual((stats.completed_cows, stats.closed_jobs, stats.total_net_grosz), (2, 1, 9600))

    def test_open_job_never_invents_a_net_total(self):
        job = make_job("J1", "F1", "pawel", datetime(2026, 8, 23, 8, tzinfo=timezone.utc), 2, False)
        stats = self.derive((job,), self.StatisticsFilter(date(2026, 8, 23), date(2026, 8, 23)))
        self.assertEqual(stats.total_net_grosz, 0)

    def test_invalid_date_range_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "date range"):
            self.StatisticsFilter(date(2026, 8, 24), date(2026, 8, 23))


if __name__ == "__main__":
    unittest.main()
