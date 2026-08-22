import unittest

from hoofcare.physical.layout import PhysicalHmiLayout, ScreenId
from hoofcare.physical.navigation import PhysicalNavigationController


class R2HmiNavigationGeometryTests(unittest.TestCase):
    def test_dashboard_open_reports_navigates_to_report_summary(self):
        controller = PhysicalNavigationController.default()
        controller.activate("open_reports")
        self.assertEqual(controller.current_screen, ScreenId.REPORT_SUMMARY)

    def test_back_navigation_is_intentional_across_workflow(self):
        controller = PhysicalNavigationController.default()
        controller.activate("start_session")
        controller.bind_identity_status("CONFIRMED")
        controller.activate("confirm_identity")
        self.assertEqual(controller.current_screen, ScreenId.LIMB_CLAW)

        controller.activate("back")
        self.assertEqual(controller.current_screen, ScreenId.ANIMAL_SESSION)

        controller.activate("confirm_identity")
        controller.activate("select_limb")
        controller.activate("select_claw")
        self.assertEqual(controller.current_screen, ScreenId.ZONE_LESION)

        controller.activate("back")
        self.assertEqual(controller.current_screen, ScreenId.LIMB_CLAW)

        controller.activate("select_limb")
        controller.activate("select_claw")
        controller.activate("select_zone")
        controller.activate("select_lesion")
        self.assertEqual(controller.current_screen, ScreenId.TREATMENT)

        controller.activate("back")
        self.assertEqual(controller.current_screen, ScreenId.ZONE_LESION)

    def test_all_touch_targets_have_concrete_coordinates_and_fit_panel(self):
        layout = PhysicalHmiLayout.default()
        self.assertEqual((layout.width_px, layout.height_px), (1024, 600))
        for target in layout.touch_targets:
            self.assertGreaterEqual(target.x_px, 0)
            self.assertGreaterEqual(target.y_px, 0)
            self.assertLessEqual(target.x_px + target.width_px, layout.width_px)
            self.assertLessEqual(target.y_px + target.height_px, layout.height_px)
            self.assertIsInstance(target.screen_id, ScreenId)

    def test_touch_targets_do_not_overlap_on_same_screen(self):
        layout = PhysicalHmiLayout.default()
        for screen_id in ScreenId:
            targets = [target for target in layout.touch_targets if target.screen_id is screen_id]
            for index, first in enumerate(targets):
                for second in targets[index + 1:]:
                    separated = (
                        first.x_px + first.width_px <= second.x_px
                        or second.x_px + second.width_px <= first.x_px
                        or first.y_px + first.height_px <= second.y_px
                        or second.y_px + second.height_px <= first.y_px
                    )
                    self.assertTrue(
                        separated,
                        f"overlap on {screen_id.value}: {first.control_id} vs {second.control_id}",
                    )


if __name__ == "__main__":
    unittest.main()
