from copy import deepcopy
from importlib import import_module
import json
from pathlib import Path
import unittest

from hoofcare.hmi.gen1.navigation import Gen1Route


MANIFEST = Path("dtools/gl100e/manifest.json")


class Generation1DToolsManifestTests(unittest.TestCase):
    def setUp(self):
        try:
            self.validator = import_module("scripts.check_gen1_dtools_manifest")
        except ModuleNotFoundError:
            self.fail("scripts.check_gen1_dtools_manifest must exist")
        self.assertTrue(MANIFEST.is_file(), "GL100E manifest must exist")
        self.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_covers_every_route_and_validates(self):
        self.validator.validate_manifest(self.data)
        self.assertEqual(
            {screen["route_id"] for screen in self.data["screens"]},
            {route.value for route in Gen1Route},
        )
        self.assertEqual(self.data["profile_id"], "gl100e-landscape-v1")
        self.assertEqual(self.data["canvas"], {"width": 1024, "height": 600})
        self.assertEqual(
            self.data["native_artifact"]["status"],
            "NATIVE_DTOOLS_ARTIFACT_REQUIRED",
        )

    def test_validator_rejects_unsafe_or_ambiguous_manifests(self):
        cases = []

        duplicate = deepcopy(self.data)
        duplicate["screens"].append(deepcopy(duplicate["screens"][0]))
        cases.append((duplicate, "duplicate screen ID"))

        unknown_route = deepcopy(self.data)
        unknown_route["screens"][0]["route_id"] = "G1-99"
        cases.append((unknown_route, "unknown route"))

        missing_label = deepcopy(self.data)
        missing_label["screens"][0]["label_pl"] = ""
        cases.append((missing_label, "Polish label"))

        untyped = deepcopy(self.data)
        del untyped["screens"][0]["widgets"][0]["binding"]["value_type"]
        cases.append((untyped, "typed binding"))

        too_many_actions = deepcopy(self.data)
        widget = deepcopy(too_many_actions["screens"][0]["widgets"][0])
        widget["widget_id"] = "fifth-primary-action"
        widget["primary_action"] = True
        too_many_actions["screens"][0]["widgets"] = [deepcopy(widget) for _ in range(5)]
        for index, item in enumerate(too_many_actions["screens"][0]["widgets"]):
            item["widget_id"] = f"primary-{index}"
        cases.append((too_many_actions, "more than four primary actions"))

        unsafe_write = deepcopy(self.data)
        unsafe_write["screens"][0]["widgets"][0]["binding"] = {
            "binding_id": "machine.write",
            "value_type": "BOOL",
            "direction": "COMMAND_REQUEST",
            "available_when": "ALWAYS",
            "missing_data": "DISABLED",
        }
        cases.append((unsafe_write, "approved local use case"))

        outside = deepcopy(self.data)
        outside["screens"][0]["widgets"][0]["geometry"]["x"] = 1024
        cases.append((outside, "outside 1024x600"))

        forbidden = deepcopy(self.data)
        forbidden["screens"][0]["widgets"][0]["binding"]["binding_id"] = "KVK.control"
        cases.append((forbidden, "forbidden binding"))

        for manifest, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    self.validator.validate_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
