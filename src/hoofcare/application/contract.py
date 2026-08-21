from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from hoofcare.domain.session import AnimalIdentityResolution, Session, SessionEvent, SessionEventType


class ErrorCode(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    INVALID_REQUEST = "INVALID_REQUEST"
    CONFLICT = "CONFLICT"
    DEGRADED = "DEGRADED"


@dataclass(frozen=True)
class ContractError:
    code: ErrorCode
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code.value, "message": self.message}


@dataclass(frozen=True)
class ContractResult:
    ok: bool
    data: dict | None = None
    error: ContractError | None = None

    @classmethod
    def success(cls, data: dict) -> "ContractResult":
        return cls(ok=True, data=data)

    @classmethod
    def failure(cls, code: ErrorCode, message: str) -> "ContractResult":
        return cls(ok=False, error=ContractError(code, message))


class BenchApplicationService:
    """In-process bench contract only. It exposes no KVK actuation capability."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}
        self._request_results: dict[str, ContractResult] = {}

    @classmethod
    def in_memory(cls) -> "BenchApplicationService":
        return cls()

    def create_session(self, *, request_id: str) -> ContractResult:
        cached = self._request_results.get(request_id)
        if cached is not None:
            return cached
        session = Session.new()
        self._sessions[session.session_id] = session
        result = ContractResult.success(self._view(session))
        self._request_results[request_id] = result
        return result

    def get_session(self, session_id: str) -> ContractResult:
        session = self._sessions.get(session_id)
        if session is None:
            return ContractResult.failure(ErrorCode.NOT_FOUND, "session not found")
        return ContractResult.success(self._view(session))

    def resolve_identity(
        self,
        session_id: str,
        *,
        request_id: str,
        confirmed_animal_id: str | None = None,
        candidates: tuple[str, ...] = (),
    ) -> ContractResult:
        cached = self._request_results.get(request_id)
        if cached is not None:
            return cached
        session = self._sessions.get(session_id)
        if session is None:
            return ContractResult.failure(ErrorCode.NOT_FOUND, "session not found")
        if confirmed_animal_id and candidates:
            return ContractResult.failure(ErrorCode.INVALID_REQUEST, "identity request is conflicting")
        try:
            if confirmed_animal_id:
                resolution = AnimalIdentityResolution.confirmed(confirmed_animal_id)
            elif candidates:
                resolution = AnimalIdentityResolution.ambiguous(candidates)
            else:
                return ContractResult.failure(ErrorCode.INVALID_REQUEST, "identity evidence is required")
            updated = session.apply(
                SessionEvent(
                    event_id=request_id,
                    event_type=SessionEventType.IDENTITY_RESOLVED,
                    payload=resolution,
                )
            )
        except (TypeError, ValueError) as exc:
            return ContractResult.failure(ErrorCode.INVALID_REQUEST, str(exc))
        self._sessions[session_id] = updated
        result = ContractResult.success(self._view(updated))
        self._request_results[request_id] = result
        return result

    @staticmethod
    def _view(session: Session) -> dict:
        return {
            "session_id": session.session_id,
            "state": session.state.value,
            "animal_id": session.animal_id,
            "identity_status": session.identity.status.value,
        }
