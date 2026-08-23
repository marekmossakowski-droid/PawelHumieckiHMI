import importlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from hoofcare.persistence.local_store import LocalSessionStore
from tests.job_fixtures import closed_job_fixture, completed_session, open_job_fixture


def require_symbol(case: unittest.TestCase, module_name: str, symbol: str):
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        case.fail(f"{module_name} must exist")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


class JobPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.LocalJobStore = require_symbol(
            self, "hoofcare.persistence.job_store", "LocalJobStore"
        )
        self.JobService = require_symbol(
            self, "hoofcare.application.job_service", "JobService"
        )

    def test_job_round_trip_preserves_pricing_and_settlement(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.LocalJobStore(Path(tmp))
            store.save(closed_job_fixture())
            loaded = store.load("TEST-JOB-1")
            self.assertEqual(loaded, closed_job_fixture())

    def test_corrupt_job_snapshot_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = self.LocalJobStore(root)
            store.save(open_job_fixture())
            path = root / "TEST-JOB-1.job.json"
            path.write_text(
                path.read_text().replace("3500", "9999"), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "invalid persisted job"):
                store.load("TEST-JOB-1")

    def test_list_jobs_is_stable_and_uses_verified_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.LocalJobStore(Path(tmp))
            store.save(open_job_fixture())
            self.assertEqual(store.list_jobs(), (open_job_fixture(),))

    def test_failed_replace_preserves_previous_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.LocalJobStore(Path(tmp))
            store.save(open_job_fixture())
            with mock.patch(
                "hoofcare.persistence.job_store.os.replace",
                side_effect=OSError("synthetic replace failure"),
            ):
                with self.assertRaises(OSError):
                    store.save(closed_job_fixture())
            self.assertEqual(store.load("TEST-JOB-1"), open_job_fixture())

    def test_session_is_durable_before_cow_count_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            jobs = self.LocalJobStore(root / "jobs")
            sessions = LocalSessionStore(root / "sessions")
            jobs.save(open_job_fixture())
            service = self.JobService(jobs, sessions)
            updated = service.commit_completed_session(
                "TEST-JOB-1",
                completed_session("TEST-COW-1", "TEST-SESSION-1"),
                "event-1",
            )
            self.assertEqual(
                sessions.load(updated.completed_session_ids[0]).state.value,
                "COMPLETED",
            )
            self.assertEqual(jobs.load("TEST-JOB-1").completed_cows, 1)

    def test_recovery_reports_but_does_not_bill_unlinked_durable_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            jobs = self.LocalJobStore(Path(tmp) / "jobs")
            jobs.save(open_job_fixture())
            service = self.JobService(
                jobs, LocalSessionStore(Path(tmp) / "sessions")
            )
            missing = service.reconciliation_required(
                "TEST-JOB-1", ("TEST-SESSION-9",)
            )
            self.assertEqual(missing, ("TEST-SESSION-9",))
            self.assertEqual(jobs.load("TEST-JOB-1").completed_cows, 0)


if __name__ == "__main__":
    unittest.main()
