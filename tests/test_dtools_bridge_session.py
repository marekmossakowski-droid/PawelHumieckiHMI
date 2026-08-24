import unittest

from hoofcare.dtools_bridge.model import BridgeState
from hoofcare.dtools_bridge.session import (
    SessionAuthorizationError,
    SessionGuard,
    SessionStopped,
)


class SessionGuardTests(unittest.TestCase):
    def test_stop_invalidates_token_and_rejects_future_actions(self):
        guard = SessionGuard()
        token = guard.issue_token()

        guard.stop("operator_hotkey")

        with self.assertRaisesRegex(SessionStopped, "operator_hotkey"):
            guard.authorize(token)
        self.assertEqual(guard.state, BridgeState.STOPPED_FAIL_CLOSED)

    def test_emergency_stop_is_terminal_and_identifiable(self):
        guard = SessionGuard()
        token = guard.issue_token()

        guard.stop("ctrl_alt_f12", emergency=True)

        with self.assertRaises(SessionStopped):
            guard.authorize(token)
        self.assertEqual(guard.state, BridgeState.EMERGENCY_STOPPED)

    def test_new_session_uses_a_different_unguessable_token(self):
        first = SessionGuard().issue_token()
        second = SessionGuard().issue_token()

        self.assertNotEqual(first, second)
        self.assertGreaterEqual(len(first), 32)

    def test_wrong_token_is_rejected_without_stopping_valid_session(self):
        guard = SessionGuard()
        token = guard.issue_token()

        with self.assertRaises(SessionAuthorizationError):
            guard.authorize("wrong-token")

        guard.authorize(token)
        self.assertEqual(guard.state, BridgeState.ACTIVE)

    def test_save_request_enters_confirmation_gate(self):
        guard = SessionGuard()
        token = guard.issue_token()

        guard.request_save(token)

        self.assertEqual(guard.state, BridgeState.AWAITING_SAVE_CONFIRMATION)


if __name__ == "__main__":
    unittest.main()
