from __future__ import annotations

import threading
from typing import Callable

from .backend import DToolsBackend


_PUBLIC_CONNECTION_CODES = frozenset(
    {
        "DTOOLS_NOT_FOUND",
        "AMBIGUOUS_WINDOW",
        "EXECUTABLE_MISMATCH",
        "PROJECT_MISMATCH",
        "WINDOWS_REQUIRED",
    }
)


class DeferredDToolsBackend:
    """Connect to the exact DTools window only when a tool needs it."""

    mechanism = "DEFERRED_WINDOWS_CONNECTION"

    def __init__(self, connect: Callable[[], DToolsBackend]) -> None:
        self._connect_callback = connect
        self._connected: DToolsBackend | None = None
        self._lock = threading.RLock()

    def connection_status(self) -> dict[str, object]:
        try:
            self._backend()
        except Exception as error:
            literal = str(error)
            code = (
                literal
                if literal in _PUBLIC_CONNECTION_CODES
                else "DTOOLS_CONNECTION_FAILED"
            )
            return {
                "available": False,
                "code": code,
                "mechanism": self.mechanism,
            }
        return {
            "available": True,
            "code": "CONNECTED",
            "mechanism": self.mechanism,
        }

    def snapshot(self):
        return self._backend().snapshot()

    def capture(self) -> bytes:
        return self._backend().capture()

    def diagnostic_texts(self) -> tuple[str, ...]:
        return self._backend().diagnostic_texts()

    def perform_named_step(self, name: str) -> None:
        self._backend().perform_named_step(name)

    def activate(self, control_id: str) -> None:
        self._backend().activate(control_id)

    def set_text(self, control_id: str, value: str) -> None:
        self._backend().set_text(control_id, value)

    def send_shortcut(self, shortcut_id: str) -> None:
        self._backend().send_shortcut(shortcut_id)

    def _backend(self) -> DToolsBackend:
        with self._lock:
            if self._connected is None:
                self._connected = self._connect_callback()
            return self._connected
