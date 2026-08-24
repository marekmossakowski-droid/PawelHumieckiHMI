from pathlib import Path
import sys
from types import ModuleType
import unittest
from unittest.mock import patch

from hoofcare.dtools_bridge.windows_backend import WindowsDToolsBackend


class _Window:
    handle = 4321


class _Application:
    def __init__(self, *, backend):
        self.backend = backend
        self.connection = None

    def connect(self, **target):
        self.connection = target
        return self


class WindowBindingTests(unittest.TestCase):
    def test_exact_window_binding_does_not_reopen_connection_by_process_id(self):
        pywinauto = ModuleType("pywinauto")
        pywinauto.Application = _Application

        with patch.dict(sys.modules, {"pywinauto": pywinauto}):
            backend = WindowsDToolsBackend._connect_pid(
                "HoofCare_GL100E_G1",
                Path("Kinco DTools.exe"),
                "0" * 64,
                22856,
                _Window(),
            )

        self.assertEqual(backend._win32_application.connection, {"handle": 4321})
        self.assertEqual(backend._uia_application.connection, {"handle": 4321})
        self.assertEqual(backend.process_id, 22856)


if __name__ == "__main__":
    unittest.main()
