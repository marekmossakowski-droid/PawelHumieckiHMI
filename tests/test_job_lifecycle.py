from datetime import datetime, timezone
from decimal import Decimal
import importlib
import unittest

from hoofcare.domain.session import (
    AnimalIdentityResolution,
    Session,
    SessionEvent,
    SessionEventType,
)


def require_symbol(case: unittest.TestCase, symbol: str):
    module = importlib.import_module("hoofcare.domain.jobs")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


def completed_session(animal_id: str) -> Session:
    session = Session.new().apply(
        SessionEvent(
            "identity",
            SessionEventType.IDENTITY_RESOLVED,
            AnimalIdentityResolution.confirmed(animal_id),
        )
    )
    return session.apply(SessionEvent("complete", SessionEventType.COMPLETE))


class JobLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.Job = require_symbol(self, "Job")
        self.JobState = require_symbol(self, "JobState")
        self.MaterialRate = require_symbol(self, "MaterialRate")
        self.JobPricingSnapshot = require_symbol(self, "JobPricingSnapshot")
        rates = (self.MaterialRate("BLOCK", "Klocek", "szt.", 1800, 0),)
        self.job = self.Job.open(
            "TEST-JOB-1",
            "TEST-FARM-1",
            "operator-pawel",
            datetime(2026, 8, 23, tzinfo=timezone.utc),
            self.JobPricingSnapshot(3500, rates),
            40,
        )

    def test_completed_session_counts_once_under_retry(self):
        session = completed_session("TEST-COW-1")
        once = self.job.record_completed_session(session, "event-1")
        twice = once.record_completed_session(session, "event-1")
        self.assertEqual(twice.completed_cows, 1)

    def test_reused_completion_event_with_different_session_fails_closed(self):
        once = self.job.record_completed_session(
            completed_session("TEST-COW-1"), "event-1"
        )
        with self.assertRaises(ValueError):
            once.record_completed_session(completed_session("TEST-COW-2"), "event-1")

    def test_draft_or_cancelled_session_does_not_count(self):
        with self.assertRaises(ValueError):
            self.job.record_completed_session(Session.new(), "event-2")

    def test_extra_material_is_billed_once_under_retry(self):
        counted = self.job.record_completed_session(
            completed_session("TEST-COW-1"), "event-1"
        )
        used = counted.record_material(
            "material-1", counted.completed_session_ids[0], "BLOCK", Decimal("2")
        )
        retried = used.record_material(
            "material-1", counted.completed_session_ids[0], "BLOCK", Decimal("2")
        )
        self.assertEqual(retried.material_total_grosz, 3600)

    def test_reused_material_event_with_different_quantity_fails_closed(self):
        counted = self.job.record_completed_session(
            completed_session("TEST-COW-1"), "event-1"
        )
        used = counted.record_material(
            "material-1", counted.completed_session_ids[0], "BLOCK", Decimal("1")
        )
        with self.assertRaises(ValueError):
            used.record_material(
                "material-1", counted.completed_session_ids[0], "BLOCK", Decimal("2")
            )

    def test_material_cannot_reference_a_session_outside_the_job(self):
        with self.assertRaises(ValueError):
            self.job.record_material(
                "material-1", "UNKNOWN-SESSION", "BLOCK", Decimal("1")
            )

    def test_local_material_can_be_added_only_while_job_is_open(self):
        local = self.MaterialRate("LOCAL-1", "Żel", "ml", 25, 1, True)
        extended = self.job.add_local_material(local)
        self.assertEqual(extended.pricing.rate("LOCAL-1"), local)
        closed = extended.close(datetime(2026, 8, 23, 18, tzinfo=timezone.utc), ())
        with self.assertRaises(ValueError):
            closed.add_local_material(
                self.MaterialRate("LOCAL-2", "Pianka", "ml", 30, 1, True)
            )

    def test_close_requires_no_unresolved_session_and_freezes_total(self):
        complete = self.job.record_completed_session(
            completed_session("TEST-COW-1"), "event-1"
        )
        closed = complete.close(
            datetime(2026, 8, 23, 18, tzinfo=timezone.utc),
            unresolved_session_ids=(),
        )
        self.assertEqual(closed.state, self.JobState.CLOSED)
        self.assertEqual(closed.settlement().total_net_grosz, 3500)
        with self.assertRaises(ValueError):
            complete.close(
                datetime.now(timezone.utc), unresolved_session_ids=("S-OPEN",)
            )


if __name__ == "__main__":
    unittest.main()
