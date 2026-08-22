from __future__ import annotations

import hashlib
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from hoofcare.domain.session import (
    AnimalIdentityResolution,
    IdentityStatus,
    Session,
    SessionState,
)


class LocalSessionStore:
    SNAPSHOT_SCHEMA_VERSION = 1
    AMENDMENT_SCHEMA_VERSION = 1

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._amendment_lock = threading.Lock()

    def save(self, session: Session) -> None:
        target = self._snapshot_path(session.session_id)
        temp = target.with_suffix(target.suffix + ".tmp")
        session_payload = self._serialize_session(session)
        envelope = {
            "schema_version": self.SNAPSHOT_SCHEMA_VERSION,
            "session": session_payload,
            "integrity": {
                "algorithm": "sha256",
                "digest": self._digest(session_payload),
            },
        }
        serialized = json.dumps(envelope, ensure_ascii=False, sort_keys=True)
        with temp.open("w", encoding="utf-8") as handle:
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, target)
        self._fsync_directory()

    def load(self, session_id: str) -> Session:
        path = self._snapshot_path(session_id)
        if not path.is_file():
            raise KeyError(session_id)
        try:
            envelope = json.loads(path.read_text(encoding="utf-8"))
            if envelope["schema_version"] != self.SNAPSHOT_SCHEMA_VERSION:
                raise ValueError("unsupported snapshot schema version")
            integrity = envelope["integrity"]
            if integrity["algorithm"] != "sha256":
                raise ValueError("unsupported snapshot integrity algorithm")
            session_payload = envelope["session"]
            if integrity["digest"] != self._digest(session_payload):
                raise ValueError("snapshot integrity mismatch")
            return self._deserialize_session(session_payload)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid persisted session: {session_id}") from exc

    def append_amendment(
        self,
        session_id: str,
        kind: str,
        payload: dict[str, Any],
        *,
        actor_id: str | None = None,
        source: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        self._validate_session_id(session_id)
        if not actor_id or not source:
            raise ValueError("audit provenance requires actor_id and source")
        if not isinstance(context, dict):
            raise ValueError("audit provenance context must be a mapping")
        path = self._amendment_path(session_id)
        with self._amendment_lock:
            existing = self.read_amendments(session_id)
            core_record = {
                "schema_version": self.AMENDMENT_SCHEMA_VERSION,
                "record_id": str(uuid4()),
                "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "sequence": len(existing) + 1,
                "kind": kind,
                "payload": payload,
                "actor_id": actor_id,
                "source": source,
                "context": context,
            }
            record = {
                **core_record,
                "integrity": {
                    "algorithm": "sha256",
                    "digest": self._digest(core_record),
                },
            }
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._fsync_directory()

    def read_amendments(self, session_id: str) -> list[dict[str, Any]]:
        path = self._amendment_path(session_id)
        if not path.exists():
            return []
        records: list[dict[str, Any]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                if record["schema_version"] != self.AMENDMENT_SCHEMA_VERSION:
                    raise ValueError("unsupported amendment schema version")
                integrity = record["integrity"]
                if integrity["algorithm"] != "sha256":
                    raise ValueError("unsupported amendment integrity algorithm")
                core_record = {key: value for key, value in record.items() if key != "integrity"}
                if integrity["digest"] != self._digest(core_record):
                    raise ValueError("amendment integrity mismatch")
            except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"invalid amendment log: {session_id}") from exc
            records.append(record)
        return records

    @staticmethod
    def _validate_session_id(session_id: str) -> str:
        if not isinstance(session_id, str):
            raise ValueError("invalid session_id")
        if not session_id or session_id in {".", ".."}:
            raise ValueError("invalid session_id")
        if "/" in session_id or "\\" in session_id:
            raise ValueError("invalid session_id")
        if Path(session_id).name != session_id:
            raise ValueError("invalid session_id")
        return session_id

    def _snapshot_path(self, session_id: str) -> Path:
        safe_id = self._validate_session_id(session_id)
        return self.root / f"{safe_id}.json"

    def _amendment_path(self, session_id: str) -> Path:
        safe_id = self._validate_session_id(session_id)
        return self.root / f"{safe_id}.amendments.jsonl"

    @staticmethod
    def _digest(payload: dict[str, Any]) -> str:
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def _fsync_directory(self) -> None:
        if not hasattr(os, "O_DIRECTORY"):
            return
        descriptor = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    @staticmethod
    def _serialize_session(session: Session) -> dict[str, Any]:
        return {
            "session_id": session.session_id,
            "state": session.state.value,
            "identity": {
                "status": session.identity.status.value,
                "animal_id": session.identity.animal_id,
                "candidates": list(session.identity.candidates),
            },
            "animal_id": session.animal_id,
            "applied_event_ids": list(session.applied_event_ids),
            "treatment_refs": list(session.treatment_refs),
            "material_refs": list(session.material_refs),
            "media_refs": list(session.media_refs),
        }

    @staticmethod
    def _deserialize_session(payload: dict[str, Any]) -> Session:
        identity_payload = payload["identity"]
        identity = AnimalIdentityResolution(
            status=IdentityStatus(identity_payload["status"]),
            animal_id=identity_payload.get("animal_id"),
            candidates=tuple(identity_payload.get("candidates", ())),
        )
        return Session(
            session_id=str(payload["session_id"]),
            state=SessionState(payload["state"]),
            identity=identity,
            animal_id=payload.get("animal_id"),
            applied_event_ids=tuple(payload.get("applied_event_ids", ())),
            treatment_refs=tuple(payload.get("treatment_refs", ())),
            material_refs=tuple(payload.get("material_refs", ())),
            media_refs=tuple(payload.get("media_refs", ())),
        )
