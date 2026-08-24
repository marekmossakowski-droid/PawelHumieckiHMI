from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from hoofcare.hmi.gen1.navigation import (
    Gen1Route,
    NavigationContext,
    RouteDecisionKind,
    next_route,
)
from hoofcare.physical.gen1_layout import Gl100eProfile


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "dtools" / "gl100e" / "manifest.json"
_DIRECTIONS = {"READ", "COMMAND_REQUEST"}
_VALUE_TYPES = {"BOOL", "INTEGER", "DECIMAL", "STRING", "ENUM", "EVENT", "DATE", "DATETIME"}
_FORBIDDEN = {"KVK", "PLC", "HYDRAULIC", "RFID_LIVE", "CAMERA_LIVE"}
_VISUAL_SYSTEM = {
    "id": "UX-HC-002-A1/G1-LIGHT-A",
    "source_blob": "8bf33ec97cd98d015545cd2720d39765510a6b9d",
    "font_family": "Arial",
    "minimum_text_px": 18,
    "color_tokens": {
        "surface.canvas": "#F2F4F7",
        "surface.card": "#FFFFFF",
        "surface.selected": "#E8F1FF",
        "text.primary": "#17212B",
        "text.secondary": "#5F6B7A",
        "action.primary": "#1477FF",
        "action.disabled": "#C7CDD5",
        "status.success": "#168A5B",
        "status.warning": "#A85F00",
        "status.blocked": "#C9363E",
        "assist.teal": "#168F84",
        "assist.violet": "#665CF6",
        "border.subtle": "#D8DEE6",
    },
}


def _text(value: object, message: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(message)
    return value.strip()


def _geometry(value: object) -> tuple[int, int, int, int]:
    if not isinstance(value, dict):
        raise ValueError("widget geometry is required")
    coordinates = tuple(value.get(key) for key in ("x", "y", "width", "height"))
    if any(type(item) is not int for item in coordinates):
        raise ValueError("widget geometry must use integer pixels")
    x, y, width, height = coordinates
    if x < 0 or y < 0 or width <= 0 or height <= 0 or x + width > 1024 or y + height > 600:
        raise ValueError("widget geometry is outside 1024x600")
    return x, y, width, height


def _validate_binding(binding: object, route: Gen1Route) -> None:
    if not isinstance(binding, dict):
        raise ValueError("typed binding is required")
    binding_id = _text(binding.get("binding_id"), "binding ID is required")
    value_type = _text(binding.get("value_type"), "typed binding is required")
    if value_type not in _VALUE_TYPES:
        raise ValueError("typed binding has an unsupported value type")
    direction = _text(binding.get("direction"), "binding direction is required")
    if direction not in _DIRECTIONS:
        raise ValueError("binding direction is not allowed")
    _text(binding.get("available_when"), "binding availability is required")
    _text(binding.get("missing_data"), "binding missing-data behavior is required")

    binding_text = json.dumps(binding, ensure_ascii=False).upper()
    if any(token in binding_text for token in _FORBIDDEN):
        raise ValueError("forbidden binding")

    if direction == "COMMAND_REQUEST":
        use_case_id = _text(binding.get("use_case_id"), "approved local use case is required")
        if not use_case_id.startswith("navigation."):
            raise ValueError("approved local use case is required")
        action = use_case_id.removeprefix("navigation.")
        decision = next_route(NavigationContext(route, owner_session_active=True), action)
        if decision.kind is RouteDecisionKind.RECOVERY_REQUIRED:
            raise ValueError("approved local use case is required")
        if binding_id != f"action.{action}":
            raise ValueError("command binding must match its approved local use case")
    elif "use_case_id" in binding:
        raise ValueError("read binding cannot claim an approved local use case")


def _validate_native_artifact(value: object) -> None:
    if not isinstance(value, dict):
        raise ValueError("native artifact evidence is required")
    status = value.get("status")
    evidence_fields = ("artifact_path", "dtools_version", "sha256", "built_at_utc", "compile_log_path")
    if status == "NATIVE_DTOOLS_ARTIFACT_REQUIRED":
        if any(value.get(field) is not None for field in evidence_fields):
            raise ValueError("blocked native artifact cannot claim evidence")
        return
    if status != "OFFLINE_COMPILE_VERIFIED":
        raise ValueError("native artifact status is invalid")
    evidence = {field: _text(value.get(field), f"native artifact {field} is required") for field in evidence_fields}
    artifact = ROOT / evidence["artifact_path"]
    compile_log = ROOT / evidence["compile_log_path"]
    if not artifact.is_file() or not compile_log.is_file():
        raise ValueError("native artifact evidence files are missing")
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    if digest != evidence["sha256"]:
        raise ValueError("native artifact SHA-256 mismatch")


def validate_manifest(data: object) -> None:
    if not isinstance(data, dict):
        raise ValueError("manifest must be a JSON object")
    if data.get("schema_version") != 1:
        raise ValueError("unsupported manifest schema")
    if data.get("profile_id") != "gl100e-landscape-v1":
        raise ValueError("unexpected GL100E profile")
    if data.get("canvas") != {"width": 1024, "height": 600}:
        raise ValueError("manifest canvas must be 1024x600")
    if data.get("visual_system") != _VISUAL_SYSTEM:
        raise ValueError("visual system differs from baselined G1-LIGHT-A")

    screens = data.get("screens")
    if not isinstance(screens, list):
        raise ValueError("manifest screens must be a list")
    screen_ids = [screen.get("screen_id") for screen in screens if isinstance(screen, dict)]
    if len(screen_ids) != len(screens) or len(screen_ids) != len(set(screen_ids)):
        raise ValueError("duplicate screen ID")

    known_routes = {route.value for route in Gen1Route}
    supplied_routes = {screen.get("route_id") for screen in screens}
    unknown_routes = supplied_routes - known_routes
    if unknown_routes:
        raise ValueError("unknown route")
    if supplied_routes != known_routes or len(screens) != len(known_routes):
        raise ValueError("manifest route coverage is incomplete")

    profile = Gl100eProfile.default()
    profile_screens = {screen.route.value: screen for screen in profile.screens}
    for screen in screens:
        route = Gen1Route(screen["route_id"])
        _text(screen.get("label_pl"), "Polish label is required")
        widgets = screen.get("widgets")
        if not isinstance(widgets, list) or not widgets:
            raise ValueError("screen widgets are required")
        primary = [widget for widget in widgets if widget.get("primary_action") is True]
        if len(primary) > 4:
            raise ValueError("more than four primary actions")
        widget_ids = [widget.get("widget_id") for widget in widgets if isinstance(widget, dict)]
        if len(widget_ids) != len(widgets) or len(widget_ids) != len(set(widget_ids)):
            raise ValueError("duplicate widget ID")

        target_by_action = {target.action_id: target for target in profile_screens[route.value].targets}
        manifest_actions: set[str] = set()
        for widget in widgets:
            _text(widget.get("widget_id"), "widget ID is required")
            _text(widget.get("label_pl"), "Polish label is required")
            x, y, width, height = _geometry(widget.get("geometry"))
            _validate_binding(widget.get("binding"), route)
            if widget.get("primary_action") is True:
                binding = widget["binding"]
                if binding["direction"] != "COMMAND_REQUEST":
                    raise ValueError("primary action must be a command request")
                action = binding["use_case_id"].removeprefix("navigation.")
                manifest_actions.add(action)
                target = target_by_action.get(action)
                if target is None or (x, y, width, height) != (
                    target.x,
                    target.y,
                    target.width,
                    target.height,
                ):
                    raise ValueError("manifest action geometry differs from GL100E profile")
                if width < 64 or height < 64:
                    raise ValueError("primary target is smaller than 64x64")
        if manifest_actions != set(target_by_action):
            raise ValueError("manifest actions differ from GL100E profile")

    _validate_native_artifact(data.get("native_artifact"))


def main() -> int:
    try:
        data = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        validate_manifest(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"GL100E DTools manifest validation failed: {exc}", file=sys.stderr)
        return 1
    print("GL100E DTools manifest validated; native artifact status is truthful")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
