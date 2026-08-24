# Kinco DTools Bridge v0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Zbudować lokalny, fail-closed serwer MCP dla Windows 11, który steruje wyłącznie projektem `HoofCare_GL100E_G1` w Kinco DTools i zatrzymuje się przed zapisem.

**Architecture:** Rdzeń polityki, sesji i kontrolera pozostaje niezależny od Windows i jest testowany na Linux CI przez deterministyczny backend testowy. Adapter Windows łączy się z istniejącym procesem DTools przez pywinauto, najpierw backendem Win32 odpowiednim dla MFC, a pomocniczo UIA; typowany serwer MCP v2 udostępnia wyłącznie zamknięty katalog operacji. Pakiet Windows uruchamia MCP przez `stdio`, zapisuje dowody lokalnie i nie otwiera portu sieciowego.

**Tech Stack:** CPython 3.13; biblioteka standardowa; `mcp>=2,<3`; `pywinauto==0.6.8`; `Pillow>=11,<13`; `pywin32>=306,<400`; `PyInstaller>=6.22,<7`; `unittest`.

**Spec:** `docs/superpowers/specs/2026-08-24-kinco-dtools-bridge-design.md`

## Global Constraints

- Zakres wyłącznie `synthetic/test-only` pod aktywnym `IA-HC-008`.
- Proces docelowy: ręcznie wskazany plik wykonywalny Kinco DTools, związany z
  zapisanym SHA-256; exact projekt: `HoofCare_GL100E_G1`.
- Brak PLC, KVK, HMI, COM, Ethernet, USB, urządzeń, konfiguracji komunikacji, uploadu, downloadu, transferu i deploymentu.
- Brak generic shell, dowolnych współrzędnych, dowolnych skrótów i dowolnych nazw procesów w interfejsie MCP.
- Zapis i zamknięcie wymagają potwierdzenia; v0.1 kończy się przed wykonaniem zapisu.
- Każda akcja ma precondition, policy decision, postcondition i rekord JSONL.
- Nieznany lub niejednoznaczny stan zatrzymuje sesję fail-closed.
- MCP v0.1 używa wyłącznie lokalnego transportu `stdio`; etap WWW pozostaje poza zakresem.
- Istniejące nieśledzone artefakty AHK i DTools są własnością użytkownika i nie mogą zostać usunięte ani nadpisane.

## Docelowa struktura plików

- `src/hoofcare/dtools_bridge/__init__.py` — publiczne typy Bridge.
- `src/hoofcare/dtools_bridge/model.py` — enumy i niezmienne rekordy wejścia/wyjścia.
- `src/hoofcare/dtools_bridge/policy.py` — permanent denylist i kontekstowa allowlista.
- `src/hoofcare/dtools_bridge/session.py` — token, STOP i przejścia stanu.
- `src/hoofcare/dtools_bridge/audit.py` — redagowany JSONL i dowody obrazowe.
- `src/hoofcare/dtools_bridge/backend.py` — protokół backendu i deterministyczny backend testowy.
- `src/hoofcare/dtools_bridge/controller.py` — wspólny pipeline pre/action/post.
- `src/hoofcare/dtools_bridge/windows_backend.py` — pywinauto Win32/UIA i zrzut DTools.
- `src/hoofcare/dtools_bridge/server.py` — dokładny katalog narzędzi MCP v2.
- `src/hoofcare/dtools_bridge/__main__.py` — lokalny entry point `stdio`.
- `dtools/gl100e/bridge/allowlist.json` — wersjonowana konfiguracja kroków DTools.
- `dtools/gl100e/bridge/requirements-windows.txt` — zależności Windows.
- `dtools/gl100e/bridge/HoofCare.DToolsBridge.spec` — deterministyczny profil PyInstaller.
- `scripts/windows/dtools_bridge/Build-DToolsBridge.ps1` — build per-user bez instalacji sterowników.
- `scripts/windows/dtools_bridge/Install-DToolsBridge.ps1` — instalacja do `%LOCALAPPDATA%`.
- `scripts/windows/dtools_bridge/Run-DToolsBridge.cmd` — jawne uruchomienie procesu.
- `scripts/windows/dtools_bridge/DToolsBridgeEmulator.py` — lokalny emulator okien do testów Windows.
- `tests/test_dtools_bridge_policy.py` — polityka i permanent boundary.
- `tests/test_dtools_bridge_session.py` — token i STOP.
- `tests/test_dtools_bridge_audit.py` — JSONL i redakcja.
- `tests/test_dtools_bridge_controller.py` — pipeline i postconditions.
- `tests/test_dtools_bridge_server.py` — katalog i schemat MCP.
- `tests/test_dtools_bridge_windows.py` — testy Windows przeciw emulatorowi.
- `docs/verification/HC-G1-5-DTools-Bridge-Verification.md` — macierz wyników prototypu.

---

### Task 1: Niezmienne typy i permanentna granica polityki

**Files:**
- Create: `src/hoofcare/dtools_bridge/__init__.py`
- Create: `src/hoofcare/dtools_bridge/model.py`
- Create: `src/hoofcare/dtools_bridge/policy.py`
- Create: `dtools/gl100e/bridge/allowlist.json`
- Create: `tests/test_dtools_bridge_policy.py`

**Interfaces:**
- Produces: `ActionKind`, `BridgeState`, `WindowSnapshot`, `ActionRequest`, `PolicyDecision`, `ActionPolicy.evaluate(request, snapshot)`.
- Consumes: exact project name `HoofCare_GL100E_G1` and the versioned allowlist JSON.

- [ ] **Step 1: Write the failing policy tests**

```python
from pathlib import Path
import unittest

from hoofcare.dtools_bridge.model import ActionKind, ActionRequest, WindowSnapshot
from hoofcare.dtools_bridge.policy import ActionPolicy


class ActionPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = ActionPolicy.from_file(
            Path("dtools/gl100e/bridge/allowlist.json")
        )
        self.snapshot = WindowSnapshot(
            pid=4242,
            process_name="KincoDToolsSynthetic.exe",
            executable_sha256="a" * 64,
            window_class="Afx:00400000",
            title="HoofCare_GL100E_G1 - [HMI0.whe]",
            project_name="HoofCare_GL100E_G1",
            active_dialog=None,
        )

    def test_allows_named_bitmap_editor_step_for_exact_project(self):
        request = ActionRequest(ActionKind.RUN_STEP, "open_bitmap_editor")
        self.assertEqual(self.policy.evaluate(request, self.snapshot).code, "ALLOW")

    def test_permanently_denies_download_even_if_named_like_a_step(self):
        request = ActionRequest(ActionKind.RUN_STEP, "download_project")
        decision = self.policy.evaluate(request, self.snapshot)
        self.assertEqual(decision.code, "DENIED_PERMANENT_BOUNDARY")
        self.assertFalse(decision.allowed)

    def test_denies_a_different_project_before_control_lookup(self):
        wrong = WindowSnapshot(**{
            **self.snapshot.__dict__, "project_name": "Production_Project"
        })
        decision = self.policy.evaluate(
            ActionRequest(ActionKind.ACTIVATE, "bitmap_component"), wrong
        )
        self.assertEqual(decision.code, "PROJECT_MISMATCH")
```

- [ ] **Step 2: Run the focused test and verify RED**

Run: `PYTHONPATH=src python -m unittest tests.test_dtools_bridge_policy -v`

Expected: `ERROR` because `hoofcare.dtools_bridge` does not exist.

- [ ] **Step 3: Implement the immutable model and minimal policy**

Use frozen dataclasses and string enums. `ActionPolicy.evaluate` must check in this order: exact executable SHA-256 and project context, permanent forbidden token scan, exact action-kind allowlist, exact named target. Hand-author `allowlist.json` with only these v0.1 named steps: `inspect`, `capture`, `open_bitmap_component`, `open_bitmap_editor`, `load_g1_00_bitmap`, `verify_bitmap_loaded`, `request_save`, `emergency_stop`. Store neither raw key sequences nor arbitrary coordinates in this file.

```python
class ActionKind(StrEnum):
    INSPECT = "inspect"
    CAPTURE = "capture"
    ACTIVATE = "activate"
    OPEN_MENU = "open_menu"
    SET_TEXT = "set_text"
    SEND_SHORTCUT = "send_shortcut"
    RUN_STEP = "run_step"
    REQUEST_SAVE = "request_save"
    EMERGENCY_STOP = "emergency_stop"


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    code: str
    reason: str
```

- [ ] **Step 4: Run policy tests and full Linux regression**

Run: `PYTHONPATH=src python -m unittest tests.test_dtools_bridge_policy -v`

Expected: all Task 1 tests `OK`.

Run: `PYTHONPATH=src python -m unittest discover -s tests -v`

Expected: repository suite `OK`; Windows-only tests do not exist yet.

- [ ] **Step 5: Inspect and commit Task 1**

Run: `git diff --check`

Commit: `git commit -m "feat: define DTools bridge safety policy"`

---

### Task 2: Token sesji, awaryjny STOP i redagowany audit trail

**Files:**
- Create: `src/hoofcare/dtools_bridge/session.py`
- Create: `src/hoofcare/dtools_bridge/audit.py`
- Create: `tests/test_dtools_bridge_session.py`
- Create: `tests/test_dtools_bridge_audit.py`

**Interfaces:**
- Consumes: `BridgeState`, `ActionRequest`, `PolicyDecision`, `WindowSnapshot` from Task 1.
- Produces: `SessionGuard.issue_token() -> str`, `SessionGuard.authorize(token)`, `SessionGuard.stop(reason)`, `AuditLog.append(...) -> int`, `AuditLog.record_evidence(image, phase) -> str`.

- [ ] **Step 1: Write failing session and audit tests**

```python
class SessionGuardTests(unittest.TestCase):
    def test_stop_invalidates_token_and_rejects_future_actions(self):
        guard = SessionGuard()
        token = guard.issue_token()
        guard.stop("operator_hotkey")
        with self.assertRaisesRegex(SessionStopped, "operator_hotkey"):
            guard.authorize(token)

    def test_new_session_uses_a_different_unguessable_token(self):
        first = SessionGuard().issue_token()
        second = SessionGuard().issue_token()
        self.assertNotEqual(first, second)
        self.assertGreaterEqual(len(first), 32)


class AuditLogTests(unittest.TestCase):
    def test_record_redacts_token_and_text_value(self):
        with tempfile.TemporaryDirectory() as directory:
            log = AuditLog(Path(directory))
            log.append(tool="dtools_set_text", arguments={
                "token": "session-secret", "value": "animal-secret"
            }, decision="ALLOW", result="OK")
            payload = (Path(directory) / "audit.jsonl").read_text("utf-8")
            self.assertNotIn("session-secret", payload)
            self.assertNotIn("animal-secret", payload)
            self.assertIn('"token": "[REDACTED]"', payload)
```

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src python -m unittest tests.test_dtools_bridge_session tests.test_dtools_bridge_audit -v`

Expected: imports fail because `session.py` and `audit.py` are absent.

- [ ] **Step 3: Implement state machine and append-only audit**

Use `secrets.token_urlsafe(32)`, `hmac.compare_digest`, an in-process lock and monotonic operation numbers. States: `IDLE`, `ACTIVE`, `AWAITING_SAVE_CONFIRMATION`, `STOPPED_FAIL_CLOSED`, `EMERGENCY_STOPPED`. Audit writes one compact JSON object per line with `flush()` and `os.fsync()`; redact keys `token`, `value`, `text`, `credential`, `password` recursively. Evidence names use only session ID, operation number and `before|after`.

- [ ] **Step 4: Run focused tests and regression**

Run: `PYTHONPATH=src python -m unittest tests.test_dtools_bridge_session tests.test_dtools_bridge_audit -v`

Expected: all Task 2 tests `OK`.

Run: `PYTHONPATH=src python scripts/run_coverage.py`

Expected: suite `OK` and local `.coverage-trace` artifacts created.

- [ ] **Step 5: Commit Task 2**

Commit: `git commit -m "feat: add fail-closed bridge session audit"`

---

### Task 3: Kontroler pre/action/post z deterministycznym backendem

**Files:**
- Create: `src/hoofcare/dtools_bridge/backend.py`
- Create: `src/hoofcare/dtools_bridge/controller.py`
- Create: `tests/test_dtools_bridge_controller.py`

**Interfaces:**
- Consumes: model, policy, session and audit interfaces from Tasks 1–2.
- Produces: `DToolsBackend` protocol, `BackendAction`, `BridgeController.execute(token, request) -> ActionResult`.

- [ ] **Step 1: Write failing controller behavior tests**

```python
class BridgeControllerTests(unittest.TestCase):
    def test_executes_once_and_verifies_expected_postcondition(self):
        backend = DeterministicBackend.exact_project()
        controller, token = make_controller(backend)
        result = controller.execute(
            token, ActionRequest(ActionKind.RUN_STEP, "open_bitmap_editor")
        )
        self.assertEqual(result.code, "OK")
        self.assertEqual(backend.performed, ["open_bitmap_editor"])
        self.assertEqual(result.postcondition, "bitmap_editor_open")

    def test_postcondition_mismatch_stops_session_without_retry(self):
        backend = DeterministicBackend.exact_project(
            outcomes={"open_bitmap_editor": "main_editor"}
        )
        controller, token = make_controller(backend)
        result = controller.execute(
            token, ActionRequest(ActionKind.RUN_STEP, "open_bitmap_editor")
        )
        self.assertEqual(result.code, "POSTCONDITION_MISMATCH")
        self.assertEqual(backend.performed, ["open_bitmap_editor"])
        self.assertEqual(controller.session.state, BridgeState.STOPPED_FAIL_CLOSED)

    def test_denied_action_never_reaches_backend(self):
        backend = DeterministicBackend.exact_project()
        controller, token = make_controller(backend)
        result = controller.execute(
            token, ActionRequest(ActionKind.RUN_STEP, "download_project")
        )
        self.assertEqual(result.code, "DENIED_PERMANENT_BOUNDARY")
        self.assertEqual(backend.performed, [])
```

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src python -m unittest tests.test_dtools_bridge_controller -v`

Expected: imports fail because backend and controller are absent.

- [ ] **Step 3: Implement one-operation controller pipeline**

`DToolsBackend` exposes exactly `snapshot()`, `capture()`, `perform_named_step(name)`, `activate(control_id)`, `set_text(control_id, value)`, `send_shortcut(shortcut_id)`. Controller authorizes token, snapshots, records evidence, evaluates policy, calls the one selected backend method, snapshots again, checks the literal postcondition from allowlist, logs the result and returns. It never retries a mutation and never auto-recovers an unexpected dialog.

- [ ] **Step 4: Run focused tests, mutation review and regression**

Run: `PYTHONPATH=src python -m unittest tests.test_dtools_bridge_controller -v`

Expected: all Task 3 tests `OK`.

Manually mutate the test backend outcome from `bitmap_editor_open` to `main_editor`; confirm the mismatch test fails if controller stops checking postconditions, then restore the code.

Run: `PYTHONPATH=src python -m unittest discover -s tests -v`

Expected: suite `OK`.

- [ ] **Step 5: Commit Task 3**

Commit: `git commit -m "feat: add verified DTools action pipeline"`

---

### Task 4: Adapter Windows MFC/UIA i niezależny awaryjny skrót

**Files:**
- Create: `src/hoofcare/dtools_bridge/windows_backend.py`
- Create: `scripts/windows/dtools_bridge/DToolsBridgeEmulator.py`
- Create: `tests/test_dtools_bridge_windows.py`

**Interfaces:**
- Consumes: `DToolsBackend`, `WindowSnapshot` and named steps from Tasks 1–3.
- Produces: `WindowsDToolsBackend.connect_exact(project_name, executable_path, executable_sha256)`, `EmergencyHotkey.start(callback)`, `EmergencyHotkey.close()`.

- [ ] **Step 1: Write Windows-only failing integration tests**

```python
@unittest.skipUnless(sys.platform == "win32", "Windows UI automation only")
class WindowsBackendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.emulator = subprocess.Popen([
            sys.executable,
            "scripts/windows/dtools_bridge/DToolsBridgeEmulator.py",
            "--project", "HoofCare_GL100E_G1",
        ])

    def test_connect_exact_reads_project_and_dialog(self):
        backend = WindowsDToolsBackend.connect_exact(
            "HoofCare_GL100E_G1", self.emulator_exe, self.emulator_sha256
        )
        snapshot = backend.snapshot()
        self.assertEqual(snapshot.project_name, "HoofCare_GL100E_G1")
        self.assertIsNone(snapshot.active_dialog)

    def test_unknown_dialog_is_reported_not_closed(self):
        signal_emulator("show_unknown_dialog")
        snapshot = WindowsDToolsBackend.connect_exact(
            "HoofCare_GL100E_G1", self.emulator_exe, self.emulator_sha256
        ).snapshot()
        self.assertEqual(snapshot.active_dialog, "Unexpected Dialog")
```

The emulator must expose real Tk/Win32 windows labelled like the required DTools states, but use process name `DToolsBridgeEmulator` so production matching can only be enabled by an explicit test-only constructor. Cleanup terminates only the subprocess created by the test.

- [ ] **Step 2: Verify RED on Windows and safe skip on Linux**

Windows run: `set PYTHONPATH=src&& python -m unittest tests.test_dtools_bridge_windows -v`

Expected on Windows: import failure because `windows_backend.py` is absent.

Linux CI run: `PYTHONPATH=src python -m unittest tests.test_dtools_bridge_windows -v`

Expected on Linux: tests `skipped`, not failed.

- [ ] **Step 3: Implement process-scoped MFC/UIA discovery**

Resolve PID only from the manually selected executable path, verify its SHA-256 before connection, then connect using `pywinauto.Application(backend="win32").connect(process=pid)` because DTools is MFC; use a second `Application(backend="uia")` view only for controls exposed by UIA. Require one matching top-level window and exact project token in title. Capture only the main window rectangle with `PIL.ImageGrab.grab(bbox=...)`. Named steps may resolve controls by class/title/automation ID from the allowlist implementation, but no MCP argument may provide coordinates or raw keys.

Register `Ctrl+Alt+F12` using Win32 `RegisterHotKey` on a dedicated thread. The callback calls only `SessionGuard.stop("operator_hotkey")`; it must not send input to DTools.

- [ ] **Step 4: Run Windows integration suite against emulator**

Run on Windows: `set PYTHONPATH=src&& python -m unittest tests.test_dtools_bridge_windows -v`

Expected: exact project discovery, unknown-dialog reporting, window-only capture and hotkey tests all `OK`.

Run on Linux: `PYTHONPATH=src python -m unittest discover -s tests -v`

Expected: all portable tests `OK`; Windows integration tests explicitly skipped.

- [ ] **Step 5: Commit Task 4**

Commit: `git commit -m "feat: add process-scoped Windows DTools backend"`

---

### Task 5: Typowany serwer MCP v2 bez powierzchni generic execute

**Files:**
- Create: `src/hoofcare/dtools_bridge/server.py`
- Create: `src/hoofcare/dtools_bridge/__main__.py`
- Create: `tests/test_dtools_bridge_server.py`

**Interfaces:**
- Consumes: `BridgeController` and Windows backend factory.
- Produces: `create_server(controller) -> MCPServer` and CLI entry point `python -m hoofcare.dtools_bridge`.

- [ ] **Step 1: Write failing MCP contract tests**

```python
from mcp import Client


class DToolsBridgeServerTests(unittest.IsolatedAsyncioTestCase):
    async def test_catalog_is_exact_and_contains_no_generic_executor(self):
        server = create_server(make_test_controller())
        async with Client(server) as client:
            catalog = await client.list_tools()
            names = {tool.name for tool in catalog.tools}
            self.assertEqual(names, {
                "dtools_status", "dtools_inspect", "dtools_capture",
                "dtools_activate", "dtools_open_menu", "dtools_set_text",
                "dtools_send_shortcut", "dtools_run_step",
                "dtools_request_save", "dtools_emergency_stop",
            })
            self.assertTrue(names.isdisjoint(
                {"execute", "shell", "click", "keypress"}
            ))

    async def test_download_step_returns_permanent_denial(self):
        server = create_server(make_test_controller())
        async with Client(server) as client:
            result = await client.call_tool(
                "dtools_run_step", {"step": "download_project"}
            )
            self.assertEqual(result.structured_content["code"],
                             "DENIED_PERMANENT_BOUNDARY")
```

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src python -m unittest tests.test_dtools_bridge_server -v`

Expected: imports fail because `server.py` is absent.

- [ ] **Step 3: Implement exact MCP v2 catalog and stdio entry point**

Use `from mcp.server import MCPServer` from the stable v2 line. Tool functions accept enum-backed strings only and return typed dataclasses/dicts. `__main__.py` validates the allowlist path and log directory before constructing `WindowsDToolsBackend`; on non-Windows it exits with code `2` and message `WINDOWS_REQUIRED`. Run only the SDK's `stdio` transport in v0.1.

- [ ] **Step 4: Run MCP contract tests and Inspector smoke test**

Run: `PYTHONPATH=src python -m unittest tests.test_dtools_bridge_server -v`

Expected: catalog and denial tests `OK`.

Run on Windows development environment: `mcp dev src/hoofcare/dtools_bridge/server.py`

Expected: exactly ten tools visible; no resources, prompts, shell, coordinates or raw-key tool.

- [ ] **Step 5: Commit Task 5**

Commit: `git commit -m "feat: expose bounded DTools MCP server"`

---

### Task 6: Pakiet Windows, instalacja per-user i dowody końcowe

**Files:**
- Create: `dtools/gl100e/bridge/requirements-windows.txt`
- Create: `dtools/gl100e/bridge/HoofCare.DToolsBridge.spec`
- Create: `scripts/windows/dtools_bridge/Build-DToolsBridge.ps1`
- Create: `scripts/windows/dtools_bridge/Install-DToolsBridge.ps1`
- Create: `scripts/windows/dtools_bridge/Run-DToolsBridge.cmd`
- Create: `docs/verification/HC-G1-5-DTools-Bridge-Verification.md`
- Modify: `.github/workflows/runtime-ci.yml`

**Interfaces:**
- Consumes: runnable module from Task 5.
- Produces: `dist/HoofCare.DToolsBridge/HoofCare.DToolsBridge.exe`, per-user installation under `%LOCALAPPDATA%\HoofCare\DToolsBridge`, verification record.

- [ ] **Step 1: Write failing package-contract tests**

Add `tests/test_dtools_bridge_package.py` that parses the PyInstaller spec and PowerShell scripts as structured configuration only where execution is not possible on Linux, and executes their safe validation modes on Windows:

```python
class DToolsBridgePackageTests(unittest.TestCase):
    def test_windows_requirements_have_bounded_major_versions(self):
        lines = set(REQUIREMENTS.read_text("utf-8").splitlines())
        self.assertIn("mcp>=2,<3", lines)
        self.assertIn("pywinauto==0.6.8", lines)
        self.assertIn("PyInstaller>=6.22,<7", lines)

    @unittest.skipUnless(sys.platform == "win32", "Windows packaging only")
    def test_installer_validate_mode_makes_no_installation_changes(self):
        result = subprocess.run([
            "powershell.exe", "-NoProfile", "-File",
            "scripts/windows/dtools_bridge/Install-DToolsBridge.ps1",
            "-ValidateOnly",
        ], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALIDATION_OK", result.stdout)
```

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src python -m unittest tests.test_dtools_bridge_package -v`

Expected: failure because requirements, spec and installer do not exist.

- [ ] **Step 3: Implement deterministic Windows build and per-user install**

Requirements contain exactly:

```text
mcp>=2,<3
Pillow>=11,<13
pywin32>=306,<400
pywinauto==0.6.8
PyInstaller>=6.22,<7
```

Build script creates an isolated virtual environment, installs only the file above, runs the full portable and Windows test suites, then calls PyInstaller with the checked-in spec. Installer accepts `-ValidateOnly` and otherwise copies the built directory to `%LOCALAPPDATA%\HoofCare\DToolsBridge`; it creates no service, scheduled task, firewall rule, driver or autostart entry. During first local configuration the operator selects the Kinco DTools executable and synthetic project directory; Bridge records their canonical paths plus executable SHA-256. Runner sets these exact values, allowlist and log paths and launches the executable via `stdio`.

- [ ] **Step 4: Extend CI without pretending Linux validates Windows UI**

Keep the existing `runtime-quality` job. Add a `dtools-bridge-windows` job on `windows-latest` that installs the bounded requirements and runs:

```powershell
$env:PYTHONPATH = "src"
python -m unittest tests.test_dtools_bridge_policy `
  tests.test_dtools_bridge_session `
  tests.test_dtools_bridge_audit `
  tests.test_dtools_bridge_controller `
  tests.test_dtools_bridge_server `
  tests.test_dtools_bridge_windows `
  tests.test_dtools_bridge_package -v
```

Do not run DTools itself in CI; the emulator is the Windows integration boundary.

- [ ] **Step 5: Run broad verification and create the verification record**

Linux:

```bash
python -m compileall -q src tests scripts
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python scripts/run_coverage.py
python scripts/check_foundation.py
python scripts/check_semantic_governance.py
git diff --check
```

Windows:

```powershell
powershell.exe -NoProfile -File scripts/windows/dtools_bridge/Build-DToolsBridge.ps1
powershell.exe -NoProfile -File scripts/windows/dtools_bridge/Install-DToolsBridge.ps1 -ValidateOnly
```

Record exact Python, dependency and PyInstaller versions, test counts, artifact SHA-256, operating system build and explicit statements `REAL_DTOOLS_PROBE=NOT_YET_RUN`, `PROJECT_SAVE=NOT_AUTHORIZED`, `DEVICE_ACCESS=NONE` in `HC-G1-5-DTools-Bridge-Verification.md`.

- [ ] **Step 6: Commit Task 6**

Commit: `git commit -m "build: package local DTools bridge for Windows"`

---

### Task 7: Kontrolowana próba na kopii rzeczywistego projektu DTools

**Files:**
- Modify: `docs/verification/HC-G1-5-DTools-Bridge-Verification.md`
- Create on Windows outside Git: Bridge JSONL log and before/after screenshots.

**Interfaces:**
- Consumes: installed Bridge, DTools V4.5.6.0 and a verified copy of `HoofCare_GL100E_G1`.
- Produces: evidence-backed result ending in `AWAITING_SAVE_CONFIRMATION`, never a saved or downloaded project.

- [ ] **Step 1: Establish a recoverable test target**

Close DTools, copy the entire synthetic project directory to a timestamped sibling, hash both source and working copy, then open only the working copy. Confirm no HMI, PLC, COM, USB or Ethernet device is attached or configured for the test.

- [ ] **Step 2: Run read-only discovery first**

Call only `dtools_status`, `dtools_inspect` and `dtools_capture`. Expected: one matching DTools process, exact project, no dialog and a complete audit record. Any mismatch ends the trial.

- [ ] **Step 3: Execute the bitmap vertical slice**

Run exact named steps in order: `open_bitmap_component`, `open_bitmap_editor`, `load_g1_00_bitmap`, `verify_bitmap_loaded`, `request_save`. Expected terminal state: `AWAITING_SAVE_CONFIRMATION`; no `Ctrl+S`, menu Save, project close, compile or download action occurs.

- [ ] **Step 4: Exercise emergency STOP independently**

Restart from the untouched copy, begin a read-only inspection, press `Ctrl+Alt+F12`, then attempt `dtools_capture`. Expected: `EMERGENCY_STOPPED`; the request is rejected and DTools remains open.

- [ ] **Step 5: Reconcile evidence and run final regression**

Update the verification record with exact log hashes, screenshot hashes, DTools version, result of each pre/postcondition and `PROJECT_SAVE=NOT_EXECUTED`. Run the full Linux and Windows suites again from the final tree.

- [ ] **Step 6: Prepare the final review commit without merge**

Commit: `git commit -m "test: verify bounded DTools bridge prototype"`

Stop with a final diff, exact head SHA, test evidence and remaining limitation. Do not push, open a PR, merge, save the DTools project or start the WWW transport stage without the applicable separate authority and Project Owner decision.
