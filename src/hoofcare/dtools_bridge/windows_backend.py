from __future__ import annotations

from io import BytesIO
import ctypes
from ctypes import wintypes
import hashlib
import os
from pathlib import Path
import queue
import sys
import threading
from typing import Any, Callable

from .model import WindowSnapshot


class WindowsBackendError(RuntimeError):
    """Fail-closed Windows UI discovery or action error."""


def _require_windows() -> None:
    if sys.platform != "win32":
        raise WindowsBackendError("WINDOWS_REQUIRED")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class WindowsDToolsBackend:
    _KNOWN_DIALOG_CONTEXTS = {
        "Bitmap Component Attribute": "bitmap_component_dialog_open",
        "Graphics Library": "bitmap_editor_open",
    }

    def __init__(
        self,
        *,
        project_name: str,
        executable_path: Path,
        executable_sha256: str,
        process_id: int,
        win32_application: Any,
        uia_application: Any,
        main_window: Any,
        mechanism: str = "WIN32",
    ) -> None:
        self.project_name = project_name
        self.executable_path = executable_path
        self.executable_sha256 = executable_sha256.lower()
        self.process_id = process_id
        self._win32_application = win32_application
        self._uia_application = uia_application
        self._main_window = main_window
        self.mechanism = mechanism

    @classmethod
    def connect_exact(
        cls,
        project_name: str,
        executable_path: str | Path,
        executable_sha256: str,
    ) -> "WindowsDToolsBackend":
        _require_windows()
        path = Path(executable_path).resolve(strict=True)
        actual_hash = _sha256(path)
        if actual_hash.casefold() != executable_sha256.casefold():
            raise WindowsBackendError("EXECUTABLE_MISMATCH")

        from pywinauto import Desktop

        candidates: list[tuple[int, Any]] = []
        for window in Desktop(backend="win32").windows():
            try:
                pid = int(window.process_id())
                if not window.is_visible():
                    continue
                candidate_path = Path(_process_image_path(pid)).resolve()
                if os.path.normcase(str(candidate_path)) != os.path.normcase(str(path)):
                    continue
                if project_name not in window.window_text():
                    continue
                candidates.append((pid, window))
            except (OSError, RuntimeError, ValueError):
                continue
        if not candidates:
            raise WindowsBackendError("DTOOLS_NOT_FOUND")
        if len(candidates) != 1:
            raise WindowsBackendError("AMBIGUOUS_WINDOW")
        return cls._connect_pid(
            project_name, path, actual_hash, candidates[0][0], candidates[0][1]
        )

    @classmethod
    def connect_test_emulator(
        cls,
        *,
        project_name: str,
        executable_path: str | Path,
        executable_sha256: str,
        process_id: int,
    ) -> "WindowsDToolsBackend":
        """Explicit test-only connection; production discovery never calls it."""
        _require_windows()
        path = Path(executable_path).resolve(strict=True)
        actual_hash = _sha256(path)
        if actual_hash.casefold() != executable_sha256.casefold():
            raise WindowsBackendError("EXECUTABLE_MISMATCH")

        from pywinauto import Desktop

        expected_title = f"{project_name} - [HMI0.whe]"
        windows = Desktop(backend="win32").windows(
            process=process_id,
            title=expected_title,
            visible_only=True,
        )
        if not windows:
            raise WindowsBackendError("DTOOLS_NOT_FOUND")
        if len(windows) != 1:
            raise WindowsBackendError("AMBIGUOUS_WINDOW")
        window = windows[0]
        backend = cls._connect_pid(
            project_name, path, actual_hash, process_id, window
        )
        backend.mechanism = "TEST_EMULATOR"
        return backend

    @classmethod
    def _connect_pid(
        cls,
        project_name: str,
        executable_path: Path,
        executable_sha256: str,
        process_id: int,
        main_window: Any,
    ) -> "WindowsDToolsBackend":
        from pywinauto import Application

        window_handle = int(main_window.handle)
        win32_app = Application(backend="win32").connect(handle=window_handle)
        uia_app = Application(backend="uia").connect(handle=window_handle)
        return cls(
            project_name=project_name,
            executable_path=executable_path,
            executable_sha256=executable_sha256,
            process_id=process_id,
            win32_application=win32_app,
            uia_application=uia_app,
            main_window=main_window,
        )

    def snapshot(self) -> WindowSnapshot:
        if _sha256(self.executable_path) != self.executable_sha256:
            raise WindowsBackendError("EXECUTABLE_MISMATCH")
        title = self._main_window.window_text()
        if self.project_name not in title:
            raise WindowsBackendError("PROJECT_MISMATCH")
        dialogs = [
            window
            for window in self._win32_application.windows()
            if window.handle != self._main_window.handle and window.is_visible()
        ]
        active_dialog = None
        context = "main_editor"
        if dialogs:
            active_dialog = dialogs[0].window_text() or "UNKNOWN_DIALOG"
            context = self._KNOWN_DIALOG_CONTEXTS.get(
                active_dialog, f"unknown_dialog:{active_dialog}"
            )
            if self._contains_text(dialogs[0], "G1-00"):
                context = "g1_00_bitmap_visible"
        return WindowSnapshot(
            pid=self.process_id,
            process_name=self.executable_path.name,
            executable_sha256=self.executable_sha256,
            window_class=self._main_window.class_name(),
            title=title,
            project_name=self.project_name,
            active_dialog=active_dialog,
            context=context,
        )

    def capture(self) -> bytes:
        from PIL import ImageGrab

        image = ImageGrab.grab(window=int(self._main_window.handle))
        if image.width < 640 or image.height < 480:
            raise WindowsBackendError(
                f"CAPTURE_BOUNDS_INVALID:{image.width}x{image.height}"
            )
        payload = BytesIO()
        image.save(payload, format="PNG")
        return payload.getvalue()

    def perform_named_step(self, name: str) -> None:
        steps: dict[str, Callable[[], None]] = {
            "open_bitmap_component": lambda: self._select_menu(
                "Components->Graph And Animation->Bitmap"
            ),
            "open_bitmap_editor": lambda: self.activate("edit_graphics"),
            "load_g1_00_bitmap": self._load_g1_00_bitmap,
            "verify_bitmap_loaded": lambda: None,
            "components.graph_and_animation.bitmap": lambda: self._select_menu(
                "Components->Graph And Animation->Bitmap"
            ),
            "draw.load_image": lambda: self._select_menu("Draw->Load Image"),
        }
        try:
            action = steps[name]
        except KeyError as error:
            raise WindowsBackendError("TARGET_NOT_ALLOWLISTED") from error
        action()

    def activate(self, control_id: str) -> None:
        titles = {
            "bitmap_component": "Bitmap Component",
            "edit_graphics": "Edit Graphics",
            "import_graphics": "Import Graphics",
        }
        try:
            title = titles[control_id]
        except KeyError as error:
            raise WindowsBackendError("TARGET_NOT_ALLOWLISTED") from error
        control = self._single_control(title)
        control.click_input()

    def set_text(self, control_id: str, value: str) -> None:
        if control_id != "new_graphics_name":
            raise WindowsBackendError("TARGET_NOT_ALLOWLISTED")
        control = self._single_control("New graphics name")
        control.set_edit_text(value)

    def send_shortcut(self, shortcut_id: str) -> None:
        if shortcut_id != "escape":
            raise WindowsBackendError("TARGET_NOT_ALLOWLISTED")
        self._main_window.type_keys("{ESC}", set_foreground=False)

    def _select_menu(self, path: str) -> None:
        self._main_window.menu_select(path)

    def _load_g1_00_bitmap(self) -> None:
        if self.mechanism != "TEST_EMULATOR":
            raise WindowsBackendError("PROFILE_STEP_UNVERIFIED")
        self.activate("import_graphics")

    def _single_control(self, title: str) -> Any:
        candidates = []
        for window in self._win32_application.windows():
            if not window.is_visible():
                continue
            candidates.extend(window.descendants(title=title))
        if len(candidates) != 1:
            raise WindowsBackendError(f"CONTROL_MATCH_COUNT:{title}:{len(candidates)}")
        return candidates[0]

    @staticmethod
    def _contains_text(window: Any, text: str) -> bool:
        try:
            return any(text in value for value in window.texts())
        except (AttributeError, RuntimeError):
            return False


class EmergencyHotkey:
    HOTKEY_ID = 0x4843
    VIRTUAL_KEY = 0x7B
    _MOD_ALT = 0x0001
    _MOD_CONTROL = 0x0002
    _WM_HOTKEY = 0x0312
    _WM_QUIT = 0x0012

    def __init__(self) -> None:
        self._thread: threading.Thread | None = None
        self._thread_id: int | None = None
        self._callback: Callable[[], None] | None = None
        self._ready = threading.Event()
        self._errors: queue.Queue[BaseException] = queue.Queue(maxsize=1)

    def start(self, callback: Callable[[], None]) -> None:
        _require_windows()
        if self._thread is not None:
            raise WindowsBackendError("HOTKEY_ALREADY_STARTED")
        self._callback = callback
        self._thread = threading.Thread(
            target=self._run, name="DToolsBridgeEmergencyHotkey", daemon=True
        )
        self._thread.start()
        if not self._ready.wait(timeout=5):
            raise WindowsBackendError("HOTKEY_START_TIMEOUT")
        if not self._errors.empty():
            raise WindowsBackendError(str(self._errors.get_nowait()))

    def close(self) -> None:
        if self._thread_id is None:
            return
        ctypes.windll.user32.PostThreadMessageW(
            self._thread_id, self._WM_QUIT, 0, 0
        )
        if self._thread is not None:
            self._thread.join(timeout=5)
        self._thread = None
        self._thread_id = None

    def _run(self) -> None:
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        self._thread_id = int(kernel32.GetCurrentThreadId())
        if not user32.RegisterHotKey(
            None,
            self.HOTKEY_ID,
            self._MOD_CONTROL | self._MOD_ALT,
            self.VIRTUAL_KEY,
        ):
            self._errors.put(WindowsBackendError("HOTKEY_REGISTRATION_FAILED"))
            self._ready.set()
            return
        self._ready.set()
        message = wintypes.MSG()
        try:
            while user32.GetMessageW(ctypes.byref(message), None, 0, 0) > 0:
                if message.message == self._WM_HOTKEY and self._callback is not None:
                    self._callback()
        finally:
            user32.UnregisterHotKey(None, self.HOTKEY_ID)


def _process_image_path(process_id: int) -> str:
    _require_windows()
    process_query_limited_information = 0x1000
    kernel32 = ctypes.windll.kernel32
    kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.QueryFullProcessImageNameW.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPWSTR,
        ctypes.POINTER(wintypes.DWORD),
    ]
    kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    handle = kernel32.OpenProcess(
        process_query_limited_information, False, process_id
    )
    if not handle:
        raise OSError(f"Cannot open process {process_id}.")
    try:
        size = wintypes.DWORD(32768)
        buffer = ctypes.create_unicode_buffer(size.value)
        if not kernel32.QueryFullProcessImageNameW(
            handle, 0, buffer, ctypes.byref(size)
        ):
            raise OSError(f"Cannot read executable path for process {process_id}.")
        return buffer.value
    finally:
        kernel32.CloseHandle(handle)
