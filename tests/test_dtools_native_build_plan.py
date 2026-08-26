from pathlib import Path
import unittest

from hoofcare.dtools_bridge.native_build import NativeDToolsBuildPlan


class NativeDToolsBuildPlanTests(unittest.TestCase):
    def test_manifest_materializes_exact_fresh_gl100e_build_plan(self):
        plan = NativeDToolsBuildPlan.from_manifest(
            Path("dtools/gl100e/manifest.json")
        )

        self.assertEqual(plan.project_name, "HoofCare_GL100E_G1")
        self.assertEqual(plan.canvas, (1024, 600))
        self.assertEqual(len(plan.screens), 21)
        self.assertEqual(sum(len(screen.widgets) for screen in plan.screens), 69)
        self.assertEqual(plan.screens[0].screen_id, "G1-00")
        self.assertEqual(plan.screens[-1].screen_id, "G1-60")
        self.assertEqual(
            plan.screens[0].widgets[1].binding_id,
            "action.open_dashboard",
        )
        self.assertEqual(
            plan.screens[0].widgets[1].geometry,
            (148, 536, 232, 64),
        )
        self.assertEqual(len(plan.source_sha256), 64)

    def test_duplicate_screen_id_is_rejected_before_dtools_mutation(self):
        source = Path("dtools/gl100e/manifest.json").read_text("utf-8")
        duplicate = source.replace('"screen_id": "G1-10"', '"screen_id": "G1-00"', 1)

        with self.assertRaisesRegex(ValueError, "DUPLICATE_SCREEN_ID:G1-00"):
            NativeDToolsBuildPlan.from_json(duplicate)

    def test_out_of_bounds_widget_is_rejected_before_dtools_mutation(self):
        source = Path("dtools/gl100e/manifest.json").read_text("utf-8")
        outside = source.replace('"x": 24,', '"x": 2000,', 1)

        with self.assertRaisesRegex(ValueError, "WIDGET_OUT_OF_BOUNDS"):
            NativeDToolsBuildPlan.from_json(outside)


if __name__ == "__main__":
    unittest.main()
