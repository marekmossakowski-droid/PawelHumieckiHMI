from __future__ import annotations

import argparse
from pathlib import Path
import sys

from hoofcare.dtools_bridge.audit import AuditLog
from hoofcare.dtools_bridge.controller import BridgeController
from hoofcare.dtools_bridge.policy import ActionPolicy
from hoofcare.dtools_bridge.server import create_server
from hoofcare.dtools_bridge.session import SessionGuard
from hoofcare.dtools_bridge.windows_backend import (
    EmergencyHotkey,
    WindowsDToolsBackend,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HoofCare Kinco DTools Bridge")
    parser.add_argument("--project", default="HoofCare_GL100E_G1")
    parser.add_argument("--project-directory", type=Path, required=True)
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--executable-sha256", required=True)
    parser.add_argument("--read-only", action="store_true")
    parser.add_argument(
        "--allowlist",
        type=Path,
        default=Path("dtools/gl100e/bridge/allowlist.json"),
    )
    parser.add_argument("--logs", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    if sys.platform != "win32":
        print("WINDOWS_REQUIRED", file=sys.stderr)
        return 2
    args = build_parser().parse_args(argv)
    project_directory = args.project_directory.resolve(strict=True)
    allowlist_path = args.allowlist.resolve(strict=True)
    executable_path = args.executable.resolve(strict=True)
    logs = args.logs.resolve()
    logs.mkdir(parents=True, exist_ok=True)
    if not project_directory.is_dir():
        print("PROJECT_DIRECTORY_REQUIRED", file=sys.stderr)
        return 2
    if len(args.executable_sha256) != 64:
        print("EXECUTABLE_SHA256_REQUIRED", file=sys.stderr)
        return 2

    session = SessionGuard()
    policy = ActionPolicy.from_file(
        allowlist_path,
        executable_sha256=args.executable_sha256,
        project_name=args.project,
    )
    backend = WindowsDToolsBackend.connect_exact(
        args.project, executable_path, args.executable_sha256
    )
    audit = AuditLog(logs)
    controller = BridgeController(
        backend=backend, policy=policy, session=session, audit=audit
    )
    server = create_server(controller, read_only=args.read_only)
    hotkey = None
    if not args.read_only:
        hotkey = EmergencyHotkey()
        hotkey.start(
            lambda: session.stop("operator_hotkey", emergency=True)
        )
    try:
        server.run(transport="stdio")
    finally:
        if hotkey is not None:
            hotkey.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
