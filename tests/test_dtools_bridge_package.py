from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "dtools" / "gl100e" / "bridge"
SCRIPTS = ROOT / "scripts" / "windows" / "dtools_bridge"
RUNTIME_WORKFLOW = ROOT / ".github" / "workflows" / "runtime-ci.yml"


class DToolsBridgePackageTests(unittest.TestCase):
    def test_windows_requirements_have_bounded_major_versions(self):
        lines = set(
            (BRIDGE / "requirements-windows.txt")
            .read_text("utf-8")
            .splitlines()
        )

        self.assertIn("mcp>=2,<3", lines)
        self.assertIn("pywinauto==0.6.8", lines)
        self.assertIn("PyInstaller>=6.22,<7", lines)
        self.assertIn("pywin32>=306,<400", lines)

    def test_pyinstaller_profile_is_onedir_and_has_fixed_name(self):
        payload = (BRIDGE / "HoofCare.DToolsBridge.spec").read_text("utf-8")

        self.assertIn("name='HoofCare.DToolsBridge'", payload)
        self.assertIn("COLLECT(", payload)
        self.assertNotIn("onefile", payload.casefold())

    def test_pyinstaller_excludes_optional_mcp_cli(self):
        payload = (BRIDGE / "HoofCare.DToolsBridge.spec").read_text("utf-8")

        self.assertIn('is_module_or_submodule(name, "mcp.cli")', payload)

    def test_pyinstaller_resolves_entrypoint_from_repository_root(self):
        payload = (BRIDGE / "HoofCare.DToolsBridge.spec").read_text("utf-8")

        self.assertIn("SPECPATH", payload)
        self.assertIn('repository_root / "src/hoofcare/dtools_bridge/__main__.py"', payload)

    def test_installer_is_per_user_and_creates_no_persistence(self):
        payload = (SCRIPTS / "Install-DToolsBridge.ps1").read_text("utf-8")
        folded = payload.casefold()

        self.assertIn("$env:localappdata", folded)
        self.assertIn("validateonly", folded)
        for forbidden in (
            "new-service",
            "scheduledtask",
            "netsh",
            "new-netfirewallrule",
            "currentversion\\run",
        ):
            self.assertNotIn(forbidden, folded)

    def test_installer_prompts_for_exact_executable_and_project_folder(self):
        payload = (SCRIPTS / "Install-DToolsBridge.ps1").read_text("utf-8")

        self.assertIn("OpenFileDialog", payload)
        self.assertIn("FolderBrowserDialog", payload)

    def test_launcher_enforces_read_only_mode(self):
        payload = (SCRIPTS / "Run-DToolsBridge.cmd").read_text("ascii")

        self.assertIn("--read-only", payload)

    def test_separate_automation_launcher_enables_named_compile_without_raw_execution(self):
        payload = (SCRIPTS / "Run-DToolsBridge-Automation.cmd").read_text(
            "ascii"
        )
        installer = (SCRIPTS / "Install-DToolsBridge.ps1").read_text("ascii")

        self.assertNotIn("--read-only", payload)
        self.assertIn("HoofCare.DToolsBridge.exe", payload)
        self.assertNotIn("%*", payload)
        self.assertIn("Run-DToolsBridge-Automation.cmd", installer)

    def test_powershell_scripts_are_ascii_safe_for_windows_powershell_51(self):
        for script in SCRIPTS.glob("*.ps1"):
            with self.subTest(script=script.name):
                script.read_bytes().decode("ascii")

    def test_build_stops_immediately_when_python_313_is_missing(self):
        payload = (SCRIPTS / "Build-DToolsBridge.ps1").read_text("ascii")
        create_venv = payload.index("& py -3.13 -m venv")
        python_path = payload.index("$Python =", create_venv)

        self.assertIn("$LASTEXITCODE", payload[create_venv:python_path])

    def test_windows_ci_builds_and_publishes_installable_bridge(self):
        payload = RUNTIME_WORKFLOW.read_text("utf-8")

        self.assertIn("Build installable DTools Bridge", payload)
        self.assertIn("Build-DToolsBridge.ps1", payload)
        self.assertIn("actions/upload-artifact@v4", payload)
        self.assertIn("HoofCare-DToolsBridge-Windows", payload)
        self.assertIn("dist/HoofCare.DToolsBridge", payload)

    @unittest.skipUnless(sys.platform == "win32", "Windows packaging only")
    def test_installer_validate_mode_makes_no_installation_changes(self):
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-File",
                str(SCRIPTS / "Install-DToolsBridge.ps1"),
                "-ValidateOnly",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALIDATION_OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
