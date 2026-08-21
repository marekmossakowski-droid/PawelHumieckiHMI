import unittest

from hoofcare.physical.layout import PhysicalHmiLayout, ScreenId


class PhysicalHmiLayoutTests(unittest.TestCase):
    def test_default_layout_targets_10_1_inch_1024x600_panel(self):
        layout = PhysicalHmiLayout.default()
        self.assertEqual(layout.width_px, 1024)
        self.assertEqual(layout.height_px, 600)
        self.assertEqual(layout.panel_class_inch, 10.1)

    def test_primary_touch_targets_are_at_least_48_pixels(self):
        layout = PhysicalHmiLayout.default()
        for target in layout.touch_targets:
            self.assertGreaterEqual(target.width_px, 48)
            self.assertGreaterEqual(target.height_px, 48)

    def test_required_screens_are_mapped(self):
        layout = PhysicalHmiLayout.default()
        self.assertEqual(
            set(layout.screens),
            {
                ScreenId.DASHBOARD,
                ScreenId.ANIMAL_SESSION,
                ScreenId.LIMB_CLAW,
                ScreenId.ZONE_LESION,
                ScreenId.TREATMENT,
                ScreenId.REPORT_SUMMARY,
            },
        )

    def test_dashboard_preserves_required_banner_and_counters(self):
        dashboard = PhysicalHmiLayout.default().screens[ScreenId.DASHBOARD]
        self.assertIn("Paweł Humięcki the best zootechnik", dashboard.text_tokens)
        self.assertIn("completed_animals", dashboard.data_bindings)
        self.assertIn("consumed_dressings", dashboard.data_bindings)

    def test_layout_exposes_no_machine_control_affordances(self):
        forbidden = {"command", "actuate", "open_gate", "close_gate", "hydraulics", "plc_write"}
        layout = PhysicalHmiLayout.default()
        labels = {label.lower() for screen in layout.screens.values() for label in screen.control_ids}
        self.assertTrue(labels.isdisjoint(forbidden))


if __name__ == "__main__":
    unittest.main()
