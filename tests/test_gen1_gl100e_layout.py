from importlib import import_module
import unittest

from hoofcare.hmi.gen1.navigation import Gen1Route


class Generation1Gl100eLayoutTests(unittest.TestCase):
    def test_every_gl100e_target_fits_and_is_at_least_64_px(self):
        try:
            module = import_module("hoofcare.physical.gen1_layout")
        except ModuleNotFoundError:
            self.fail("hoofcare.physical.gen1_layout must exist")

        profile = module.Gl100eProfile.default()
        self.assertEqual((profile.width, profile.height), (1024, 600))
        self.assertTrue(hasattr(profile, "visual_system_id"), "visual system ID is required")
        self.assertEqual(profile.visual_system_id, "UX-HC-002-A1/G1-LIGHT-A")
        self.assertEqual(profile.color_tokens["surface.canvas"], "#F2F4F7")
        self.assertEqual(profile.color_tokens["action.primary"], "#1477FF")
        self.assertEqual(profile.color_tokens["assist.violet"], "#665CF6")
        self.assertEqual(
            {screen.route for screen in profile.screens},
            set(Gen1Route),
        )
        for screen in profile.screens:
            self.assertTrue(screen.within_canvas(profile.width, profile.height))
            self.assertFalse(screen.has_overlaps())
            self.assertLessEqual(len(screen.targets), 4)
            self.assertTrue(
                all(target.width >= 64 and target.height >= 64 for target in screen.targets)
            )

    def test_profile_keeps_geometry_out_of_semantic_route_values(self):
        self.assertFalse(any("1024" in route.value or "600" in route.value for route in Gen1Route))


if __name__ == "__main__":
    unittest.main()
