import json
from pathlib import Path
import tempfile
import unittest

from hoofcare.dtools_bridge.diagnostics import DToolsDiagnosticCollector
from hoofcare.dtools_bridge.model import WindowSnapshot


def _snapshot() -> WindowSnapshot:
    return WindowSnapshot(
        pid=4242,
        process_name="Kinco DTools.exe",
        executable_sha256="a" * 64,
        window_class="Afx:00400000",
        title="HoofCare_GL100E_G1 - [HMI0.whe]",
        project_name="HoofCare_GL100E_G1",
        active_dialog=None,
        context="main_editor",
    )


class DToolsDiagnosticCollectorTests(unittest.TestCase):
    def make_project(self, root: Path) -> Path:
        project = root / "HoofCare_GL100E_G1"
        project.mkdir()
        (project / "HoofCare_GL100E_G1.dpj").write_bytes(b"synthetic-dpj")
        (project / "HMI0.whe").write_bytes(b"synthetic-screen")
        return project

    def test_clean_message_counts_do_not_claim_compile_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            collector = DToolsDiagnosticCollector(
                project_directory=self.make_project(root),
                output_directory=root / "handoff",
            )

            report = collector.collect(
                snapshot=_snapshot(),
                visible_texts=("Ready", "Info 62", "warning 0", "Error 0"),
            )

            self.assertEqual(report["result"], "BLOCKED")
            self.assertEqual(report["blocked_stage"], "native_compile_evidence")
            self.assertEqual(report["reason"], "COMPILE_OUTPUT_NOT_FOUND")
            self.assertEqual(report["message_counts"], {"info": 62, "warning": 0, "error": 0})

    def test_error_count_identifies_dtools_message_stage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            collector = DToolsDiagnosticCollector(
                project_directory=self.make_project(root),
                output_directory=root / "handoff",
            )

            report = collector.collect(
                snapshot=_snapshot(),
                visible_texts=("Info 12", "warning 1", "Error 3"),
            )

            self.assertEqual(report["result"], "FAIL")
            self.assertEqual(report["blocked_stage"], "dtools_build_messages")
            self.assertEqual(report["reason"], "DTOOLS_REPORTED_ERRORS")

    def test_unbound_native_package_and_zero_errors_do_not_prove_current_compile(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = self.make_project(root)
            (project / "HoofCare_GL100E_G1.pkgx").write_bytes(
                b"synthetic-compiled-package"
            )
            collector = DToolsDiagnosticCollector(
                project_directory=project,
                output_directory=root / "handoff",
            )

            report = collector.collect(
                snapshot=_snapshot(),
                visible_texts=("Info 62", "Warning 0", "Error 0"),
            )

            self.assertEqual(report["result"], "BLOCKED")
            self.assertEqual(report["blocked_stage"], "compile_provenance")
            self.assertEqual(report["reason"], "COMPILE_RUN_NOT_BOUND")
            package = next(
                item
                for item in report["project_inventory"]
                if item["relative_path"].endswith(".pkgx")
            )
            self.assertEqual(len(package["sha256"]), 64)

    def test_handoff_contains_hashes_not_project_file_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            collector = DToolsDiagnosticCollector(
                project_directory=self.make_project(root),
                output_directory=root / "handoff",
            )

            report = collector.collect(
                snapshot=_snapshot(),
                visible_texts=("Ready",),
            )
            handoff = Path(report["handoff_path"])
            persisted = json.loads(handoff.read_text("utf-8"))
            payload = handoff.read_text("utf-8")

            self.assertEqual(persisted["schema_version"], 1)
            self.assertEqual(
                [item["relative_path"] for item in persisted["project_inventory"]],
                ["HMI0.whe", "HoofCare_GL100E_G1.dpj"],
            )
            self.assertTrue(all(len(item["sha256"]) == 64 for item in persisted["project_inventory"]))
            self.assertNotIn("synthetic-dpj", payload)
            self.assertNotIn("synthetic-screen", payload)

    def test_unknown_dialog_fails_closed_before_compile_assessment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            collector = DToolsDiagnosticCollector(
                project_directory=self.make_project(root),
                output_directory=root / "handoff",
            )
            snapshot = WindowSnapshot(
                **{
                    **_snapshot().__dict__,
                    "active_dialog": "Unexpected Dialog",
                    "context": "unknown_dialog:Unexpected Dialog",
                }
            )

            report = collector.collect(snapshot=snapshot, visible_texts=())

            self.assertEqual(report["result"], "BLOCKED")
            self.assertEqual(report["blocked_stage"], "ui_context")
            self.assertEqual(report["reason"], "UNEXPECTED_DIALOG")


if __name__ == "__main__":
    unittest.main()
