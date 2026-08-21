from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from hoofcare.domain.session import (
    AnimalIdentityResolution,
    IdentityStatus,
    Session,
    SessionState,
)


class LocalSessionStore:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, session: Session) -> None:
        target = self._snapshot_path(session.session_id)
        temp = target.with_suffix(target.suffix + ".tmp")
        payload = self._serialize_session(session)
        temp.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        os.replace(temp, target)

    def load(self, session_id: str) -> Session:
        path = self._snapshot_path(session_id)
        if not path.is_file():
            raise KeyError(session_id)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            return self._deserialize_session(payload)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid persisted session: {session_id}") from exc

    def append_amendment(self, session_id: str, kind: str, payload: dict[str, Any]) -> None:
        path = self._amendment_path(session_id)
        existing = self.read_amendments(session_id)
        record = {
            "sequence": len(existing) + 1,
            "kind": kind,
            "payload": payload,
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
            handle.write("\n")

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
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid amendment log: {session_id}") from exc
            records.append(record)
        return records

    def _snapshot_path(self, session_id: str) -> Path:
        return self.root / f"{session_id}.json"

    def _amendment_path(self, session_id: str) -> Path:
        return self.root / f"{session_id}.amendments.jsonl"

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
