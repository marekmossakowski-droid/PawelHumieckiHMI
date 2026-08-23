from pathlib import Path
import unittest


class Generation1HmiGuiPackageGovernanceTests(unittest.TestCase):
    def test_generation_1_gui_package_is_complete_and_activation_gated(self):
        surfaces = {
            "decision": Path(
                "docs/decisions/HC-REQ-HC-003-G1-PREPARATION-DECISION-001.md"
            ),
            "requirements": Path(
                "docs/requirements/REQ-HC-003_Generation_1_Complete_HMI_GUI_and_DTools_v0.1.md"
            ),
            "design": Path(
                "docs/design/UX-HC-002_Generation_1_Complete_HMI_GUI_and_DTools_v0.1.md"
            ),
            "plan": Path(
                "docs/superpowers/plans/2026-08-24-generation-1-hmi-gui-dtools.md"
            ),
            "authority": Path(
                "governance/IA-HC-008_Generation_1_HMI_GUI_and_DTools_Authority_v0.1.md"
            ),
        }
        for label, path in surfaces.items():
            self.assertTrue(path.is_file(), f"{label} surface must exist")

        decision = surfaces["decision"].read_text(encoding="utf-8")
        requirements = surfaces["requirements"].read_text(encoding="utf-8")
        design = surfaces["design"].read_text(encoding="utf-8")
        plan = surfaces["plan"].read_text(encoding="utf-8")
        authority = surfaces["authority"].read_text(encoding="utf-8")
        current = Path("project_context/CURRENT_STATE.md").read_text(encoding="utf-8")
        trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "PACKAGE PREPARATION AUTHORIZED / CONTENT APPROVAL PENDING / RUNTIME NOT AUTHORIZED",
            decision,
        )
        self.assertIn("d2af53d739403ff6f4199fabe43159cb3de10317", decision)
        self.assertIn("APPROVED / BASELINED — EFFECTIVE AFTER MERGE", requirements)
        for requirement_id in (
            "REQ-HC-G1-NAV-001",
            "REQ-HC-G1-JOB-001",
            "REQ-HC-G1-TREAT-001",
            "REQ-HC-G1-STAT-001",
            "REQ-HC-G1-ADMIN-001",
            "REQ-HC-G1-ADAPT-001",
            "REQ-HC-G1-DTOOLS-001",
        ):
            self.assertIn(requirement_id, requirements)

        self.assertIn("EDGE_HOST_REQUIRED / NOT YET SELECTED", design)
        self.assertIn("1024×600", design)
        self.assertIn("G1-1", plan)
        self.assertIn("G1-6", plan)
        self.assertIn("clean assertion RED", plan)
        self.assertIn("APPROVED / ACTIVE — PROSPECTIVELY AFTER MERGE", authority)
        self.assertIn("Przed merge i Repository Verification", authority)
        for forbidden_boundary in (
            "Generation 2",
            "real data",
            "network/cloud",
            "KVK I/O",
            "PLC/safety mutation",
            "invoicing",
            "public distribution",
        ):
            self.assertIn(forbidden_boundary, authority)

        self.assertIn("`REQ-HC-003-G1`: `APPROVED / BASELINED PROSPECTIVELY", current)
        self.assertIn("`IA-HC-008`: `ACTIVATION READY", current)
        self.assertIn(
            "| HC-IA-008 | Generation 1 HMI GUI and DTools authority | IA-HC-008 | ACTIVATION READY / OWNER MERGE REQUIRED |",
            trace,
        )


if __name__ == "__main__":
    unittest.main()
