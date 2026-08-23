# Generation 1 HMI GUI and DTools Implementation Plan

## Status

`APPROVED / ACTIVE — EFFECTIVE AFTER MERGE AND REPOSITORY VERIFICATION OF HC-IA-HC-008-ACTIVATION-001`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Zrealizować kompletne lokalne GUI Generacji 1 dla Pawła i właściciela oraz zweryfikowany offline projekt Kinco DTools dla GL100E bez rozszerzenia granic urządzeń, danych lub wdrożenia.

**Architecture:** Kanoniczna domena i usługi aplikacyjne pozostają jedynym źródłem reguł. Nowa warstwa `hmi/gen1` dostarcza immutable semantyczne view modele i deterministyczny graf tras, `physical/gen1_layout.py` mapuje je na profil GL100E, a repozytoryjny manifest DTools wiąże widgety z semantyką bez kopiowania logiki biznesowej. Operacyjne połączenie z HMI pozostaje zablokowane przez `EDGE_HOST_REQUIRED / NOT YET SELECTED`.

**Tech Stack:** Python 3.12 standard library, `dataclasses`, `Enum`, `unittest`, JSON Schema v1 jako repozytoryjny kontrakt manifestu, Kinco DTools wyłącznie do natywnego offline build/compile.

**Spec:** `docs/design/UX-HC-002_Generation_1_Complete_HMI_GUI_and_DTools_v0.1.md`

## Global Constraints

- Runtime start requires `REQ-HC-003-G1 = APPROVED / BASELINED` and `IA-HC-008 = APPROVED / ACTIVE` after a separate activation record and Repository Verification.
- Each G1 increment uses clean assertion RED → remote test-only checkpoint → minimal GREEN → full regression → Draft PR → exact-head owner approval.
- All fixtures, farms, animals, operators, prices, credentials and bindings are local synthetic/test-only.
- GUI never recalculates money, cow counts, material totals, pricing freeze or clinical domain rules.
- Prices are hidden on routine treatment screens and remain available to Paweł only at approved stages.
- GL100E `1024×600` is a device profile; minimum touch target is `64×64 px`.
- No Generation 2, real data, network/cloud, synchronization, live RFID, camera, device access, KVK I/O, machine control, hydraulics, PLC/safety mutation, invoicing, VAT, accounting, payments, deployment, signing, release or public distribution.
- Native DTools build evidence does not establish upload, physical acceptance or HW-A1/HW-A2/HW-A3 PASS.

## Planned file structure

| Path | Odpowiedzialność |
|---|---|
| `src/hoofcare/hmi/gen1/navigation.py` | route IDs, guards and recovery destination |
| `src/hoofcare/hmi/gen1/shell.py` | app shell, role state and owner-zone session |
| `src/hoofcare/hmi/gen1/job_views.py` | opening, pricing and active-job projections |
| `src/hoofcare/hmi/gen1/treatment_views.py` | treatment wizard projections and actions |
| `src/hoofcare/hmi/gen1/records_views.py` | statistics, history, settlement, reports and admin projections |
| `src/hoofcare/physical/gen1_layout.py` | adaptive regions and GL100E geometry |
| `dtools/gl100e/manifest.json` | screen/widget/binding truth for DTools |
| `dtools/gl100e/README.md` | tool version, native artifact path, hash and offline build evidence |
| `scripts/check_gen1_dtools_manifest.py` | fail-closed manifest validation |
| `tests/test_gen1_*.py` | public-behavior evidence per increment |

---

### Task G1-1: Application shell, route graph and owner boundary

**Files:**
- Create: `src/hoofcare/hmi/gen1/__init__.py`
- Create: `src/hoofcare/hmi/gen1/navigation.py`
- Create: `src/hoofcare/hmi/gen1/shell.py`
- Test: `tests/test_gen1_navigation.py`

**Interfaces:**
- Produces: `Gen1Route`, `RouteDecision`, `NavigationContext`, `next_route(context, action) -> RouteDecision`.
- Produces: `OwnerGateState`, `OwnerSession`, `unlock_owner_zone(pin, now, state) -> OwnerSession`.
- Consumes: no device, network or persistence adapter.

- [ ] **Step 1: Write the clean assertion RED**

```python
def test_route_graph_denies_owner_admin_without_owner_session():
    module = importlib.import_module("hoofcare.hmi.gen1.navigation")
    context = module.NavigationContext.synthetic_operator()
    decision = module.next_route(context, "open_owner_admin")
    self.assertEqual(decision.kind, module.RouteDecisionKind.DENY_WITH_REASON)
    self.assertEqual(decision.reason, "OWNER_UNLOCK_REQUIRED")
```

- [ ] **Step 2: Run and publish RED**

Run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest tests.test_gen1_navigation -v`

Expected: assertion failure `hoofcare.hmi.gen1.navigation must exist`; zero import/setup errors. Commit only the test and push the RED checkpoint.

- [ ] **Step 3: Implement minimal route and owner-gate contracts**

```python
class RouteDecisionKind(str, Enum):
    ALLOW = "ALLOW"
    DENY_WITH_REASON = "DENY_WITH_REASON"
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"

@dataclass(frozen=True)
class RouteDecision:
    kind: RouteDecisionKind
    destination: Gen1Route | None
    reason: str | None
```

Implement exact allowed transitions from the UX screen table. Accept only six ASCII digits for the synthetic PIN, count failed attempts, lock fail-closed and expire the owner session by injected timezone-aware time.
Use the exact contract: five consecutive failures lock attempts for five
minutes; a successful session expires after ten minutes of inactivity.

- [ ] **Step 4: Prove focused behavior**

Run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest tests.test_gen1_navigation -v`

Expected: PASS for route allow/deny/recovery, dirty-form back guard, PIN format, lockout, expiry and the rule that operator pricing routes do not require owner unlock.

- [ ] **Step 5: Run full regression and publish Draft PR**

Run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests -q`

Commit: `feat: add generation 1 application shell and route guards`.

### Task G1-2: Job opening, pricing and active-work dashboard

**Files:**
- Create: `src/hoofcare/hmi/gen1/job_views.py`
- Modify: `src/hoofcare/hmi/job_menu.py`
- Test: `tests/test_gen1_job_views.py`

**Interfaces:**
- Consumes: `Job`, `JobMenuView`, `JobScreenStage`, `JobStatistics`.
- Produces: `JobOpeningView`, `ActiveJobView`, `project_job_opening(job)`, `project_active_job(job, statistics)`.

- [ ] **Step 1: Write and publish RED**

```python
def test_active_job_hides_prices_but_shows_counts_and_materials():
    view = project_active_job(job=synthetic_open_job(), statistics=statistics())
    self.assertFalse(view.prices_visible)
    self.assertEqual(view.completed_cows, 2)
    self.assertEqual(view.primary_actions, ("new_cow", "resume_cow", "materials", "more"))
```

Run the focused module. Expected RED is a clean missing-surface assertion before production files exist. Push the test-only commit.

- [ ] **Step 2: Implement immutable projections**

```python
@dataclass(frozen=True)
class ActiveJobView:
    job_id: str
    farm_id: str
    completed_cows: int
    planned_cows: int | None
    unfinished_sessions: int
    material_quantities: tuple[MaterialQuantity, ...]
    prices_visible: bool
    primary_actions: tuple[str, ...]
```

Opening view exposes stored pricing snapshot and `set_prices`; active view exposes no `*_grosz` binding. Reuse `job_menu_view` for pricing eligibility; do not copy freeze rules.

- [ ] **Step 3: Verify focused and broad suites**

Run the focused test, `tests.test_job_menu`, `tests.test_job_price_correction_integration`, then the full suite. Inspect the diff for accidental money calculation or persistence.

- [ ] **Step 4: Commit and open Draft PR**

Commit: `feat: add generation 1 job opening and work views`.

### Task G1-3: Complete treatment wizard

**Files:**
- Create: `src/hoofcare/hmi/gen1/treatment_views.py`
- Modify: `src/hoofcare/hmi/workflow.py`
- Test: `tests/test_gen1_treatment_wizard.py`

**Interfaces:**
- Consumes: canonical session/clinical records and the existing workflow catalogue.
- Produces: `TreatmentStep`, `TreatmentWizardView`, `project_treatment_step(session, step)`, `allowed_treatment_actions(session, step)`.
- Does not consume camera, RFID or KVK adapters.

- [ ] **Step 1: Write and publish RED**

```python
def test_pawel_can_complete_every_required_treatment_step_without_camera():
    steps = tuple(step.value for step in complete_synthetic_wizard())
    self.assertEqual(
        steps,
        ("IDENTITY", "LIMB_CLAW", "ZONE_LESION", "TREATMENT", "MATERIALS", "FOLLOW_UP", "SUMMARY"),
    )
```

Expected RED: missing `complete_synthetic_wizard` assertion only. Persist the remote test-only checkpoint.

- [ ] **Step 2: Implement step projections and fail-closed guards**

Every step declares required canonical fields, visible actions and Polish labels. `complete_cow` appears only on `SUMMARY` when identity, clinical selection, treatment and durable-write prerequisites are valid. Camera and RFID actions are absent; their unavailable status is presentation text, never synthetic evidence.

- [ ] **Step 3: Verify persistence ordering and idempotency**

Run `tests.test_gen1_treatment_wizard`, `tests.test_session_core`, `tests.test_canonical_clinical_records`, `tests.test_job_lifecycle` and `tests.test_job_persistence`. Add a negative assertion that a failed store leaves the counter unchanged.

- [ ] **Step 4: Full regression and Draft PR**

Commit: `feat: add generation 1 treatment wizard projections`.

### Task G1-4: Statistics, history, settlement, reports and owner admin views

**Files:**
- Create: `src/hoofcare/hmi/gen1/records_views.py`
- Test: `tests/test_gen1_records_views.py`

**Interfaces:**
- Consumes: `JobStatistics`, `SettlementDocument`, stored synthetic jobs and explicit application capabilities.
- Produces: `WorkStatisticsView`, `HistoryView`, `SettlementView`, `OwnerDashboardView`, `AdminCapabilityView`.

- [ ] **Step 1: Write and publish RED**

```python
def test_work_and_settlement_views_keep_money_at_the_correct_boundary():
    work = project_work_statistics(statistics_fixture())
    closed = project_settlement(settlement_document_fixture())
    self.assertFalse(work.prices_visible)
    self.assertEqual(work.money_bindings, ())
    self.assertEqual(closed.total_label, "RAZEM NETTO: 122,00 zł")
```

Expected RED: one clean missing-surface failure. Push before implementation.

- [ ] **Step 2: Implement read-only view projections**

Use only stored values. `AdminCapabilityView` receives an explicit tuple of application capability IDs and exposes no action absent from that tuple. History filters remain inclusive and local. PDF action calls the existing settlement renderer.

- [ ] **Step 3: Verify role and financial boundaries**

Run the focused tests plus `tests.test_job_statistics`, `tests.test_job_statistics_hmi`, `tests.test_job_settlement_report` and `tests.test_job_settlement_integration`. Assert no work-screen field ends in `_grosz` and no owner capability implies device or KVK control.

- [ ] **Step 4: Full regression and Draft PR**

Commit: `feat: add generation 1 records and administration views`.

### Task G1-5: Adaptive layout, GL100E manifest and native DTools evidence

**Files:**
- Create: `src/hoofcare/physical/gen1_layout.py`
- Create: `dtools/gl100e/manifest.json`
- Create: `dtools/gl100e/README.md`
- Create: `scripts/check_gen1_dtools_manifest.py`
- Test: `tests/test_gen1_gl100e_layout.py`
- Test: `tests/test_gen1_dtools_manifest.py`

**Interfaces:**
- Consumes: semantic route/widget IDs from G1-1..G1-4.
- Produces: `AdaptiveRegion`, `TouchTarget`, `Gl100eProfile.default()`, validated JSON manifest and exact native-artifact evidence record.

- [ ] **Step 1: Write geometry and manifest RED**

```python
def test_every_gl100e_target_fits_and_is_at_least_64_px():
    profile = Gl100eProfile.default()
    for screen in profile.screens:
        self.assertTrue(screen.within_canvas())
        self.assertFalse(screen.has_overlaps())
        self.assertTrue(all(target.width >= 64 and target.height >= 64 for target in screen.targets))
```

The manifest RED asserts exact route coverage and fails because the files do not exist. Push only the tests.

- [ ] **Step 2: Implement profile and manifest validator**

The validator rejects duplicate IDs, unknown routes, missing Polish labels,
untyped bindings, more than four primary actions, write bindings without an
approved use case, geometry outside `1024×600` and any `KVK`, `PLC`,
`HYDRAULIC`, `RFID_LIVE`, `CAMERA_LIVE` binding.

- [ ] **Step 3: Create native DTools project or stop truthfully**

Use the installed Kinco DTools toolchain to create the exact GL100E project
from the validated manifest. Save tool-generated files under `dtools/gl100e/`,
record the exact relative artifact path, DTools version, SHA-256 and UTC build
timestamp in `dtools/gl100e/README.md`, and run offline build/compile.

If DTools is unavailable or the project cannot compile with zero errors, stop
the increment as `BLOCKED / NATIVE_DTOOLS_ARTIFACT_REQUIRED`; do not create a
substitute extension, encoded text or claimed artifact.

- [ ] **Step 4: Verify repository and tool evidence**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest tests.test_gen1_gl100e_layout tests.test_gen1_dtools_manifest -v
python scripts/check_gen1_dtools_manifest.py
```

Compare the native artifact hash with README and preserve the complete offline compile log. No upload or physical PASS is allowed.

- [ ] **Step 5: Full regression and Draft PR**

Commit: `feat: realize generation 1 GL100E DTools profile`.

### Task G1-6: Restart integration, requirement traceability and bounded closure

**Files:**
- Create: `tests/test_gen1_complete_workflow_integration.py`
- Modify: `docs/traceability/HC-REQ-TRACE-001_Requirement_Level_Matrix_v0.1.md`
- Modify: `docs/traceability/HC-TRACE-001_Traceability.md`
- Modify: `project_context/CURRENT_STATE.md`
- Create after verified implementation: `docs/closure/HC-REQ-HC-003-G1-CLOSURE-001.md`

**Interfaces:**
- Consumes: all public G1 projections, canonical store/service and deterministic PDF renderer.
- Produces: one restart-safe synthetic workflow and requirement-level evidence for every `REQ-HC-G1-*` ID.

- [ ] **Step 1: Write and publish final integration RED**

```python
def test_complete_generation_1_workflow_survives_restart():
    result = run_complete_gen1_synthetic_scenario()
    self.assertEqual(result.completed_cows, 2)
    self.assertEqual(result.total_label, "RAZEM NETTO: 122,00 zł")
    self.assertTrue(result.prices_hidden_during_treatment)
    self.assertTrue(result.owner_zone_expired_after_idle)
    self.assertEqual(result.dtools_manifest_status, "VALIDATED_OFFLINE")
```

Expected RED: missing scenario assertion before orchestration exists. Push the test-only checkpoint.

- [ ] **Step 2: Implement the smallest orchestration through public seams**

Exercise open → price correction → treatment → durable completion → material
usage → restart → statistics → close → PDF → owner unlock/expiry → route
recovery. Do not bypass services or read private fields.

- [ ] **Step 3: Map every requirement honestly**

Mark semantic/synthetic/offline requirements `IMPLEMENTED FOR AUTHORIZED G1
SCOPE` only with direct evidence. Keep physical upload, real panel touch,
edge-host transport and HW-A3 `BLOCKED` or `PARTIAL`.

- [ ] **Step 4: Run final verification**

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests -q
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/run_coverage.py
PYTHONDONTWRITEBYTECODE=1 python -m compileall -q src tests scripts
python scripts/check_foundation.py
python scripts/check_semantic_governance.py
python scripts/check_gen1_dtools_manifest.py
```

Expected: all commands exit 0; exact remote head/tree match the tested tree.

- [ ] **Step 5: Publish closure-ready Draft PR**

Commit: `test: verify complete generation 1 HMI workflow`.

Closure requires separate exact-head approval, controlled merge and Repository Verification. Physical product acceptance remains outside this plan.
