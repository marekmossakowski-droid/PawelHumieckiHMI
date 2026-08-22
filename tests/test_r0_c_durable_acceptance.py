from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from hoofcare.domain.session import AnimalIdentityResolution, Session, SessionEvent, SessionEventType, SessionState
from hoofcare.physical.durable_acceptance import DurablePhysicalPrototypeAcceptance
from hoofcare.physical.persistence_reporting import PhysicalPersistenceReportingValidator


class FailingStore:
    def save(self, session):
        raise OSError("synthetic persistence failure")


class DurableCompletionTests(unittest.TestCase):
    def _identified_session(self):
        return Session.new().apply(
            SessionEvent(
                event_id="identity",
                event_type=SessionEventType.IDENTITY_RESOLVED,
                payload=AnimalIdentityResolution.confirmed("TEST-COW-R0C"),
            )
        )

    def test_completion_is_acknowledged_only_after_durable_commit(self):
        with TemporaryDirectory() as tmp:
            validator = PhysicalPersistenceReportingValidator(Path(tmp))
            completed = validator.complete_and_commit(self._identified_session(), event_id="complete")
            recovered = validator.recover_session(completed.session_id)

        self.assertEqual(completed.state, SessionState.COMPLETED)
        self.assertEqual(recovered, completed)

    def test_persistence_failure_does_not_return_completed_session(self):
        with TemporaryDirectory() as tmp:
            validator = PhysicalPersistenceReportingValidator(Path(tmp))
            validator.store = FailingStore()
            original = self._identified_session()
            with self.assertRaises(OSError):
                validator.complete_and_commit(original, event_id="complete")
            self.assertEqual(original.state, SessionState.IN_PROGRESS)

    def test_acceptance_checks_are_evidence_derived(self):
        with TemporaryDirectory() as tmp:
            result = DurablePhysicalPrototypeAcceptance.synthetic(Path(tmp)).run()

        self.assertEqual(result.checks["durable_completion"], "PASS")
        self.assertEqual(result.checks["persistence_restart"], "PASS")
        self.assertEqual(result.checks["local_report"], "PASS")
        self.assertNotIn("end_to_end", result.checks)
        self.assertTrue(all(value in {"PASS", "FAIL"} for value in result.checks.values()))


if __name__ == "__main__":
    unittest.main()
