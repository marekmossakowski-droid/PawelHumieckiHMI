from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import threading
import uuid
from typing import Any


_REDACTED = "[REDACTED]"
_SENSITIVE_KEYS = frozenset({"token", "value", "text", "credential", "password"})
_SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9_-]+$")


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): _REDACTED if str(key).casefold() in _SENSITIVE_KEYS else _redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact(item) for item in value]
    if isinstance(value, tuple):
        return [_redact(item) for item in value]
    return value


class AuditLog:
    def __init__(self, directory: Path, *, session_id: str | None = None) -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.evidence_directory = self.directory / "evidence"
        self.evidence_directory.mkdir(exist_ok=True)
        self.path = self.directory / "audit.jsonl"
        self.session_id = session_id or uuid.uuid4().hex
        if not _SAFE_IDENTIFIER.fullmatch(self.session_id):
            raise ValueError("session_id must contain only letters, digits, '_' or '-'.")
        self._lock = threading.Lock()
        self._operation_number = 0

    def append(
        self,
        tool: str,
        arguments: dict[str, Any],
        decision: str,
        result: str,
        *,
        evidence_before_image: bytes | None = None,
        evidence_after_image: bytes | None = None,
        **details: Any,
    ) -> int:
        with self._lock:
            self._operation_number += 1
            operation_number = self._operation_number
            evidence_before = self._write_evidence(
                evidence_before_image, operation_number, "before"
            )
            evidence_after = self._write_evidence(
                evidence_after_image, operation_number, "after"
            )
            record = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "session_id": self.session_id,
                "operation_number": operation_number,
                "tool": tool,
                "arguments": _redact(arguments),
                "decision": decision,
                "result": result,
                "evidence_before": evidence_before,
                "evidence_after": evidence_after,
                **_redact(details),
            }
            payload = json.dumps(
                record, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
            with self.path.open("a", encoding="utf-8", newline="\n") as handle:
                handle.write(payload + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            return operation_number

    def record_evidence(
        self, image: bytes, operation_number: int, phase: str
    ) -> str:
        with self._lock:
            result = self._write_evidence(image, operation_number, phase)
        if result is None:
            raise ValueError("Evidence image is required.")
        return result

    def evidence_filename(self, operation_number: int, phase: str) -> str:
        if phase not in {"before", "after"}:
            raise ValueError("Evidence phase must be 'before' or 'after'.")
        if operation_number < 1:
            raise ValueError("Evidence operation number must be positive.")
        return f"{self.session_id}-{operation_number:06d}-{phase}.png"

    def _write_evidence(
        self, image: bytes | None, operation_number: int, phase: str
    ) -> str | None:
        if image is None:
            return None
        filename = self.evidence_filename(operation_number, phase)
        path = self.evidence_directory / filename
        with path.open("xb") as handle:
            handle.write(image)
            handle.flush()
            os.fsync(handle.fileno())
        return filename
