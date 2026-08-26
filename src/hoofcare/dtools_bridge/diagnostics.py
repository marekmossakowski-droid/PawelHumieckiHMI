from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Iterable

from .model import WindowSnapshot


_PROJECT_SUFFIXES = frozenset(
    {".bg", ".dpj", ".pkg", ".pkgx", ".png", ".whe"}
)
_MESSAGE_COUNT = re.compile(
    r"\b(info|warning|error)\s*[:=]?\s*(\d+)\b", re.IGNORECASE
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class DToolsDiagnosticCollector:
    """Create a bounded, read-only handoff for compilation diagnosis."""

    def __init__(self, *, project_directory: Path, output_directory: Path) -> None:
        self.project_directory = Path(project_directory).resolve(strict=True)
        if not self.project_directory.is_dir():
            raise ValueError("PROJECT_DIRECTORY_REQUIRED")
        self.output_directory = Path(output_directory)

    def collect(
        self,
        *,
        snapshot: WindowSnapshot,
        visible_texts: Iterable[str],
    ) -> dict[str, object]:
        inventory = self._inventory()
        counts = self._message_counts(visible_texts)
        result, blocked_stage, reason = self._classify(
            snapshot=snapshot,
            inventory=inventory,
            counts=counts,
        )
        report: dict[str, object] = {
            "schema_version": 1,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "mode": "READ_ONLY_DIAGNOSTIC",
            "result": result,
            "blocked_stage": blocked_stage,
            "reason": reason,
            "project_name": snapshot.project_name,
            "window": {
                "pid": snapshot.pid,
                "process_name": snapshot.process_name,
                "executable_sha256": snapshot.executable_sha256,
                "window_class": snapshot.window_class,
                "title": snapshot.title,
                "active_dialog": snapshot.active_dialog,
                "context": snapshot.context,
            },
            "message_counts": counts,
            "project_inventory": inventory,
            "safety_boundary": {
                "project_mutated": False,
                "compile_triggered": False,
                "panel_upload_triggered": False,
                "device_io_used": False,
            },
            "next_action": self._next_action(reason),
        }
        self.output_directory.mkdir(parents=True, exist_ok=True)
        handoff = self.output_directory / "ai-programmer-dtools-handoff.json"
        temporary = handoff.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        temporary.replace(handoff)
        report["handoff_path"] = str(handoff)
        return report

    def _inventory(self) -> list[dict[str, object]]:
        files = sorted(
            (
                path
                for path in self.project_directory.rglob("*")
                if path.is_file() and path.suffix.casefold() in _PROJECT_SUFFIXES
            ),
            key=lambda path: path.relative_to(self.project_directory).as_posix(),
        )
        return [
            {
                "relative_path": path.relative_to(self.project_directory).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": _sha256(path),
            }
            for path in files
        ]

    @staticmethod
    def _message_counts(visible_texts: Iterable[str]) -> dict[str, int | None]:
        counts: dict[str, int | None] = {
            "info": None,
            "warning": None,
            "error": None,
        }
        for text in visible_texts:
            for match in _MESSAGE_COUNT.finditer(str(text)):
                counts[match.group(1).casefold()] = int(match.group(2))
        return counts

    @staticmethod
    def _classify(
        *,
        snapshot: WindowSnapshot,
        inventory: list[dict[str, object]],
        counts: dict[str, int | None],
    ) -> tuple[str, str | None, str]:
        if snapshot.context.startswith("unknown_dialog:"):
            return "BLOCKED", "ui_context", "UNEXPECTED_DIALOG"
        native_projects = [
            item for item in inventory if str(item["relative_path"]).casefold().endswith(".dpj")
        ]
        if len(native_projects) != 1:
            return "BLOCKED", "native_project", "NATIVE_PROJECT_COUNT_INVALID"
        if counts["error"] is not None and counts["error"] > 0:
            return "FAIL", "dtools_build_messages", "DTOOLS_REPORTED_ERRORS"
        native_packages = [
            item
            for item in inventory
            if Path(str(item["relative_path"])).suffix.casefold()
            in {".pkg", ".pkgx"}
        ]
        if len(native_packages) == 1 and counts["error"] == 0:
            return "BLOCKED", "compile_provenance", "COMPILE_RUN_NOT_BOUND"
        return "BLOCKED", "native_compile_evidence", "COMPILE_OUTPUT_NOT_FOUND"

    @staticmethod
    def _next_action(reason: str) -> str:
        return {
            "UNEXPECTED_DIALOG": "Close or classify the dialog, then run diagnostics again.",
            "NATIVE_PROJECT_COUNT_INVALID": "Provide exactly one native .dpj project in the selected test directory.",
            "DTOOLS_REPORTED_ERRORS": "Capture the DTools message pane and analyze the reported errors before any retry.",
            "COMPILE_OUTPUT_NOT_FOUND": "Run a separately authorized offline DTools compile and attach its native output and complete log.",
            "COMPILE_RUN_NOT_BOUND": "Run the named offline compile operation so the package, messages and timestamps can be bound to one execution.",
        }[reason]
