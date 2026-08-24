from pathlib import Path
import unittest
from unittest.mock import patch

from PIL import Image

from hoofcare.dtools_bridge.windows_backend import (
    WindowsBackendError,
    WindowsDToolsBackend,
)


class _Window:
    handle = 4321

    def rectangle(self):
        raise AssertionError("capture must bind to the exact window handle")


def _backend() -> WindowsDToolsBackend:
    return WindowsDToolsBackend(
        project_name="HoofCare_GL100E_G1",
        executable_path=Path("Kinco DTools.exe"),
        executable_sha256="0" * 64,
        process_id=7824,
        win32_application=object(),
        uia_application=object(),
        main_window=_Window(),
    )


class WindowCaptureTests(unittest.TestCase):
    def test_capture_reads_the_exact_dtools_window_handle(self):
        image = Image.new("RGB", (1024, 600), "white")

        with patch("PIL.ImageGrab.grab", return_value=image) as grab:
            payload = _backend().capture()

        grab.assert_called_once_with(window=4321)
        self.assertTrue(payload.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_capture_rejects_minimized_or_implausibly_small_evidence(self):
        image = Image.new("RGB", (160, 28), "black")

        with patch("PIL.ImageGrab.grab", return_value=image):
            with self.assertRaisesRegex(
                WindowsBackendError, "CAPTURE_BOUNDS_INVALID:160x28"
            ):
                _backend().capture()


if __name__ == "__main__":
    unittest.main()
