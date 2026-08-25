import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from hoofcare.integration.bench_mvp import BenchMvpScenario


class R2DERuntimeAndRfidV2Tests(unittest.TestCase):
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

    def _run_module(self, config_path: Path) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        src_path = str((Path(__file__).parent.parent / "src").resolve())
        env["PYTHONPATH"] = os.pathsep.join(
            value for value in (src_path, env.get("PYTHONPATH")) if value
        )
        return subprocess.run(
            [sys.executable, "-m", "hoofcare.runtime", str(config_path)],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def test_bench_runtime_reproducible_and_fail_closed(self):
        from hoofcare.runtime.bench import BenchRuntimeConfig, launch_bench_runtime

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = BenchRuntimeConfig.from_json_file(self._write_config(root))
            first = launch_bench_runtime(config)
            second = launch_bench_runtime(config)
            self.assertTrue(first["runtime_ready"])
            self.assertEqual(first["data_dir"], second["data_dir"])
            self.assertFalse(first["network_enabled"])
            self.assertFalse(first["kvk_connected"])

    def test_module_entrypoint_rejects_invalid_config_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_path = self._write_config(Path(tmp))
            payload = json.loads(config_path.read_text(encoding="utf-8"))
            payload["network_enabled"] = True
            config_path.write_text(json.dumps(payload), encoding="utf-8")
            completed = self._run_module(config_path)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("ERROR: bench runtime configuration invalid:", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)

    def test_rfid_identity_comes_from_observation_and_mismatch_fails_closed(self):
        result = BenchMvpScenario.synthetic().run()
        self.assertEqual(result.session["animal_id"], "TEST-COW-001")
        with self.assertRaisesRegex(ValueError, "RFID identity mismatch"):
            BenchMvpScenario.synthetic().run(animal_id="OTHER-COW")


if __name__ == "__main__":
    unittest.main()
