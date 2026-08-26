from pathlib import Path
import tempfile
import unittest

from mcp import Client

from hoofcare.dtools_bridge.audit import AuditLog
from hoofcare.dtools_bridge.controller import BridgeController
from hoofcare.dtools_bridge.deferred_backend import DeferredDToolsBackend
from hoofcare.dtools_bridge.diagnostics import DToolsDiagnosticCollector
from hoofcare.dtools_bridge.model import WindowSnapshot
from hoofcare.dtools_bridge.policy import ActionPolicy
from hoofcare.dtools_bridge.server import create_server
from hoofcare.dtools_bridge.session import SessionGuard


class ServerBackend:
    def __init__(self):
        self.context = "bitmap_component_dialog_open"

    def snapshot(self):
        return WindowSnapshot(
            pid=4242,
            process_name="KincoDToolsSynthetic.exe",
            executable_sha256="a" * 64,
            window_class="Afx:00400000",
            title="HoofCare_GL100E_G1 - [HMI0.whe]",
            project_name="HoofCare_GL100E_G1",
            active_dialog=None,
            context=self.context,
        )

    def capture(self):
        return b"synthetic-png"

    def diagnostic_texts(self):
        return ("Ready", "Info 62", "warning 0", "Error 0")

    def perform_named_step(self, name):
        outcomes = {
            "open_bitmap_component": "bitmap_component_dialog_open",
            "open_bitmap_editor": "bitmap_editor_open",
            "load_g1_00_bitmap": "g1_00_bitmap_visible",
            "verify_bitmap_loaded": "g1_00_bitmap_visible",
            "compile_offline": "main_editor",
        }
        self.context = outcomes[name]

    def activate(self, control_id):
        return None

    def set_text(self, control_id, value):
        return None

    def send_shortcut(self, shortcut_id):
        return None


class DToolsBridgeServerTests(unittest.IsolatedAsyncioTestCase):
    def make_controller(self, backend=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return BridgeController(
            backend=backend or ServerBackend(),
            policy=ActionPolicy.from_file(
                Path("dtools/gl100e/bridge/allowlist.json")
            ),
            session=SessionGuard(),
            audit=AuditLog(Path(temporary.name), session_id="server-test"),
        )

    def make_server(self, *, read_only=False, controller=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        project = root / "HoofCare_GL100E_G1"
        project.mkdir()
        (project / "HoofCare_GL100E_G1.dpj").write_bytes(b"synthetic")
        diagnostics = DToolsDiagnosticCollector(
            project_directory=project,
            output_directory=root / "handoff",
        )
        return create_server(
            controller or self.make_controller(),
            read_only=read_only,
            diagnostics=diagnostics,
        )

    async def test_status_reports_unavailable_deferred_window_without_stopping_session(self):
        def connect():
            raise RuntimeError("DTOOLS_NOT_FOUND")

        controller = self.make_controller(DeferredDToolsBackend(connect))
        server = self.make_server(read_only=True, controller=controller)

        async with Client(server) as client:
            result = await client.call_tool("dtools_status", {})

        self.assertEqual(
            result.structured_content,
            {
                "available": False,
                "code": "DTOOLS_NOT_FOUND",
                "mechanism": "DEFERRED_WINDOWS_CONNECTION",
                "bridge_state": "active",
            },
        )
        self.assertEqual(controller.session.state.value, "active")

    async def test_catalog_is_exact_and_contains_no_generic_executor(self):
        server = self.make_server()

        async with Client(server) as client:
            catalog = await client.list_tools()
            names = {tool.name for tool in catalog.tools}

        self.assertEqual(
            names,
            {
                "dtools_status",
                "dtools_inspect",
                "dtools_capture",
                "dtools_diagnose",
                "dtools_compile_offline",
                "dtools_activate",
                "dtools_open_menu",
                "dtools_set_text",
                "dtools_send_shortcut",
                "dtools_run_step",
                "dtools_request_save",
                "dtools_emergency_stop",
            },
        )
        self.assertTrue(
            names.isdisjoint({"execute", "shell", "click", "keypress"})
        )

    async def test_offline_compile_is_parameterless_named_operation(self):
        controller = self.make_controller()
        controller.backend.context = "main_editor"
        server = self.make_server(controller=controller)

        async with Client(server) as client:
            result = await client.call_tool("dtools_compile_offline", {})

        self.assertEqual(result.structured_content["code"], "OK")
        self.assertEqual(
            result.structured_content["postcondition"], "main_editor"
        )

    async def test_read_only_catalog_exposes_only_approved_trial_tools(self):
        server = self.make_server(read_only=True)

        async with Client(server) as client:
            catalog = await client.list_tools()
            names = {tool.name for tool in catalog.tools}

        self.assertEqual(
            names,
            {
                "dtools_status",
                "dtools_inspect",
                "dtools_capture",
                "dtools_diagnose",
            },
        )

    async def test_diagnose_returns_ai_programmer_handoff_without_mutation(self):
        server = self.make_server(read_only=True)

        async with Client(server) as client:
            result = await client.call_tool("dtools_diagnose", {})

        self.assertEqual(result.structured_content["result"], "BLOCKED")
        self.assertEqual(
            result.structured_content["blocked_stage"],
            "native_compile_evidence",
        )

    async def test_download_step_returns_permanent_denial(self):
        server = self.make_server()

        async with Client(server) as client:
            result = await client.call_tool(
                "dtools_run_step", {"step": "download_project"}
            )

        self.assertEqual(
            result.structured_content["code"], "DENIED_PERMANENT_BOUNDARY"
        )

    async def test_mutating_schemas_expose_no_coordinates_or_raw_keys(self):
        server = self.make_server()

        async with Client(server) as client:
            catalog = await client.list_tools()

        schemas = " ".join(
            str(tool.input_schema).casefold() for tool in catalog.tools
        )
        self.assertNotIn("coordinate", schemas)
        self.assertNotIn("keypress", schemas)
        self.assertNotIn("executable_path", schemas)


if __name__ == "__main__":
    unittest.main()
