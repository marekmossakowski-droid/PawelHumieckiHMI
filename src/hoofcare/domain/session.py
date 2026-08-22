from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Any
from uuid import uuid4


class SessionState(str, Enum):
    IDENTITY_PENDING = "IDENTITY_PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    FOLLOW_UP_REQUIRED = "FOLLOW_UP_REQUIRED"
    COMPLETED = "COMPLETED"
    UNRESOLVED = "UNRESOLVED"
    CANCELLED = "CANCELLED"


class IdentityStatus(str, Enum):
    UNRESOLVED = "UNRESOLVED"
    AMBIGUOUS = "AMBIGUOUS"
    CONFIRMED = "CONFIRMED"


@dataclass(frozen=True)
class AnimalIdentityResolution:
    status: IdentityStatus
    animal_id: str | None = None
    candidates: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status is IdentityStatus.CONFIRMED:
            if self.animal_id is None or not self.animal_id.strip():
                raise ValueError("confirmed identity requires a non-empty animal_id")
            if self.candidates:
                raise ValueError("confirmed identity cannot carry candidates")
            return
        if self.animal_id is not None:
            raise ValueError("non-confirmed identity cannot carry animal_id")
        if self.status is IdentityStatus.AMBIGUOUS:
            if len(tuple(dict.fromkeys(self.candidates))) < 2:
                raise ValueError("ambiguous identity requires at least two candidates")
        elif self.candidates:
            raise ValueError("unresolved identity cannot carry candidates")

    @classmethod
    def unresolved(cls) -> "AnimalIdentityResolution":
        return cls(status=IdentityStatus.UNRESOLVED)

    @classmethod
    def ambiguous(cls, candidates: list[str] | tuple[str, ...]) -> "AnimalIdentityResolution":
        normalized = tuple(dict.fromkeys(candidates))
        return cls(status=IdentityStatus.AMBIGUOUS, candidates=normalized)

    @classmethod
    def confirmed(cls, animal_id: str) -> "AnimalIdentityResolution":
        animal_id = animal_id.strip()
        return cls(status=IdentityStatus.CONFIRMED, animal_id=animal_id)


class SessionEventType(str, Enum):
    IDENTITY_RESOLVED = "IDENTITY_RESOLVED"
    COMPLETE = "COMPLETE"
    FOLLOW_UP_REQUIRED = "FOLLOW_UP_REQUIRED"
    CANCEL = "CANCEL"
    MARK_UNRESOLVED = "MARK_UNRESOLVED"


@dataclass(frozen=True)
class SessionEvent:
    event_id: str
    event_type: SessionEventType
    payload: Any = None

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id must be non-empty")


_TERMINAL_STATES = {
    SessionState.COMPLETED,
    SessionState.UNRESOLVED,
    SessionState.CANCELLED,
}


@dataclass(frozen=True)
class Session:
    session_id: str
    state: SessionState
    identity: AnimalIdentityResolution
    animal_id: str | None
    applied_event_ids: tuple[str, ...] = ()
    treatment_refs: tuple[str, ...] = ()
    material_refs: tuple[str, ...] = ()
    media_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.session_id.strip():
            raise ValueError("session_id must be non-empty")
        if self.identity.status is IdentityStatus.CONFIRMED:
            if self.animal_id != self.identity.animal_id:
                raise ValueError("confirmed identity must match session animal_id")
        elif self.animal_id is not None:
            raise ValueError("non-confirmed identity cannot carry session animal_id")
        if self.state in {SessionState.IN_PROGRESS, SessionState.FOLLOW_UP_REQUIRED, SessionState.COMPLETED}:
            if self.identity.status is not IdentityStatus.CONFIRMED or not self.animal_id:
                raise ValueError(f"{self.state.value} requires confirmed identity")

    @classmethod
    def new(cls) -> "Session":
        return cls(
            session_id=str(uuid4()),
            state=SessionState.IDENTITY_PENDING,
            identity=AnimalIdentityResolution.unresolved(),
            animal_id=None,
        )

    def apply(self, event: SessionEvent) -> "Session":
        if event.event_id in self.applied_event_ids:
            return self

        if self.state in _TERMINAL_STATES:
            raise ValueError(f"cannot apply {event.event_type.value} to terminal session")

        if event.event_type is SessionEventType.IDENTITY_RESOLVED:
            return self._apply_identity(event)

        if event.event_type is SessionEventType.COMPLETE:
            self._require_confirmed_identity()
            return self._with_event(event, state=SessionState.COMPLETED)

        if event.event_type is SessionEventType.FOLLOW_UP_REQUIRED:
            self._require_confirmed_identity()
            return self._with_event(event, state=SessionState.FOLLOW_UP_REQUIRED)

        if event.event_type is SessionEventType.CANCEL:
            return self._with_event(event, state=SessionState.CANCELLED)

        if event.event_type is SessionEventType.MARK_UNRESOLVED:
            return self._with_event(event, state=SessionState.UNRESOLVED)

        raise ValueError(f"unsupported event type: {event.event_type}")

    def _apply_identity(self, event: SessionEvent) -> "Session":
        if not isinstance(event.payload, AnimalIdentityResolution):
            raise TypeError("IDENTITY_RESOLVED payload must be AnimalIdentityResolution")

        identity = event.payload
        if identity.status is IdentityStatus.CONFIRMED:
            return self._with_event(
                event,
                identity=identity,
                animal_id=identity.animal_id,
                state=SessionState.IN_PROGRESS,
            )

        return self._with_event(
            event,
            identity=identity,
            animal_id=None,
            state=SessionState.IDENTITY_PENDING,
        )

    def _require_confirmed_identity(self) -> None:
        if self.identity.status is not IdentityStatus.CONFIRMED or not self.animal_id:
            raise ValueError("confirmed animal identity is required")

    def _with_event(self, event: SessionEvent, **changes: Any) -> "Session":
        return replace(
            self,
            applied_event_ids=self.applied_event_ids + (event.event_id,),
            **changes,
        )
