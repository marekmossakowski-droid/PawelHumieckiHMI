from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ActionKind(StrEnum):
    INSPECT = "inspect"
    CAPTURE = "capture"
    ACTIVATE = "activate"
    OPEN_MENU = "open_menu"
    SET_TEXT = "set_text"
    SEND_SHORTCUT = "send_shortcut"
    RUN_STEP = "run_step"
    REQUEST_SAVE = "request_save"
    EMERGENCY_STOP = "emergency_stop"


class BridgeState(StrEnum):
    IDLE = "idle"
    ACTIVE = "active"
    AWAITING_SAVE_CONFIRMATION = "awaiting_save_confirmation"
    STOPPED_FAIL_CLOSED = "stopped_fail_closed"
    EMERGENCY_STOPPED = "emergency_stopped"


@dataclass(frozen=True)
class WindowSnapshot:
    pid: int
    process_name: str
    executable_sha256: str
    window_class: str
    title: str
    project_name: str
    active_dialog: str | None
    context: str = "main_editor"


@dataclass(frozen=True)
class ActionRequest:
    kind: ActionKind
    target: str
    value: str | None = None


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    code: str
    reason: str


@dataclass(frozen=True)
class ActionResult:
    code: str
    message: str
    postcondition: str | None = None
    evidence_before: str | None = None
    evidence_after: str | None = None
