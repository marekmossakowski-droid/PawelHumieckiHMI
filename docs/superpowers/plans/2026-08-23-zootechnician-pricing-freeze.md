# Zootechnician Pricing Access and Freeze Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dodać lokalny, synthetic/test-only, audytowany mechanizm korekty cen przez Pawła przed pierwszą ukończoną krową oraz zamrożenie cen po jej trwałym przypisaniu.

**Architecture:** `Job` pozostaje agregatem i jedynym miejscem reguły korekty oraz zamrożenia. `LocalJobStore` zapisuje pełną historię snapshotów i audytu w jednym integralnościowym envelope, `JobService` zapewnia atomową operację aplikacyjną, a HMI konsumuje semantyczny view model niezależny od rozdzielczości. GL100E `1024×600` pozostaje osobnym profilem prezentacji.

**Tech Stack:** Python 3.11+, standard library (`dataclasses`, `datetime`, `enum`, `json`, `pathlib`, `unittest`), istniejący SHA-256/atomic replace persistence pattern.

**Spec:** `docs/superpowers/specs/2026-08-23-zootechnician-pricing-freeze-design.md`

## Global Constraints

- Runtime może rozpocząć się wyłącznie po `IA-HC-007-A1 = APPROVED / ACTIVE` i Repository Verification rekordu aktywacji.
- Każdy task wymaga zdalnego clean assertion RED przed zmianą kodu produkcyjnego.
- Wszystkie dane i fixture'y pozostają synthetic/test-only i używają prefiksu `TEST-`.
- Kwoty są całkowitą liczbą groszy; binary `float` jest zabroniony.
- Korekta jest dozwolona wyłącznie dla `JobState.OPEN` z `completed_cows == 0`.
- Pierwsza trwała sesja `COMPLETED` nieodwracalnie zamraża ceny.
- Korekty zamkniętego rozliczenia i korekty po pierwszej krowie są wyłączone.
- Brak klientów Generacji 2, sieci/chmury, realnych danych, device access, KVK I/O, sterowania, hydrauliki, PLC/safety mutation, fakturowania, płatności, deploymentu, signing, release i public distribution.

---

## File Structure

| Path | Responsibility |
|---|---|
| `src/hoofcare/domain/jobs.py` | wersje snapshotu, rekord audytu, korekta i punkt zamrożenia |
| `src/hoofcare/persistence/job_store.py` | integralnościowy round-trip historii cen i audytu |
| `src/hoofcare/application/job_service.py` | trwała aplikacyjna operacja korekty |
| `src/hoofcare/hmi/job_menu.py` | semantyczne view models widoczności cen i uprawnień Pawła |
| `src/hoofcare/physical/job_layout.py` | profil GL100E dla ekranów zlecenia bez logiki finansowej |
| `tests/test_job_price_correction.py` | domenowy RED/GREEN korekty, retry, konflikt i freeze |
| `tests/test_job_price_correction_persistence.py` | round-trip, corruption i atomic replace |
| `tests/test_job_price_correction_service.py` | operacja aplikacyjna i błąd trwałości |
| `tests/test_job_menu.py` | ceny widoczne/ukryte i brak wymogu PIN-u |
| `tests/test_job_price_correction_integration.py` | pełny przebieg z restartem |

### Task 1: Versioned Pricing Snapshot and Domain Audit

**Files:**
- Modify: `src/hoofcare/domain/jobs.py`
- Create: `tests/test_job_price_correction.py`

**Interfaces:**
- Produces: `PriceField(str, Enum)`, `PriceCorrection`, `Job.correct_price(...) -> Job`, `Job.pricing_frozen -> bool`.
- `Job.correct_price(event_id: str, operator_id: str, corrected_at: datetime, reason: str, field: PriceField, new_value_grosz: int, material_code: str | None = None) -> Job`.

- [ ] **Step 1: Write the clean RED tests**

```python
from datetime import datetime, timezone
import importlib
import unittest

from tests.job_fixtures import completed_session, open_job_fixture


class JobPriceCorrectionTests(unittest.TestCase):
    def setUp(self):
        module = importlib.import_module("hoofcare.domain.jobs")
        self.assertTrue(hasattr(module, "PriceField"), "PriceField must exist")
        self.PriceField = module.PriceField

    def test_pawel_corrects_cow_price_before_first_completed_cow(self):
        job = open_job_fixture()
        changed = job.correct_price(
            "TEST-CORRECTION-1", "TEST-PAWEL",
            datetime(2026, 8, 23, 8, 30, tzinfo=timezone.utc),
            "Błąd przy wpisywaniu stawki", self.PriceField.COW_UNIT_PRICE, 3600,
        )
        self.assertEqual(changed.pricing.cow_unit_price_grosz, 3600)
        self.assertEqual(changed.pricing_version, 2)
        self.assertEqual(changed.price_corrections[0].old_value_grosz, 3500)

    def test_identical_retry_is_idempotent_and_conflict_fails_closed(self):
        job = open_job_fixture()
        args = ("TEST-CORRECTION-1", "TEST-PAWEL", datetime(2026, 8, 23, 8, 30, tzinfo=timezone.utc), "Literówka", self.PriceField.COW_UNIT_PRICE, 3600)
        once = job.correct_price(*args)
        self.assertEqual(once.correct_price(*args), once)
        with self.assertRaisesRegex(ValueError, "correction event payload conflict"):
            once.correct_price(*args[:-1], 3700)

    def test_first_completed_cow_freezes_all_prices(self):
        frozen = open_job_fixture().record_completed_session(
            completed_session("TEST-COW-1", "TEST-SESSION-1"), "TEST-COMPLETE-1"
        )
        self.assertTrue(frozen.pricing_frozen)
        with self.assertRaisesRegex(ValueError, "pricing is frozen"):
            frozen.correct_price(
                "TEST-CORRECTION-2", "TEST-PAWEL",
                datetime(2026, 8, 23, 9, tzinfo=timezone.utc),
                "Zmiana po pracy", self.PriceField.COW_UNIT_PRICE, 3700,
            )
```

- [ ] **Step 2: Run and preserve RED remotely**

Run: `PYTHONPATH=src python -m unittest tests.test_job_price_correction -v`

Expected: controlled assertion failures for absent symbols/methods; zero import or discovery errors. Commit and publish only the test file as the remote RED checkpoint.

- [ ] **Step 3: Implement immutable domain types and correction**

```python
class PriceField(str, Enum):
    COW_UNIT_PRICE = "COW_UNIT_PRICE"
    MATERIAL_UNIT_PRICE = "MATERIAL_UNIT_PRICE"


@dataclass(frozen=True)
class PriceCorrection:
    event_id: str
    operator_id: str
    corrected_at: datetime
    reason: str
    field: PriceField
    material_code: str | None
    old_value_grosz: int
    new_value_grosz: int


@property
def pricing_frozen(self) -> bool:
    return bool(self.completed_links)
```

Add `pricing_version: int = 1` and `price_corrections: tuple[PriceCorrection, ...] = ()` to `Job`. `correct_price()` MUST validate aware time, non-empty identifiers/reason, exact integer grosze, field/material consistency, `state is OPEN`, `completed_cows == 0`, identical retry, and conflicting retry. Use `replace()` to create the updated `JobPricingSnapshot`, increment `pricing_version`, and append one audit record.

- [ ] **Step 4: Run GREEN and full regression**

Run: `PYTHONPATH=src python -m unittest tests.test_job_price_correction -v`

Run: `PYTHONPATH=src python -m unittest discover -s tests -q`

Expected: targeted tests and full suite PASS.

- [ ] **Step 5: Commit GREEN**

```bash
git add src/hoofcare/domain/jobs.py tests/test_job_price_correction.py
git commit -m "feat(jobs): add audited pre-work price correction"
```

### Task 2: Durable Pricing History

**Files:**
- Modify: `src/hoofcare/persistence/job_store.py`
- Create: `tests/test_job_price_correction_persistence.py`

**Interfaces:**
- Consumes: `Job.pricing_version`, `Job.price_corrections`, `PriceCorrection`.
- Produces: schema version `2` persistence with exact round-trip and fail-closed validation.

- [ ] **Step 1: Write persistence RED**

```python
from datetime import datetime, timezone
from tests.job_fixtures import open_job_fixture


def corrected_open_job_fixture():
    from hoofcare.domain.jobs import PriceField
    return open_job_fixture().correct_price(
        "TEST-CORRECTION-1", "TEST-PAWEL",
        datetime(2026, 8, 23, 8, 30, tzinfo=timezone.utc),
        "Błąd stawki", PriceField.COW_UNIT_PRICE, 3600,
    )


def test_corrected_job_round_trip_preserves_version_and_audit(self):
    job = corrected_open_job_fixture()
    with tempfile.TemporaryDirectory() as tmp:
        store = LocalJobStore(Path(tmp))
        store.save(job)
        self.assertEqual(store.load(job.job_id), job)


def test_failed_replace_preserves_previous_pricing_version(self):
    with tempfile.TemporaryDirectory() as tmp:
        store = LocalJobStore(Path(tmp))
        store.save(open_job_fixture())
        with mock.patch("hoofcare.persistence.job_store.os.replace", side_effect=OSError("TEST-FAIL")):
            with self.assertRaises(OSError):
                store.save(corrected_open_job_fixture())
        self.assertEqual(store.load("TEST-JOB-1").pricing_version, 1)
```

- [ ] **Step 2: Run and preserve RED remotely**

Run: `PYTHONPATH=src python -m unittest tests.test_job_price_correction_persistence -v`

Expected: equality/field assertion failures because schema v1 omits the new history; zero setup errors.

- [ ] **Step 3: Implement schema v2 serialization**

Set `SNAPSHOT_SCHEMA_VERSION = 2`. Serialize `pricing_version` and every correction field. Deserialize with exact type checks, aware timestamps, sequential positive version, non-empty reason, valid `PriceField`, integer values and audit length equal to `pricing_version - 1`. Reconstruct `Job` with the persisted active pricing and immutable audit tuple. Any mismatch MUST surface as `ValueError("invalid persisted job: ...")`.

- [ ] **Step 4: Run targeted and broad GREEN**

Run: `PYTHONPATH=src python -m unittest tests.test_job_price_correction_persistence tests.test_job_persistence -v`

Run: `PYTHONPATH=src python scripts/run_coverage.py`

Expected: PASS with schema corruption and atomic replace negatives covered.

- [ ] **Step 5: Commit**

```bash
git add src/hoofcare/persistence/job_store.py tests/test_job_price_correction_persistence.py tests/job_fixtures.py
git commit -m "feat(persistence): preserve audited pricing history"
```

### Task 3: Application Correction Use Case

**Files:**
- Modify: `src/hoofcare/application/job_service.py`
- Create: `tests/test_job_price_correction_service.py`

**Interfaces:**
- Produces: `JobService.correct_price(job_id: str, event_id: str, operator_id: str, corrected_at: datetime, reason: str, field: PriceField, new_value_grosz: int, material_code: str | None = None) -> Job`.

- [ ] **Step 1: Write service RED**

```python
def service_fixture(root: Path):
    jobs = LocalJobStore(root / "jobs")
    sessions = LocalSessionStore(root / "sessions")
    jobs.save(open_job_fixture())
    return JobService(jobs, sessions), jobs


def test_service_persists_correction_before_returning_success(self):
    with tempfile.TemporaryDirectory() as tmp:
        service, jobs = service_fixture(Path(tmp))
        changed = service.correct_price(
            "TEST-JOB-1", "TEST-CORRECTION-1", "TEST-PAWEL", CORRECTED_AT,
            "Błąd stawki", PriceField.COW_UNIT_PRICE, 3600,
        )
        self.assertEqual(jobs.load("TEST-JOB-1"), changed)


def test_storage_failure_does_not_change_durable_job(self):
    with tempfile.TemporaryDirectory() as tmp:
        service, jobs = service_fixture(Path(tmp))
        with mock.patch.object(jobs, "save", side_effect=OSError("TEST-FAIL")):
            with self.assertRaises(OSError):
                service.correct_price(
                    "TEST-JOB-1", "TEST-CORRECTION-1", "TEST-PAWEL", CORRECTED_AT,
                    "Błąd stawki", PriceField.COW_UNIT_PRICE, 3600,
                )
        self.assertEqual(jobs.load("TEST-JOB-1").pricing_version, 1)
```

- [ ] **Step 2: Run and preserve RED remotely**

Run: `PYTHONPATH=src python -m unittest tests.test_job_price_correction_service -v`

Expected: controlled missing-method assertion failure.

- [ ] **Step 3: Implement minimal orchestration**

Load the job, call its exact `correct_price()` interface, persist through `LocalJobStore.save()`, then return the persisted value. Do not catch storage errors and do not add fallback values.

- [ ] **Step 4: Verify**

Run: `PYTHONPATH=src python -m unittest tests.test_job_price_correction_service tests.test_job_persistence -v`

Run: `PYTHONPATH=src python -m unittest discover -s tests -q`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/hoofcare/application/job_service.py tests/test_job_price_correction_service.py
git commit -m "feat(jobs): expose durable price correction use case"
```

### Task 4: Semantic HMI and GL100E Profile

**Files:**
- Create: `src/hoofcare/hmi/job_menu.py`
- Create: `src/hoofcare/physical/job_layout.py`
- Create: `tests/test_job_menu.py`

**Interfaces:**
- Produces: `JobScreenStage`, `JobMenuView`, `job_menu_view(job: Job, stage: JobScreenStage) -> JobMenuView`, `Gl100eJobLayout.default()`.

- [ ] **Step 1: Write HMI RED**

```python
def test_pawel_sees_prices_without_owner_pin_at_open_and_correction(self):
    job = open_job_fixture()
    self.assertTrue(job_menu_view(job, JobScreenStage.OPEN).prices_visible)
    self.assertTrue(job_menu_view(job, JobScreenStage.PRICE_CORRECTION).price_edit_allowed)


def test_work_screen_hides_prices_and_first_cow_removes_edit_action(self):
    job = open_job_fixture()
    self.assertFalse(job_menu_view(job, JobScreenStage.TREATMENT).prices_visible)
    frozen = job.record_completed_session(completed_session("TEST-COW-1", "TEST-SESSION-1"), "TEST-COMPLETE-1")
    self.assertFalse(job_menu_view(frozen, JobScreenStage.SUMMARY).price_edit_allowed)


def test_gl100e_profile_keeps_touch_targets_at_least_64_pixels(self):
    layout = Gl100eJobLayout.default()
    self.assertEqual((layout.width_px, layout.height_px), (1024, 600))
    self.assertTrue(all(target.width >= 64 and target.height >= 64 for target in layout.touch_targets))
```

- [ ] **Step 2: Run and preserve RED remotely**

Run: `PYTHONPATH=src python -m unittest tests.test_job_menu -v`

Expected: controlled assertion failures for missing modules/symbols.

- [ ] **Step 3: Implement presentation-only models**

`JobMenuView` MUST contain semantic flags and labels only: `prices_visible`, `price_edit_allowed`, `cow_count`, `material_quantities`, `actions`. It MUST derive monetary visibility from stage and edit permission from `not job.pricing_frozen`; it MUST NOT calculate totals or require owner PIN. `Gl100eJobLayout` MUST contain only geometry/touch targets and import no domain or application module.

- [ ] **Step 4: Verify geometry and boundaries**

Run: `PYTHONPATH=src python -m unittest tests.test_job_menu tests.test_physical_hmi_layout tests.test_r2_hmi_navigation_geometry -v`

Expected: PASS; existing GL100E contracts remain unchanged.

- [ ] **Step 5: Commit**

```bash
git add src/hoofcare/hmi/job_menu.py src/hoofcare/physical/job_layout.py tests/test_job_menu.py
git commit -m "feat(hmi): add zootechnician pricing views"
```

### Task 5: Restart Integration and Traceability

**Files:**
- Create: `tests/test_job_price_correction_integration.py`
- Modify: `docs/traceability/HC-REQ-TRACE-001_Requirement_Level_Matrix_v0.1.md`
- Modify: `docs/traceability/HC-TRACE-001_Traceability.md`

**Interfaces:**
- Consumes all Task 1–4 public interfaces.
- Produces end-to-end evidence for every `REQ-HC-002-A1` requirement.

- [ ] **Step 1: Write integration RED before integration-only code changes**

```python
def durable_fixture(root: Path):
    jobs = LocalJobStore(root / "jobs")
    sessions = LocalSessionStore(root / "sessions")
    return jobs, sessions, JobService(jobs, sessions)


def test_open_correct_restart_complete_freeze_and_close(self):
    with tempfile.TemporaryDirectory() as tmp:
        jobs, sessions, service = durable_fixture(Path(tmp))
        jobs.save(open_job_fixture())
        service.correct_price(
            "TEST-JOB-1", "TEST-CORRECTION-1", "TEST-PAWEL", CORRECTED_AT,
            "Błąd stawki", PriceField.COW_UNIT_PRICE, 3600,
        )
        restarted = JobService(LocalJobStore(jobs.root), LocalSessionStore(sessions.root))
        completed = restarted.commit_completed_session(
            "TEST-JOB-1", completed_session("TEST-COW-1", "TEST-SESSION-1"), "TEST-COMPLETE-1"
        )
        self.assertTrue(completed.pricing_frozen)
        with self.assertRaisesRegex(ValueError, "pricing is frozen"):
            restarted.correct_price(
                "TEST-JOB-1", "TEST-CORRECTION-2", "TEST-PAWEL", LATER,
                "Po rozpoczęciu", PriceField.COW_UNIT_PRICE, 3700,
            )
        closed = jobs.load("TEST-JOB-1").close(CLOSED, ())
        self.assertEqual(closed.settlement().total_net_grosz, 3600)
```

- [ ] **Step 2: Run integration evidence**

Run: `PYTHONPATH=src python -m unittest tests.test_job_price_correction_integration -v`

Expected before final wiring: FAIL only at the first unmet integration assertion; no environment error.

- [ ] **Step 3: Add only missing fixture/wiring and update traceability**

Keep durable roots explicit, reload `LocalJobStore` and `LocalSessionStore`, and map `REQ-HC-JOB-ROLE-A1-001..003` plus `REQ-HC-JOB-PRICE-A1-001..004` to exact test names. Do not mark Generation 2, real-data, deployment or closed-settlement correction requirements implemented.

- [ ] **Step 4: Run final verification**

Run: `PYTHONPATH=src python -m unittest discover -s tests -q`

Run: `PYTHONPATH=src python scripts/run_coverage.py`

Run: `python -m compileall -q src tests`

Run: `python scripts/check_foundation.py && python scripts/check_semantic_governance.py && git diff --check`

Expected: all commands exit `0`.

- [ ] **Step 5: Commit final evidence**

```bash
git add tests/test_job_price_correction_integration.py tests/job_fixtures.py docs/traceability/HC-REQ-TRACE-001_Requirement_Level_Matrix_v0.1.md docs/traceability/HC-TRACE-001_Traceability.md
git commit -m "test(jobs): verify pricing correction freeze flow"
```

## Execution Gate

Do not execute this plan until a canonical activation record establishes
`IA-HC-007-A1 = APPROVED / ACTIVE` after controlled merge and Repository
Verification. Every task remains a separate Draft PR exact-head approval gate.
