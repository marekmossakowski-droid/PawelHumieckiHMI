import json
import tempfile
import tomllib
import unittest
from pathlib import Path

from hoofcare.integration.bench_mvp import BenchMvpScenario


class R2DERuntimeAndRfidTests(unittest.TestCase):
    def _write_config(self, root: Path) -> Path:
        config_path = root / "bench-runtime.json"
        config_path.write_text(
            json.dumps(
                {
                    "mode": "SYNTHETIC_TEST_ONLY",
                    "data_dir": str(root / "data"),
                    "report_dir": str(root / "reports"),
                    "network_enabled": False,
                    "kvk_connected": False,
                }
            ),
            encoding="utf-8",
        )
        return config_path

    def test_bench_runtime_has_local_config_schema_and_reproducible_launch(self):
        from hoofcare.runtime.bench import BenchRuntimeConfig, launch_bench_runtime

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = BenchRuntimeConfig.from_json_file(self._write_config(root))
            status = launch_bench_runtime(config)

            self.assertEqual(status["mode"], "SYNTHETIC_TEST_ONLY")
            self.assertFalse(status["network_enabled"])
            self.assertFalse(status["kvk_connected"])
            self.assertTrue(Path(status["data_dir"]).is_dir())
            self.assertTrue(Path(status["report_dir"]).is_dir())

    def test_bench_runtime_restart_reuses_canonical_local_directories(self):
        from hoofcare.runtime.bench import BenchRuntimeConfig, launch_bench_runtime

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = BenchRuntimeConfig.from_json_file(self._write_config(root))
            first = launch_bench_runtime(config)
            second = launch_bench_runtime(config)
            self.assertEqual(first["data_dir"], second["data_dir"])
            self.assertEqual(first["report_dir"], second["report_dir"])
            self.assertTrue(second["runtime_ready"])

    def test_package_declares_local_bench_console_entrypoint(self):
        payload = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(payload["project"]["scripts"]["hoofcare-bench"], "hoofcare.runtime.__main__:main")

    def test_bench_runtime_rejects_network_or_kvk_enablement(self):
        from hoofcare.runtime.bench import BenchRuntimeConfig

        with self.assertRaises(ValueError):
            BenchRuntimeConfig(
                mode="SYNTHETIC_TEST_ONLY",
                data_dir="data",
                report_dir="reports",
                network_enabled=True,
                kvk_connected=False,
            )
        with self.assertRaises(ValueError):
            BenchRuntimeConfig(
                mode="SYNTHETIC_TEST_ONLY",
                data_dir="data",
                report_dir="reports",
                network_enabled=False,
                kvk_connected=True,
            )

    def test_rfid_identity_is_derived_from_observation_payload(self):
        scenario = BenchMvpScenario.synthetic()
        result = scenario.run()
        self.assertEqual(result.session["animal_id"], "TEST-COW-001")

    def test_rfid_expected_identity_mismatch_fails_closed(self):
        scenario = BenchMvpScenario.synthetic()
        with self.assertRaisesRegex(ValueError, "RFID identity mismatch"):
            scenario.run(animal_id="OTHER-COW")


if __name__ == "__main__":
    unittest.main()
