import unittest
from uuid import UUID

from hoofcare.domain.session import (
    AnimalIdentityResolution,
    IdentityStatus,
    Session,
    SessionEvent,
    SessionEventType,
    SessionState,
)


class SessionCoreTests(unittest.TestCase):
    def test_new_session_has_immutable_id_and_identity_pending_state(self):
        session = Session.new()
        UUID(session.session_id)
        self.assertEqual(SessionState.IDENTITY_PENDING, session.state)

    def test_ambiguous_identity_fails_closed(self):
        session = Session.new()
        result = AnimalIdentityResolution.ambiguous(["cow-001", "cow-002"])
        session = session.apply(
            SessionEvent("evt-1", SessionEventType.IDENTITY_RESOLVED, result)
        )
        self.assertEqual(IdentityStatus.AMBIGUOUS, session.identity.status)
        self.assertEqual(SessionState.IDENTITY_PENDING, session.state)
        self.assertIsNone(session.animal_id)

    def test_confirmed_identity_allows_session_to_enter_in_progress(self):
        session = Session.new().apply(
            SessionEvent(
                "evt-1",
                SessionEventType.IDENTITY_RESOLVED,
                AnimalIdentityResolution.confirmed("cow-001"),
            )
        )
        self.assertEqual("cow-001", session.animal_id)
        self.assertEqual(SessionState.IN_PROGRESS, session.state)

    def test_duplicate_event_is_idempotent(self):
        session = Session.new()
        event = SessionEvent(
            "evt-1",
            SessionEventType.IDENTITY_RESOLVED,
            AnimalIdentityResolution.confirmed("cow-001"),
        )
        once = session.apply(event)
        twice = once.apply(event)
        self.assertEqual(once, twice)
        self.assertEqual(("evt-1",), twice.applied_event_ids)

    def test_completion_requires_confirmed_identity(self):
        session = Session.new()
        with self.assertRaises(ValueError):
            session.apply(SessionEvent("evt-2", SessionEventType.COMPLETE))

    def test_completion_is_terminal(self):
        session = Session.new().apply(
            SessionEvent(
                "evt-1",
                SessionEventType.IDENTITY_RESOLVED,
                AnimalIdentityResolution.confirmed("cow-001"),
            )
        )
        completed = session.apply(SessionEvent("evt-2", SessionEventType.COMPLETE))
        self.assertEqual(SessionState.COMPLETED, completed.state)
        with self.assertRaises(ValueError):
            completed.apply(SessionEvent("evt-3", SessionEventType.COMPLETE))


if __name__ == "__main__":
    unittest.main()
