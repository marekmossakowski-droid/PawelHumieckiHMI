from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


LOCKOUT_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=5)
SESSION_TIMEOUT = timedelta(minutes=10)


def _require_aware(moment: datetime) -> None:
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise ValueError("now must be timezone-aware")


def _is_ascii_pin(pin: str) -> bool:
    return len(pin) == 6 and pin.isascii() and pin.isdigit()


@dataclass(frozen=True)
class OwnerGateState:
    secret_pin: str
    failed_attempts: int = 0
    locked_until: datetime | None = None

    def __post_init__(self) -> None:
        if not _is_ascii_pin(self.secret_pin):
            raise ValueError("secret_pin must contain exactly six ASCII digits")
        if self.failed_attempts < 0:
            raise ValueError("failed_attempts cannot be negative")
        if self.locked_until is not None:
            _require_aware(self.locked_until)


@dataclass(frozen=True)
class OwnerSession:
    authorized: bool
    gate_state: OwnerGateState
    last_activity_at: datetime | None = None
    expires_at: datetime | None = None
    reason: str | None = None

    def is_active(self, now: datetime) -> bool:
        _require_aware(now)
        return bool(self.authorized and self.expires_at is not None and now < self.expires_at)

    def touch(self, now: datetime) -> "OwnerSession":
        _require_aware(now)
        if not self.is_active(now):
            return OwnerSession(False, self.gate_state, reason="OWNER_SESSION_EXPIRED")
        return OwnerSession(True, self.gate_state, now, now + SESSION_TIMEOUT)


def unlock_owner_zone(pin: str, now: datetime, state: OwnerGateState) -> OwnerSession:
    _require_aware(now)

    if state.locked_until is not None and now < state.locked_until:
        return OwnerSession(False, state, reason="OWNER_GATE_LOCKED")

    if state.locked_until is not None:
        state = OwnerGateState(secret_pin=state.secret_pin)

    if pin == state.secret_pin:
        reset_state = OwnerGateState(secret_pin=state.secret_pin)
        return OwnerSession(True, reset_state, now, now + SESSION_TIMEOUT)

    failed_attempts = state.failed_attempts + 1
    locked_until = now + LOCKOUT_DURATION if failed_attempts >= LOCKOUT_ATTEMPTS else None
    next_state = OwnerGateState(
        secret_pin=state.secret_pin,
        failed_attempts=failed_attempts,
        locked_until=locked_until,
    )
    if locked_until is not None:
        reason = "OWNER_GATE_LOCKED"
    elif not _is_ascii_pin(pin):
        reason = "INVALID_PIN_FORMAT"
    else:
        reason = "INVALID_PIN"
    return OwnerSession(False, next_state, reason=reason)
