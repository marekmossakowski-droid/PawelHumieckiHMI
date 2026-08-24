from dataclasses import replace
from pathlib import Path
import unittest

from hoofcare.dtools_bridge.model import ActionKind, ActionRequest, WindowSnapshot
from hoofcare.dtools_bridge.policy import ActionPolicy


ALLOWLIST = Path("dtools/gl100e/bridge/allowlist.json")


class ActionPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = ActionPolicy.from_file(ALLOWLIST)
        self.snapshot = WindowSnapshot(
            pid=4242,
            process_name="KincoDToolsSynthetic.exe",
            executable_sha256="a" * 64,
            window_class="Afx:00400000",
            title="HoofCare_GL100E_G1 - [HMI0.whe]",
            project_name="HoofCare_GL100E_G1",
            active_dialog=None,
        )

    def test_allows_named_bitmap_editor_step_for_exact_project(self):
        request = ActionRequest(ActionKind.RUN_STEP, "open_bitmap_editor")
        snapshot = replace(
            self.snapshot, context="bitmap_component_dialog_open"
        )

        decision = self.policy.evaluate(request, snapshot)

        self.assertEqual(decision.code, "ALLOW")
        self.assertTrue(decision.allowed)

    def test_permanently_denies_download_even_if_named_like_a_step(self):
        request = ActionRequest(ActionKind.RUN_STEP, "download_project")

        decision = self.policy.evaluate(request, self.snapshot)

        self.assertEqual(decision.code, "DENIED_PERMANENT_BOUNDARY")
        self.assertFalse(decision.allowed)

    def test_denies_a_different_project_before_control_lookup(self):
        wrong = replace(self.snapshot, project_name="Production_Project")

        decision = self.policy.evaluate(
            ActionRequest(ActionKind.ACTIVATE, "bitmap_component"), wrong
        )

        self.assertEqual(decision.code, "PROJECT_MISMATCH")
        self.assertFalse(decision.allowed)

    def test_denies_changed_executable_hash(self):
        wrong = replace(self.snapshot, executable_sha256="b" * 64)

        decision = self.policy.evaluate(
            ActionRequest(ActionKind.CAPTURE, "capture"), wrong
        )

        self.assertEqual(decision.code, "EXECUTABLE_MISMATCH")
        self.assertFalse(decision.allowed)

    def test_unknown_target_is_not_implicitly_allowed(self):
        decision = self.policy.evaluate(
            ActionRequest(ActionKind.RUN_STEP, "open_anything"), self.snapshot
        )

        self.assertEqual(decision.code, "TARGET_NOT_ALLOWLISTED")
        self.assertFalse(decision.allowed)

    def test_unknown_dialog_stops_before_allowlisted_action(self):
        unexpected = replace(
            self.snapshot,
            active_dialog="Unexpected Dialog",
            context="unknown_dialog:Unexpected Dialog",
        )

        decision = self.policy.evaluate(
            ActionRequest(ActionKind.ACTIVATE, "edit_graphics"), unexpected
        )

        self.assertEqual(decision.code, "UNEXPECTED_DIALOG")
        self.assertFalse(decision.allowed)


if __name__ == "__main__":
    unittest.main()
