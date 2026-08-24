from __future__ import annotations

import hmac
import secrets
import threading

from .model import BridgeState


class SessionError(RuntimeError):
    """Base error for local bridge session failures."""


class SessionAuthorizationError(SessionError):
    """Raised when a caller does not hold the current session token."""


class SessionStopped(SessionError):
    """Raised after the bridge has entered a terminal stopped state."""


class SessionGuard:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._state = BridgeState.IDLE
        self._token: str | None = None
        self._stop_reason: str | None = None

    @property
    def state(self) -> BridgeState:
        with self._lock:
            return self._state

    def issue_token(self) -> str:
        with self._lock:
            if self._state is not BridgeState.IDLE:
                raise SessionError("A session token has already been issued.")
            self._token = secrets.token_urlsafe(32)
            self._state = BridgeState.ACTIVE
            return self._token

    def authorize(self, token: str) -> None:
        with self._lock:
            if self._state in {
                BridgeState.STOPPED_FAIL_CLOSED,
                BridgeState.EMERGENCY_STOPPED,
            }:
                reason = self._stop_reason or "unspecified"
                raise SessionStopped(f"Bridge session stopped: {reason}")
            if self._token is None or not hmac.compare_digest(self._token, token):
                raise SessionAuthorizationError("Invalid bridge session token.")

    def request_save(self, token: str) -> None:
        with self._lock:
            self.authorize(token)
            if self._state is not BridgeState.ACTIVE:
                raise SessionError("Save confirmation is already pending.")
            self._state = BridgeState.AWAITING_SAVE_CONFIRMATION

    def stop(self, reason: str, *, emergency: bool = False) -> None:
        with self._lock:
            self._token = None
            self._stop_reason = reason
            self._state = (
                BridgeState.EMERGENCY_STOPPED
                if emergency
                else BridgeState.STOPPED_FAIL_CLOSED
            )
