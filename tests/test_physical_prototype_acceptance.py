from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest

from hoofcare.domain.session import (
    AnimalIdentityResolution,
    Session,
    SessionEvent,
    SessionEventType,
)
from hoofcare.physical.acceptance import PhysicalPrototypeAcceptance


class PhysicalPrototypeAcceptanceTests(unittest.TestCase):
    def _committed_session(self) -> Session:
        session = Session.new()
        session = session.apply(
            SessionEvent(
                event_id="identity-1",
                event_type=SessionEventType.IDENTITY_RESOLVED,
                payload=AnimalIdentityResolution.confirmed("TEST-COW-001"),
            )
        )
        return session.apply(SessionEvent(event_id="complete-1", event_type=SessionEventType.COMPLETE))

    def test_acceptance_summary_closes_isolated_physical_prototype(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            acceptance = PhysicalPrototypeAcceptance(Path(tmp))
            summary = acceptance.run(
                self._committed_session(),
                report_id="REPORT-TEST-001",
                generated_at=datetime(2026, 8, 21, 19, 45, tzinfo=timezone.utc),
            )

            self.assertTrue(summary.accepted)
            self.assertTrue(summary.restart_recovery_verified)
            self.assertTrue(summary.canonical_pdf_verified)
            self.assertTrue(summary.negative_controls_verified)
            self.assertFalse(summary.kvk_connection_allowed)
            self.assertFalse(summary.real_farm_data_allowed)
            self.assertIn(b"%PDF-1.4", summary.pdf_bytes)
            self.assertIn(b"Source-Session-ID:", summary.pdf_bytes)

    def test_machine_control_actions_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            acceptance = PhysicalPrototypeAcceptance(Path(tmp))
            for action in ("open_valve", "kvk_command", "plc_write", "motor_start"):
                with self.assertRaises(ValueError):
                    acceptance.assert_operator_action_allowed(action)

    def test_unresolved_session_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            acceptance = PhysicalPrototypeAcceptance(Path(tmp))
            with self.assertRaises(ValueError):
                acceptance.run(
                    Session.new(),
                    report_id="REPORT-TEST-002",
                    generated_at=datetime(2026, 8, 21, 19, 45, tzinfo=timezone.utc),
                )


if __name__ == "__main__":
    unittest.main()
