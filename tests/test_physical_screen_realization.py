import unittest

from hoofcare.physical.screen_realization import PhysicalScreenRealization, WidgetKind
from hoofcare.physical.layout import ScreenId


class PhysicalScreenRealizationTests(unittest.TestCase):
    def test_default_realization_maps_every_layout_screen(self):
        realization = PhysicalScreenRealization.default()
        self.assertEqual(set(realization.screens), set(ScreenId))
        self.assertTrue(realization.isolated_synthetic_only)
        self.assertFalse(realization.kvk_connection_allowed)
        self.assertFalse(realization.real_farm_data_allowed)

    def test_dashboard_preserves_banner_and_counters(self):
        dashboard = realization_screen(ScreenId.DASHBOARD)
        texts = {widget.text for widget in dashboard.widgets if widget.text}
        bindings = {widget.binding for widget in dashboard.widgets if widget.binding}
        self.assertIn("Paweł Humięcki the best zootechnik", texts)
        self.assertIn("completed_animals", bindings)
        self.assertIn("consumed_dressings", bindings)

    def test_interactive_widgets_keep_minimum_touch_target(self):
        realization = PhysicalScreenRealization.default()
        for screen in realization.screens.values():
            for widget in screen.widgets:
                if widget.kind == WidgetKind.BUTTON:
                    self.assertGreaterEqual(widget.width_px, 48)
                    self.assertGreaterEqual(widget.height_px, 48)

    def test_no_machine_control_widget_or_action_exists(self):
        realization = PhysicalScreenRealization.default()
        forbidden = {"kvk_command", "plc_write", "open_valve", "motor_start", "winch", "hydraulic"}
        all_ids = {widget.widget_id.lower() for screen in realization.screens.values() for widget in screen.widgets}
        all_actions = {widget.action.lower() for screen in realization.screens.values() for widget in screen.widgets if widget.action}
        for token in forbidden:
            self.assertTrue(all(token not in value for value in all_ids | all_actions))


def realization_screen(screen_id: ScreenId):
    return PhysicalScreenRealization.default().screens[screen_id]


if __name__ == "__main__":
    unittest.main()
