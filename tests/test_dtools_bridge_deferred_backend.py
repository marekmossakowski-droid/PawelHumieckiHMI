import unittest

from hoofcare.dtools_bridge.__main__ import build_backend
from hoofcare.dtools_bridge.deferred_backend import DeferredDToolsBackend


class ConnectedBackend:
    def snapshot(self):
        return "snapshot"

    def capture(self):
        return b"capture"

    def diagnostic_texts(self):
        return ("Ready",)

    def perform_named_step(self, name):
        self.last_step = name

    def activate(self, control_id):
        self.last_control = control_id

    def set_text(self, control_id, value):
        self.last_text = (control_id, value)

    def send_shortcut(self, shortcut_id):
        self.last_shortcut = shortcut_id


class DeferredDToolsBackendTests(unittest.TestCase):
    def test_runtime_builder_does_not_connect_during_mcp_startup(self):
        attempts = []

        def connect(project_name, executable_path, executable_sha256):
            attempts.append(
                (project_name, str(executable_path), executable_sha256)
            )
            raise RuntimeError("DTOOLS_NOT_FOUND")

        backend = build_backend(
            project_name="HoofCare_GL100E_G1",
            executable_path="C:/Kinco/DTools.exe",
            executable_sha256="a" * 64,
            connect_exact=connect,
        )

        self.assertEqual(attempts, [])
        self.assertFalse(backend.connection_status()["available"])
        self.assertEqual(len(attempts), 1)

    def test_unavailable_window_is_status_not_startup_failure(self):
        attempts = []

        def connect():
            attempts.append("connect")
            raise RuntimeError("DTOOLS_NOT_FOUND")

        backend = DeferredDToolsBackend(connect)

        self.assertEqual(
            backend.connection_status(),
            {
                "available": False,
                "code": "DTOOLS_NOT_FOUND",
                "mechanism": "DEFERRED_WINDOWS_CONNECTION",
            },
        )
        self.assertEqual(attempts, ["connect"])

    def test_successful_connection_is_cached_and_delegates_real_behavior(self):
        connected = ConnectedBackend()
        attempts = []

        def connect():
            attempts.append("connect")
            return connected

        backend = DeferredDToolsBackend(connect)

        self.assertEqual(
            backend.connection_status(),
            {
                "available": True,
                "code": "CONNECTED",
                "mechanism": "DEFERRED_WINDOWS_CONNECTION",
            },
        )
        self.assertEqual(backend.snapshot(), "snapshot")
        self.assertEqual(backend.capture(), b"capture")
        self.assertEqual(attempts, ["connect"])

    def test_unknown_connection_error_is_redacted(self):
        def connect():
            raise RuntimeError("C:\\secret\\unexpected failure")

        backend = DeferredDToolsBackend(connect)

        self.assertEqual(
            backend.connection_status(),
            {
                "available": False,
                "code": "DTOOLS_CONNECTION_FAILED",
                "mechanism": "DEFERRED_WINDOWS_CONNECTION",
            },
        )


if __name__ == "__main__":
    unittest.main()
