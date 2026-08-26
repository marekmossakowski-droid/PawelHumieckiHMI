from pathlib import Path
import tempfile
import unittest

from PIL import Image

from hoofcare.dtools_bridge.native_assets import render_native_screen_assets
from hoofcare.dtools_bridge.native_build import NativeDToolsBuildPlan


class NativeDToolsAssetTests(unittest.TestCase):
    def test_renders_one_exact_gl100e_png_per_manifest_screen(self):
        plan = NativeDToolsBuildPlan.from_manifest(
            Path("dtools/gl100e/manifest.json")
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)

            assets = render_native_screen_assets(plan, output)

            self.assertEqual(len(assets), 21)
            self.assertEqual(assets[0].path.name, "G1-00.png")
            self.assertEqual(assets[-1].path.name, "G1-60.png")
            self.assertTrue(all(len(asset.sha256) == 64 for asset in assets))
            with Image.open(assets[0].path) as image:
                self.assertEqual(image.size, (1024, 600))
                self.assertEqual(image.mode, "RGB")
                self.assertEqual(image.info["screen_id"], "G1-00")

    def test_render_is_byte_deterministic(self):
        plan = NativeDToolsBuildPlan.from_manifest(
            Path("dtools/gl100e/manifest.json")
        )
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_assets = render_native_screen_assets(plan, Path(first))
            second_assets = render_native_screen_assets(plan, Path(second))

            self.assertEqual(
                [asset.sha256 for asset in first_assets],
                [asset.sha256 for asset in second_assets],
            )


if __name__ == "__main__":
    unittest.main()
