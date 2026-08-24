from pathlib import Path
import tempfile
import unittest

from hoofcare.dtools_bridge.audit import AuditLog
from hoofcare.dtools_bridge.controller import BridgeController
from hoofcare.dtools_bridge.model import (
    ActionKind,
    ActionRequest,
    BridgeState,
    WindowSnapshot,
)
from hoofcare.dtools_bridge.policy import ActionPolicy
from hoofcare.dtools_bridge.session import SessionGuard


ALLOWLIST = Path("dtools/gl100e/bridge/allowlist.json")


class DeterministicBackend:
    def __init__(self, outcomes=None, context="bitmap_component_dialog_open"):
        self.context = context
        self.outcomes = outcomes or {}
        self.performed = []

    def snapshot(self):
        return WindowSnapshot(
            pid=4242,
            process_name="KincoDToolsSynthetic.exe",
            executable_sha256="a" * 64,
            window_class="Afx:00400000",
            title="HoofCare_GL100E_G1 - [HMI0.whe]",
            project_name="HoofCare_GL100E_G1",
            active_dialog=None,
            context=self.context,
        )

    def capture(self):
        return b"synthetic-png"

    def perform_named_step(self, name):
        self.performed.append(name)
        defaults = {
            "open_bitmap_component": "bitmap_component_dialog_open",
            "open_bitmap_editor": "bitmap_editor_open",
            "load_g1_00_bitmap": "g1_00_bitmap_visible",
            "verify_bitmap_loaded": "g1_00_bitmap_visible",
        }
        self.context = self.outcomes.get(name, defaults[name])

    def activate(self, control_id):
        self.performed.append(control_id)

    def set_text(self, control_id, value):
        self.performed.append(control_id)

    def send_shortcut(self, shortcut_id):
        self.performed.append(shortcut_id)


class BridgeControllerTests(unittest.TestCase):
    def make_controller(self, backend):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        session = SessionGuard()
        token = session.issue_token()
        controller = BridgeController(
            backend=backend,
            policy=ActionPolicy.from_file(ALLOWLIST),
            session=session,
            audit=AuditLog(Path(temporary.name), session_id="controller-test"),
        )
        return controller, token

    def test_executes_once_and_verifies_expected_postcondition(self):
        backend = DeterministicBackend()
        controller, token = self.make_controller(backend)

        result = controller.execute(
            token, ActionRequest(ActionKind.RUN_STEP, "open_bitmap_editor")
        )

        self.assertEqual(result.code, "OK")
        self.assertEqual(backend.performed, ["open_bitmap_editor"])
        self.assertEqual(result.postcondition, "bitmap_editor_open")

    def test_postcondition_mismatch_stops_session_without_retry(self):
        backend = DeterministicBackend(
            outcomes={"open_bitmap_editor": "main_editor"}
        )
        controller, token = self.make_controller(backend)

        result = controller.execute(
            token, ActionRequest(ActionKind.RUN_STEP, "open_bitmap_editor")
        )

        self.assertEqual(result.code, "POSTCONDITION_MISMATCH")
        self.assertEqual(backend.performed, ["open_bitmap_editor"])
        self.assertEqual(
            controller.session.state, BridgeState.STOPPED_FAIL_CLOSED
        )

    def test_denied_action_never_reaches_backend(self):
        backend = DeterministicBackend()
        controller, token = self.make_controller(backend)

        result = controller.execute(
            token, ActionRequest(ActionKind.RUN_STEP, "download_project")
        )

        self.assertEqual(result.code, "DENIED_PERMANENT_BOUNDARY")
        self.assertEqual(backend.performed, [])

    def test_backend_failure_stops_without_retry(self):
        class FailingBackend(DeterministicBackend):
            def perform_named_step(self, name):
                self.performed.append(name)
                raise RuntimeError("synthetic failure")

        backend = FailingBackend()
        controller, token = self.make_controller(backend)

        result = controller.execute(
            token, ActionRequest(ActionKind.RUN_STEP, "open_bitmap_editor")
        )

        self.assertEqual(result.code, "BACKEND_ERROR")
        self.assertEqual(backend.performed, ["open_bitmap_editor"])
        self.assertEqual(
            controller.session.state, BridgeState.STOPPED_FAIL_CLOSED
        )

    def test_precondition_read_failure_stops_before_any_action(self):
        class MissingWindowBackend(DeterministicBackend):
            def snapshot(self):
                raise RuntimeError("window disappeared")

        backend = MissingWindowBackend()
        controller, token = self.make_controller(backend)

        result = controller.execute(
            token, ActionRequest(ActionKind.RUN_STEP, "open_bitmap_editor")
        )

        self.assertEqual(result.code, "PRECONDITION_ERROR")
        self.assertEqual(backend.performed, [])
        self.assertEqual(
            controller.session.state, BridgeState.STOPPED_FAIL_CLOSED
        )

    def test_unknown_dialog_policy_denial_stops_without_action(self):
        backend = DeterministicBackend(
            context="unknown_dialog:Unexpected Dialog"
        )
        controller, token = self.make_controller(backend)

        result = controller.execute(
            token, ActionRequest(ActionKind.ACTIVATE, "edit_graphics")
        )

        self.assertEqual(result.code, "UNEXPECTED_DIALOG")
        self.assertEqual(backend.performed, [])
        self.assertEqual(
            controller.session.state, BridgeState.STOPPED_FAIL_CLOSED
        )


if __name__ == "__main__":
    unittest.main()
