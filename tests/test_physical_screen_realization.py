import unittest

from hoofcare.physical.layout import PhysicalHmiLayout, ScreenId
from hoofcare.physical.screen_realization import PhysicalScreenRealization


class PhysicalScreenRealizationTests(unittest.TestCase):
    def setUp(self):
        self.layout = PhysicalHmiLayout.default()
        self.realization = PhysicalScreenRealization.from_layout(self.layout)

    def test_all_layout_screens_have_realized_widgets(self):
        self.assertEqual(set(self.realization.screens), set(ScreenId))
        for screen_id in ScreenId:
            self.assertGreater(len(self.realization.screens[screen_id].widgets), 0)

    def test_dashboard_preserves_banner_and_counters(self):
        dashboard = self.realization.screens[ScreenId.DASHBOARD]
        self.assertIn("Paweł Humięcki the best zootechnik", dashboard.static_text)
        bindings = {widget.binding for widget in dashboard.widgets if widget.binding}
        self.assertIn("completed_animals", bindings)
        self.assertIn("consumed_dressings", bindings)

    def test_primary_controls_are_touch_sized(self):
        for screen in self.realization.screens.values():
            for widget in screen.widgets:
                if widget.interactive:
                    self.assertGreaterEqual(widget.width_px, 48)
                    self.assertGreaterEqual(widget.height_px, 48)

    def test_identity_confirmation_is_fail_closed_when_ambiguous(self):
        screen = self.realization.render(ScreenId.ANIMAL_SESSION, {"identity_status": "AMBIGUOUS"})
        confirm = next(widget for widget in screen.widgets if widget.widget_id == "confirm_identity")
        self.assertFalse(confirm.enabled)

    def test_no_machine_control_widgets_exist(self):
        forbidden = ("kvk", "hydraulic", "plc", "actuate", "command", "write", "valve", "motor", "gate", "winch")
        for screen in self.realization.screens.values():
            for widget in screen.widgets:
                lowered = widget.widget_id.lower()
                self.assertFalse(any(token in lowered for token in forbidden))
        self.assertFalse(hasattr(self.realization, "command_kvk"))
        self.assertFalse(hasattr(self.realization, "write_kvk"))
        self.assertFalse(hasattr(self.realization, "actuate"))

    def test_realization_remains_isolated_and_synthetic_only(self):
        self.assertTrue(self.realization.isolated_synthetic_only)
        self.assertFalse(self.realization.kvk_connection_allowed)
        self.assertFalse(self.realization.real_farm_data_allowed)


if __name__ == "__main__":
    unittest.main()
