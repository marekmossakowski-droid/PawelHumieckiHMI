import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import uuid


@unittest.skipUnless(sys.platform == "win32", "Windows UI automation only")
class WindowsBackendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from hoofcare.dtools_bridge.windows_backend import (
            EmergencyHotkey,
            WindowsDToolsBackend,
        )

        cls.backend_type = WindowsDToolsBackend
        cls.hotkey_type = EmergencyHotkey

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.command_file = Path(self.temporary.name) / "command.txt"
        self.ready_file = Path(self.temporary.name) / "ready.json"
        self.project_name = f"HoofCare_GL100E_G1_TEST_{uuid.uuid4().hex}"
        self.emulator_pid = None
        self.process = subprocess.Popen(
            [
                sys.executable,
                "scripts/windows/dtools_bridge/DToolsBridgeEmulator.py",
                "--project",
                self.project_name,
                "--command-file",
                str(self.command_file),
                "--ready-file",
                str(self.ready_file),
            ]
        )
        self.addCleanup(self._stop_emulator)
        deadline = time.monotonic() + 10
        last_error = None
        while time.monotonic() < deadline:
            try:
                ready = json.loads(self.ready_file.read_text("utf-8"))
                self.emulator_pid = int(ready["pid"])
                if ready["title"] != f"{self.project_name} - [HMI0.whe]":
                    raise AssertionError("Emulator title handshake mismatch")
                executable = Path(ready["executable"])
                executable_hash = hashlib.sha256(executable.read_bytes()).hexdigest()
                self.backend = self.backend_type.connect_test_emulator(
                    project_name=self.project_name,
                    executable_path=executable,
                    executable_sha256=executable_hash,
                    process_id=self.emulator_pid,
                )
                break
            except Exception as error:
                last_error = error
                time.sleep(0.2)
        else:
            self.fail(f"Emulator did not become ready: {last_error}")

    def _stop_emulator(self):
        if self.emulator_pid is not None and self.emulator_pid != self.process.pid:
            subprocess.run(
                ["taskkill", "/PID", str(self.emulator_pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)

    def test_connect_exact_reads_project_and_capture_is_window_only_png(self):
        snapshot = self.backend.snapshot()

        self.assertEqual(snapshot.project_name, self.project_name)
        self.assertIsNone(snapshot.active_dialog)
        self.assertTrue(self.backend.capture().startswith(b"\x89PNG\r\n\x1a\n"))

    def test_unknown_dialog_is_reported_not_closed(self):
        self.command_file.write_text("show_unknown_dialog", encoding="utf-8")
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            snapshot = self.backend.snapshot()
            if snapshot.active_dialog == "Unexpected Dialog":
                break
            time.sleep(0.2)

        self.assertEqual(snapshot.active_dialog, "Unexpected Dialog")
        self.assertEqual(snapshot.context, "unknown_dialog:Unexpected Dialog")

    def test_windows_backend_exposes_only_named_action_methods(self):
        public = {
            name
            for name in dir(self.backend_type)
            if not name.startswith("_")
        }

        self.assertTrue(
            {
                "connect_exact",
                "connect_test_emulator",
                "snapshot",
                "capture",
                "diagnostic_texts",
                "perform_named_step",
                "activate",
                "set_text",
                "send_shortcut",
            }.issubset(public)
        )
        self.assertTrue({"click", "keypress", "execute"}.isdisjoint(public))

    def test_hotkey_registration_constants_are_fixed(self):
        self.assertEqual(self.hotkey_type.HOTKEY_ID, 0x4843)
        self.assertEqual(self.hotkey_type.VIRTUAL_KEY, 0x7B)


if __name__ == "__main__":
    unittest.main()
