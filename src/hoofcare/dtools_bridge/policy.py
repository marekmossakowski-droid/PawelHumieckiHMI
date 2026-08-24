from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any

from .model import ActionRequest, PolicyDecision, WindowSnapshot


_PERMANENTLY_FORBIDDEN = re.compile(
    r"(?:^|[^a-z0-9])"
    r"(?:download|upload|transfer|deployment|deploy|plc|kvk|ethernet|usb|"
    r"device|com[0-9]*)"
    r"(?:$|[^a-z0-9])",
    re.IGNORECASE,
)


class ActionPolicy:
    def __init__(self, config: dict[str, Any]):
        self._project_name = str(config["project_name"])
        self._executable_sha256 = str(config["executable_sha256"]).lower()
        self._allowed = {
            str(kind): frozenset(str(target) for target in targets)
            for kind, targets in dict(config["allowed_targets"]).items()
        }
        self._postconditions = {
            str(target): str(postcondition)
            for target, postcondition in dict(
                config.get("postconditions", {})
            ).items()
        }
        self._preconditions = {
            str(target): str(precondition)
            for target, precondition in dict(
                config.get("preconditions", {})
            ).items()
        }
        canonical = json.dumps(config, sort_keys=True, separators=(",", ":"))
        self.config_sha256 = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @classmethod
    def from_file(
        cls,
        path: Path,
        *,
        executable_sha256: str | None = None,
        project_name: str | None = None,
    ) -> "ActionPolicy":
        config = json.loads(path.read_text(encoding="utf-8"))
        if executable_sha256 is not None:
            config["executable_sha256"] = executable_sha256
        if project_name is not None:
            config["project_name"] = project_name
        return cls(config)

    def evaluate(
        self, request: ActionRequest, snapshot: WindowSnapshot
    ) -> PolicyDecision:
        if snapshot.executable_sha256.lower() != self._executable_sha256:
            return PolicyDecision(
                False,
                "EXECUTABLE_MISMATCH",
                "Executable SHA-256 does not match the approved session target.",
            )
        if snapshot.project_name != self._project_name:
            return PolicyDecision(
                False,
                "PROJECT_MISMATCH",
                "The active DTools project is not the approved synthetic project.",
            )
        if snapshot.context.startswith("unknown_dialog:"):
            return PolicyDecision(
                False,
                "UNEXPECTED_DIALOG",
                "An unknown dialog is active; the session must stop fail-closed.",
            )
        if _PERMANENTLY_FORBIDDEN.search(request.target):
            return PolicyDecision(
                False,
                "DENIED_PERMANENT_BOUNDARY",
                "The requested target belongs to a permanent device boundary.",
            )
        expected_precondition = self._preconditions.get(request.target)
        if (
            expected_precondition is not None
            and snapshot.context != expected_precondition
        ):
            return PolicyDecision(
                False,
                "PRECONDITION_MISMATCH",
                "The active UI context does not match the named step precondition.",
            )
        allowed_targets = self._allowed.get(request.kind.value)
        if allowed_targets is None:
            return PolicyDecision(
                False,
                "ACTION_KIND_NOT_ALLOWLISTED",
                "The requested action kind is not exposed by this profile.",
            )
        if request.target not in allowed_targets:
            return PolicyDecision(
                False,
                "TARGET_NOT_ALLOWLISTED",
                "The requested named target is not allowlisted.",
            )
        return PolicyDecision(True, "ALLOW", "Exact bounded action allowed.")

    def expected_postcondition(self, target: str) -> str | None:
        return self._postconditions.get(target)
