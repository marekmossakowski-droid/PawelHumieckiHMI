import unittest

from hoofcare.physical.navigation import NavigationError, PhysicalNavigationController
from hoofcare.physical.layout import ScreenId


class PhysicalNavigationControllerTests(unittest.TestCase):
    def test_starts_on_dashboard(self):
        controller = PhysicalNavigationController.default()
        self.assertEqual(controller.current_screen, ScreenId.DASHBOARD)

    def test_start_session_moves_to_animal_session(self):
        controller = PhysicalNavigationController.default()
        controller.activate("start_session")
        self.assertEqual(controller.current_screen, ScreenId.ANIMAL_SESSION)

    def test_ambiguous_identity_cannot_advance(self):
        controller = PhysicalNavigationController.default()
        controller.activate("start_session")
        controller.bind_identity_status("AMBIGUOUS")
        with self.assertRaises(NavigationError):
            controller.activate("confirm_identity")
        self.assertEqual(controller.current_screen, ScreenId.ANIMAL_SESSION)

    def test_confirmed_identity_advances_to_limb_claw(self):
        controller = PhysicalNavigationController.default()
        controller.activate("start_session")
        controller.bind_identity_status("CONFIRMED")
        controller.activate("confirm_identity")
        self.assertEqual(controller.current_screen, ScreenId.LIMB_CLAW)

    def test_nominal_operator_flow_reaches_report_summary(self):
        controller = PhysicalNavigationController.default()
        controller.activate("start_session")
        controller.bind_identity_status("CONFIRMED")
        controller.activate("confirm_identity")
        controller.activate("select_limb")
        controller.activate("select_claw")
        controller.activate("select_zone")
        controller.activate("select_lesion")
        controller.activate("select_treatment")
        controller.activate("complete_session")
        self.assertEqual(controller.current_screen, ScreenId.REPORT_SUMMARY)

    def test_unknown_or_machine_control_actions_fail_closed(self):
        controller = PhysicalNavigationController.default()
        for action in ("open_valve", "kvk_command", "plc_write", "motor_start"):
            with self.assertRaises(NavigationError):
                controller.activate(action)

    def test_model_is_synthetic_only_and_has_no_kvk_connection(self):
        controller = PhysicalNavigationController.default()
        self.assertTrue(controller.isolated_synthetic_only)
        self.assertFalse(controller.kvk_connection_allowed)
        self.assertFalse(controller.real_farm_data_allowed)


if __name__ == "__main__":
    unittest.main()
