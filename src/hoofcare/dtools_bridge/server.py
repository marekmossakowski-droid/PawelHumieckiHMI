from __future__ import annotations

from dataclasses import asdict
from enum import StrEnum
from typing import Any

from mcp.server import MCPServer

from .controller import BridgeController
from .model import ActionKind, ActionRequest
from .session import SessionError


class ControlId(StrEnum):
    BITMAP_COMPONENT = "bitmap_component"
    EDIT_GRAPHICS = "edit_graphics"
    IMPORT_GRAPHICS = "import_graphics"


class MenuPath(StrEnum):
    BITMAP_COMPONENT = "components.graph_and_animation.bitmap"
    LOAD_IMAGE = "draw.load_image"


class TextControlId(StrEnum):
    NEW_GRAPHICS_NAME = "new_graphics_name"


class ShortcutId(StrEnum):
    ESCAPE = "escape"


class StepId(StrEnum):
    OPEN_BITMAP_COMPONENT = "open_bitmap_component"
    OPEN_BITMAP_EDITOR = "open_bitmap_editor"
    LOAD_G1_00_BITMAP = "load_g1_00_bitmap"
    VERIFY_BITMAP_LOADED = "verify_bitmap_loaded"
    DENIED_DOWNLOAD_PROJECT = "download_project"


def create_server(
    controller: BridgeController, *, read_only: bool = False
) -> MCPServer:
    server = MCPServer(
        name="hoofcare-kinco-dtools-bridge",
        title="HoofCare Kinco DTools Bridge",
        description="Bounded synthetic/test-only GL100E UI automation bridge.",
        version="0.1.0",
        instructions=(
            "Use only named tools for the synthetic HoofCare_GL100E_G1 project. "
            "No PLC, KVK, device, transfer, upload or download actions exist."
        ),
    )
    session_token = controller.session.issue_token()

    def execute(request: ActionRequest) -> dict[str, Any]:
        try:
            return asdict(controller.execute(session_token, request))
        except SessionError:
            return {
                "code": "SESSION_STOPPED",
                "message": "The local bridge session is not authorized or is stopped.",
                "postcondition": None,
                "evidence_before": None,
                "evidence_after": None,
            }

    @server.tool(
        name="dtools_status",
        description="Return bounded session and active DTools status.",
        structured_output=True,
    )
    def dtools_status() -> dict[str, Any]:
        payload = execute(ActionRequest(ActionKind.INSPECT, "inspect"))
        payload["bridge_state"] = controller.session.state.value
        return payload

    @server.tool(
        name="dtools_inspect",
        description="Inspect the allowlisted DTools context without mutation.",
        structured_output=True,
    )
    def dtools_inspect() -> dict[str, Any]:
        return execute(ActionRequest(ActionKind.INSPECT, "inspect"))

    @server.tool(
        name="dtools_capture",
        description="Capture only the identified DTools window.",
        structured_output=True,
    )
    def dtools_capture() -> dict[str, Any]:
        return execute(ActionRequest(ActionKind.CAPTURE, "capture"))

    if read_only:
        return server

    @server.tool(
        name="dtools_activate",
        description="Activate one allowlisted named control.",
        structured_output=True,
    )
    def dtools_activate(control_id: ControlId) -> dict[str, Any]:
        return execute(ActionRequest(ActionKind.ACTIVATE, control_id.value))

    @server.tool(
        name="dtools_open_menu",
        description="Open one allowlisted named menu path.",
        structured_output=True,
    )
    def dtools_open_menu(menu_path: MenuPath) -> dict[str, Any]:
        return execute(ActionRequest(ActionKind.OPEN_MENU, menu_path.value))

    @server.tool(
        name="dtools_set_text",
        description="Set text only in the allowlisted graphics-name field.",
        structured_output=True,
    )
    def dtools_set_text(
        control_id: TextControlId, value: str
    ) -> dict[str, Any]:
        return execute(
            ActionRequest(ActionKind.SET_TEXT, control_id.value, value=value)
        )

    @server.tool(
        name="dtools_send_shortcut",
        description="Send one fixed allowlisted shortcut identifier.",
        structured_output=True,
    )
    def dtools_send_shortcut(shortcut_id: ShortcutId) -> dict[str, Any]:
        return execute(
            ActionRequest(ActionKind.SEND_SHORTCUT, shortcut_id.value)
        )

    @server.tool(
        name="dtools_run_step",
        description="Run one named bounded step with literal postcondition.",
        structured_output=True,
    )
    def dtools_run_step(step: StepId) -> dict[str, Any]:
        return execute(ActionRequest(ActionKind.RUN_STEP, step.value))

    @server.tool(
        name="dtools_request_save",
        description="Enter the local save-confirmation gate; never saves by itself.",
        structured_output=True,
    )
    def dtools_request_save() -> dict[str, Any]:
        return execute(ActionRequest(ActionKind.REQUEST_SAVE, "request_save"))

    @server.tool(
        name="dtools_emergency_stop",
        description="Immediately stop the bridge and invalidate its session.",
        structured_output=True,
    )
    def dtools_emergency_stop() -> dict[str, Any]:
        return execute(
            ActionRequest(ActionKind.EMERGENCY_STOP, "emergency_stop")
        )

    return server
