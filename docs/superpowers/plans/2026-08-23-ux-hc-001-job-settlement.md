# UX-HC-001 Job Settlement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Zbudować lokalny, synthetic/test-only moduł zleceń z rolami operator/właściciel, trwałym liczeniem krów i materiałów, snapshotem cen oraz końcowym rozliczeniem netto w PLN.

**Architecture:** Nowy agregat `Job` pozostaje oddzielony od istniejącego agregatu `Session`; warstwa aplikacyjna wiąże je wyłącznie stabilnymi identyfikatorami i zapisuje ukończoną sesję przed aktualizacją zlecenia. Cennik zlecenia jest snapshotem domenowym, statystyki są pochodne z trwałych zleceń, a HMI prezentuje role-aware view models bez kanonicznych obliczeń finansowych.

**Tech Stack:** Python 3.11+, standard library (`dataclasses`, `decimal`, `enum`, `json`, `pathlib`, `unittest`), obecny lokalny persistence pattern z SHA-256 i atomic replace, obecny minimalny generator PDF.

**Spec:** `docs/design/UX-HC-001_Role_Based_Menu_Job_Settlement_and_Statistics_v0.1.md`

## Global Constraints

- Implementacja może rozpocząć się wyłącznie po `IA-HC-007 = APPROVED / ACTIVE` i Repository Verification.
- Każdy inkrement wymaga zdalnego clean assertion RED przed kodem produkcyjnym.
- Wszystkie gospodarstwa, operatorzy, zwierzęta, ceny i materiały są synthetic/test-only.
- Kwoty PLN są całkowitą liczbą groszy; pieniądze nie używają binarnego `float`.
- Ilości materiałów używają `Decimal` i precyzji zero–trzy miejsca.
- Każda pozycja materiałowa używa `ROUND_HALF_UP` do pełnego grosza.
- Standardowe materiały są zawarte w stawce za krowę i nie są doliczane osobno.
- Licznik krów pochodzi z unikalnych, trwale zapisanych sesji `COMPLETED`.
- Zamknięte snapshoty nie są przeliczane po zmianie katalogu.
- Brak realnych danych, live RFID, KVK I/O, machine bus, commands/writes/configuration/actuation, hydrauliki, PLC/safety mutation, network/cloud, fakturowania, płatności, deployment, signing, release i public distribution.

---

## File Structure

| Path | Responsibility |
|---|---|
| `src/hoofcare/domain/jobs.py` | pieniądze, stawki, materiał lokalny, agregat zlecenia, kalkulacja i lifecycle |
| `src/hoofcare/persistence/job_store.py` | atomowy, integralnościowy zapis/odczyt niezmiennych snapshotów zleceń |
| `src/hoofcare/application/job_service.py` | kolejność trwałego zapisu sesja → zlecenie i operacje aplikacyjne |
| `src/hoofcare/application/job_statistics.py` | pochodne statystyki operatora i właściciela |
| `src/hoofcare/hmi/job_menu.py` | role-aware menu, ekranowe view models i widoczność cen |
| `src/hoofcare/hmi/owner_access.py` | lokalna, nieprodukcyjna bramka 6-cyfrowego PIN-u z timeoutem |
| `src/hoofcare/reporting/pdf.py` | współdzielony minimalny renderer PDF z linii tekstu |
| `src/hoofcare/reporting/settlement.py` | dokument rozliczenia z zamkniętego zlecenia |
| `tests/test_job_pricing.py` | pieniądze, precyzja, snapshot i materiały lokalne |
| `tests/test_job_lifecycle.py` | liczenie krów, materiały, idempotency i blokady zamknięcia |
| `tests/job_fixtures.py` | deterministyczne, jawnie syntetyczne fixture’y współdzielone od Task 2 |
| `tests/test_job_persistence.py` | round-trip, integralność i atomowość snapshotów |
| `tests/test_job_menu.py` | role, ceny, geometria i brak sterowania maszyną |
| `tests/test_job_statistics_reporting.py` | agregacje, netto i PDF |
| `tests/test_job_settlement_integration.py` | pełny syntetyczny przebieg z restartem |

## Requirement Coverage

| Requirement group | Primary evidence task |
|---|---|
| `REQ-HC-JOB-ROLE-001..003` | Task 4: distinct role menus, six-digit owner PIN, timeout and owner lock |
| `REQ-HC-JOB-OPEN-001..003` | Tasks 1–2: required job context, immutable pricing snapshot, cow subtotal only |
| `REQ-HC-JOB-MAT-001..003` | Tasks 1–3: active material definition, job-local extension, durable idempotent usage |
| `REQ-HC-JOB-COUNT-001..003` | Tasks 2–5: unique completed sessions, durable ordering, daily/farm filters |
| `REQ-HC-JOB-PRICE-001..003` | Tasks 1, 4 and 6: visibility policy, integer grosze, Decimal and exact integrated total |
| `REQ-HC-JOB-CLOSE-001..003` | Tasks 2, 3, 5 and 6: fail-closed closure, immutable persisted settlement and PDF |
| `REQ-HC-JOB-STAT-001..003` | Task 5: role scope plus operator/farm/date/status derived filters |
| `REQ-HC-JOB-SAF-001`, `DATA-001`, `FIN-001` | Tasks 4–6: prohibited actions, explicit `TEST-` fixtures and not-an-invoice marker |

---

### Task 1: Money, Material Rates and Pricing Snapshot

**Files:**
- Create: `src/hoofcare/domain/jobs.py`
- Create: `tests/test_job_pricing.py`

**Interfaces:**
- Produces: `MaterialRate` and `JobPricingSnapshot`.
- `MaterialRate.line_total_grosz(quantity: Decimal) -> int` performs exact validation and `ROUND_HALF_UP`.
- `JobPricingSnapshot.with_local_material(rate: MaterialRate) -> JobPricingSnapshot` returns a new snapshot.

- [ ] **Step 1: Write the failing pricing tests**

```python
from decimal import Decimal
import importlib
import unittest


def require_symbol(case: unittest.TestCase, module_name: str, symbol: str):
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        case.fail(f"{module_name} must exist")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


class JobPricingTests(unittest.TestCase):
    def setUp(self):
        self.MaterialRate = require_symbol(self, "hoofcare.domain.jobs", "MaterialRate")
        self.JobPricingSnapshot = require_symbol(self, "hoofcare.domain.jobs", "JobPricingSnapshot")

    def test_material_line_uses_decimal_half_up_to_grosz(self):
        rate = self.MaterialRate("BLOCK", "Klocek", "szt.", 1855, 2, False)
        self.assertEqual(rate.line_total_grosz(Decimal("1.235")), 2291)

    def test_standard_scope_is_only_the_cow_rate(self):
        snapshot = self.JobPricingSnapshot(cow_unit_price_grosz=3500, additional_materials=())
        self.assertEqual(snapshot.cow_subtotal_grosz(40), 140000)
        self.assertEqual(snapshot.additional_materials, ())

    def test_local_material_extends_only_the_job_snapshot(self):
        original = self.JobPricingSnapshot(3500, ())
        local = self.MaterialRate("LOCAL-1", "Żel ochronny", "ml", 25, 1, True, True)
        extended = original.with_local_material(local)
        self.assertEqual(original.additional_materials, ())
        self.assertEqual(extended.additional_materials, (local,))

    def test_invalid_money_and_quantity_fail_closed(self):
        with self.assertRaises(ValueError):
            self.JobPricingSnapshot(-1, ())
        rate = self.MaterialRate("BLOCK", "Klocek", "szt.", 1855, 0, False, True)
        with self.assertRaises(ValueError):
            rate.line_total_grosz(Decimal("0.5"))

    def test_inactive_material_cannot_enter_a_new_snapshot(self):
        inactive = self.MaterialRate("OLD", "Wycofany", "szt.", 100, 0, False, False)
        with self.assertRaises(ValueError):
            self.JobPricingSnapshot(3500, (inactive,))
```

- [ ] **Step 2: Run RED and preserve the remote RED commit**

Run: `PYTHONPATH=src python -m unittest tests.test_job_pricing -v`

Expected: `require_symbol()` converts the absent module/symbol into a controlled `AssertionError`; zero import or discovery errors. Preserve this exact clean RED remotely before creating `jobs.py`.

- [ ] **Step 3: Implement exact pricing primitives**

```python
from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal, ROUND_HALF_UP


def _text(name: str, value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{name} must be non-empty")
    return normalized


@dataclass(frozen=True)
class MaterialRate:
    code: str
    label: str
    unit: str
    unit_price_grosz: int
    quantity_scale: int
    job_local: bool = False
    active: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _text("material code", self.code))
        object.__setattr__(self, "label", _text("material label", self.label))
        object.__setattr__(self, "unit", _text("material unit", self.unit))
        if type(self.unit_price_grosz) is not int or self.unit_price_grosz < 0:
            raise ValueError("unit price must be non-negative integer grosze")
        if self.quantity_scale not in range(4):
            raise ValueError("quantity scale must be between zero and three")
        if type(self.active) is not bool:
            raise ValueError("active must be boolean")

    def normalize_quantity(self, quantity: Decimal) -> Decimal:
        if not isinstance(quantity, Decimal) or quantity <= 0:
            raise ValueError("quantity must be a positive Decimal")
        quantum = Decimal(1).scaleb(-self.quantity_scale)
        normalized = quantity.quantize(quantum)
        if normalized != quantity:
            raise ValueError("quantity exceeds material precision")
        return normalized

    def line_total_grosz(self, quantity: Decimal) -> int:
        normalized = self.normalize_quantity(quantity)
        amount = normalized * Decimal(self.unit_price_grosz)
        return int(amount.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


@dataclass(frozen=True)
class JobPricingSnapshot:
    cow_unit_price_grosz: int
    additional_materials: tuple[MaterialRate, ...]

    def __post_init__(self) -> None:
        if type(self.cow_unit_price_grosz) is not int or self.cow_unit_price_grosz < 0:
            raise ValueError("cow price must be non-negative integer grosze")
        codes = tuple(rate.code for rate in self.additional_materials)
        if len(codes) != len(set(codes)):
            raise ValueError("material codes must be unique within job pricing")
        if any(not rate.active for rate in self.additional_materials):
            raise ValueError("job pricing accepts only active materials")

    def cow_subtotal_grosz(self, completed_cows: int) -> int:
        if type(completed_cows) is not int or completed_cows < 0:
            raise ValueError("completed cows must be a non-negative integer")
        return completed_cows * self.cow_unit_price_grosz

    def rate(self, code: str) -> MaterialRate:
        for item in self.additional_materials:
            if item.code == code:
                return item
        raise KeyError(code)

    def with_local_material(self, rate: MaterialRate) -> "JobPricingSnapshot":
        if not rate.job_local or not rate.active:
            raise ValueError("job-local extension requires an active job_local material")
        return replace(self, additional_materials=self.additional_materials + (rate,))
```

- [ ] **Step 4: Run GREEN and regression**

Run: `PYTHONPATH=src python -m unittest tests.test_job_pricing -v`

Expected: 5 tests PASS.

Run: `PYTHONPATH=src python -m unittest discover -s tests -q`

Expected: all existing and new tests PASS.

- [ ] **Step 5: Commit GREEN**

```bash
git add src/hoofcare/domain/jobs.py tests/test_job_pricing.py
git commit -m "feat(jobs): add deterministic pricing snapshot"
```

---

### Task 2: Job Lifecycle, Idempotent Counters and Settlement

**Files:**
- Modify: `src/hoofcare/domain/jobs.py`
- Create: `tests/test_job_lifecycle.py`
- Create: `tests/job_fixtures.py`

**Interfaces:**
- Consumes: `JobPricingSnapshot`, `MaterialRate` from Task 1 and `Session` from `hoofcare.domain.session`.
- Produces: `CompletedSessionLink`, `MaterialUsage`, `SettlementLine`, `Settlement`, `Job.open(...)`, `Job.record_completed_session(session, event_id)`, `Job.record_material(...)`, `Job.add_local_material(...)`, `Job.close(...)`, and `Job.settlement()`.
- `completed_cows` is derived from unique committed session links and is never assigned directly.

- [ ] **Step 1: Write clean failing lifecycle tests**

```python
from datetime import datetime, timezone
from decimal import Decimal
import importlib
import unittest

from hoofcare.domain.session import AnimalIdentityResolution, Session, SessionEvent, SessionEventType


def require_symbol(case: unittest.TestCase, symbol: str):
    module = importlib.import_module("hoofcare.domain.jobs")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


def completed_session(animal_id: str) -> Session:
    session = Session.new().apply(SessionEvent("identity", SessionEventType.IDENTITY_RESOLVED, AnimalIdentityResolution.confirmed(animal_id)))
    return session.apply(SessionEvent("complete", SessionEventType.COMPLETE))


class JobLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.Job = require_symbol(self, "Job")
        self.JobState = require_symbol(self, "JobState")
        self.MaterialRate = require_symbol(self, "MaterialRate")
        self.JobPricingSnapshot = require_symbol(self, "JobPricingSnapshot")
        rates = (self.MaterialRate("BLOCK", "Klocek", "szt.", 1800, 0),)
        self.job = self.Job.open("TEST-JOB-1", "TEST-FARM-1", "operator-pawel", datetime(2026, 8, 23, tzinfo=timezone.utc), self.JobPricingSnapshot(3500, rates), 40)

    def test_completed_session_counts_once_under_retry(self):
        session = completed_session("TEST-COW-1")
        once = self.job.record_completed_session(session, "event-1")
        twice = once.record_completed_session(session, "event-1")
        self.assertEqual(twice.completed_cows, 1)

    def test_reused_completion_event_with_different_session_fails_closed(self):
        once = self.job.record_completed_session(completed_session("TEST-COW-1"), "event-1")
        with self.assertRaises(ValueError):
            once.record_completed_session(completed_session("TEST-COW-2"), "event-1")

    def test_draft_or_cancelled_session_does_not_count(self):
        with self.assertRaises(ValueError):
            self.job.record_completed_session(Session.new(), "event-2")

    def test_extra_material_is_billed_once_under_retry(self):
        counted = self.job.record_completed_session(completed_session("TEST-COW-1"), "event-1")
        used = counted.record_material("material-1", counted.completed_session_ids[0], "BLOCK", Decimal("2"))
        retried = used.record_material("material-1", counted.completed_session_ids[0], "BLOCK", Decimal("2"))
        self.assertEqual(retried.material_total_grosz, 3600)

    def test_reused_material_event_with_different_quantity_fails_closed(self):
        counted = self.job.record_completed_session(completed_session("TEST-COW-1"), "event-1")
        used = counted.record_material("material-1", counted.completed_session_ids[0], "BLOCK", Decimal("1"))
        with self.assertRaises(ValueError):
            used.record_material("material-1", counted.completed_session_ids[0], "BLOCK", Decimal("2"))

    def test_material_cannot_reference_a_session_outside_the_job(self):
        with self.assertRaises(ValueError):
            self.job.record_material("material-1", "UNKNOWN-SESSION", "BLOCK", Decimal("1"))

    def test_local_material_can_be_added_only_while_job_is_open(self):
        local = self.MaterialRate("LOCAL-1", "Żel", "ml", 25, 1, True)
        extended = self.job.add_local_material(local)
        self.assertEqual(extended.pricing.rate("LOCAL-1"), local)
        closed = extended.close(datetime(2026, 8, 23, 18, tzinfo=timezone.utc), ())
        with self.assertRaises(ValueError):
            closed.add_local_material(self.MaterialRate("LOCAL-2", "Pianka", "ml", 30, 1, True))

    def test_close_requires_no_unresolved_session_and_freezes_total(self):
        complete = self.job.record_completed_session(completed_session("TEST-COW-1"), "event-1")
        closed = complete.close(datetime(2026, 8, 23, 18, tzinfo=timezone.utc), unresolved_session_ids=())
        self.assertEqual(closed.state, self.JobState.CLOSED)
        self.assertEqual(closed.settlement().total_net_grosz, 3500)
        with self.assertRaises(ValueError):
            complete.close(datetime.now(timezone.utc), unresolved_session_ids=("S-OPEN",))
```

- [ ] **Step 2: Run and record RED**

Run: `PYTHONPATH=src python -m unittest tests.test_job_lifecycle -v`

Expected: clean assertion failures because lifecycle behavior is absent; zero import/setup errors.

- [ ] **Step 3: Implement immutable lifecycle types**

```python
from datetime import datetime
from enum import Enum

from hoofcare.domain.session import Session, SessionState


class JobState(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass(frozen=True)
class CompletedSessionLink:
    event_id: str
    session_id: str
    animal_id: str


@dataclass(frozen=True)
class MaterialUsage:
    event_id: str
    session_id: str
    material_code: str
    quantity: Decimal


@dataclass(frozen=True)
class SettlementLine:
    code: str
    label: str
    quantity: Decimal
    unit: str
    unit_price_grosz: int
    total_net_grosz: int


@dataclass(frozen=True)
class Settlement:
    settlement_id: str
    job_id: str
    closed_at: datetime
    lines: tuple[SettlementLine, ...]
    total_net_grosz: int


@dataclass(frozen=True)
class Job:
    job_id: str
    farm_id: str
    operator_id: str
    opened_at: datetime
    pricing: JobPricingSnapshot
    planned_cows: int | None
    state: JobState = JobState.OPEN
    completed_links: tuple[CompletedSessionLink, ...] = ()
    usages: tuple[MaterialUsage, ...] = ()
    closed_settlement: Settlement | None = None

    @classmethod
    def open(cls, job_id: str, farm_id: str, operator_id: str, opened_at: datetime, pricing: JobPricingSnapshot, planned_cows: int | None) -> "Job":
        if opened_at.tzinfo is None:
            raise ValueError("opened_at must be timezone-aware")
        if planned_cows is not None and planned_cows < 0:
            raise ValueError("planned_cows must be non-negative")
        return cls(_text("job_id", job_id), _text("farm_id", farm_id), _text("operator_id", operator_id), opened_at, pricing, planned_cows)

    @property
    def completed_cows(self) -> int:
        return len(self.completed_links)

    @property
    def completed_session_ids(self) -> tuple[str, ...]:
        return tuple(link.session_id for link in self.completed_links)

    @property
    def animal_ids(self) -> tuple[str, ...]:
        return tuple(link.animal_id for link in self.completed_links)

    @property
    def material_total_grosz(self) -> int:
        return sum(self.pricing.rate(item.material_code).line_total_grosz(item.quantity) for item in self.usages)

    def record_completed_session(self, session: Session, event_id: str) -> "Job":
        self._require_open()
        if session.state is not SessionState.COMPLETED or not session.animal_id:
            raise ValueError("only completed identified sessions are billable")
        normalized_event_id = _text("event_id", event_id)
        for link in self.completed_links:
            if link.event_id == normalized_event_id:
                if (link.session_id, link.animal_id) == (session.session_id, session.animal_id):
                    return self
                raise ValueError("completion event payload conflict")
        if session.session_id in self.completed_session_ids or session.animal_id in self.animal_ids:
            raise ValueError("session or animal already counted in job")
        link = CompletedSessionLink(normalized_event_id, session.session_id, session.animal_id)
        return replace(self, completed_links=self.completed_links + (link,))

    def record_material(self, event_id: str, session_id: str, material_code: str, quantity: Decimal) -> "Job":
        self._require_open()
        if session_id not in self.completed_session_ids:
            raise ValueError("material requires a completed session linked to this job")
        rate = self.pricing.rate(material_code)
        normalized = rate.normalize_quantity(quantity)
        usage = MaterialUsage(_text("event_id", event_id), _text("session_id", session_id), material_code, normalized)
        for existing in self.usages:
            if existing.event_id == usage.event_id:
                if existing == usage:
                    return self
                raise ValueError("material event payload conflict")
        return replace(self, usages=self.usages + (usage,))

    def add_local_material(self, rate: MaterialRate) -> "Job":
        self._require_open()
        return replace(self, pricing=self.pricing.with_local_material(rate))

    def close(self, closed_at: datetime, unresolved_session_ids: tuple[str, ...]) -> "Job":
        self._require_open()
        if closed_at.tzinfo is None or unresolved_session_ids:
            raise ValueError("job closure requires a timezone and no unresolved sessions")
        settlement = self._build_settlement(closed_at)
        return replace(self, state=JobState.CLOSED, closed_settlement=settlement)

    def settlement(self) -> Settlement:
        if self.closed_settlement is None:
            raise ValueError("job is not closed")
        return self.closed_settlement

    def _require_open(self) -> None:
        if self.state is not JobState.OPEN:
            raise ValueError("job must be open")

    def _build_settlement(self, closed_at: datetime) -> Settlement:
        cow_line = SettlementLine(
            "COW", "Wykonane krowy", Decimal(self.completed_cows), "szt.",
            self.pricing.cow_unit_price_grosz,
            self.pricing.cow_subtotal_grosz(self.completed_cows),
        )
        quantities: dict[str, Decimal] = {}
        for usage in self.usages:
            quantities[usage.material_code] = quantities.get(usage.material_code, Decimal("0")) + usage.quantity
        material_lines = tuple(
            SettlementLine(code, self.pricing.rate(code).label, quantity,
                           self.pricing.rate(code).unit,
                           self.pricing.rate(code).unit_price_grosz,
                           self.pricing.rate(code).line_total_grosz(quantity))
            for code, quantity in sorted(quantities.items())
        )
        lines = (cow_line,) + material_lines
        return Settlement(f"{self.job_id}-SETTLEMENT-1", self.job_id, closed_at,
                          lines, sum(line.total_net_grosz for line in lines))
```

Create `tests/job_fixtures.py` exactly as deterministic synthetic data; no helper reads environment, network or real data:

```python
from datetime import datetime, timezone
from decimal import Decimal

from hoofcare.domain.jobs import Job, JobPricingSnapshot, MaterialRate
from hoofcare.domain.session import AnimalIdentityResolution, Session, SessionState


OPENED = datetime(2026, 8, 23, 8, tzinfo=timezone.utc)
CLOSED = datetime(2026, 8, 23, 18, tzinfo=timezone.utc)


def completed_session(animal_id: str, session_id: str) -> Session:
    return Session(
        session_id=session_id,
        state=SessionState.COMPLETED,
        identity=AnimalIdentityResolution.confirmed(animal_id),
        animal_id=animal_id,
        applied_event_ids=(f"identity-{session_id}", f"complete-{session_id}"),
    )


def open_job_fixture() -> Job:
    pricing = JobPricingSnapshot(3500, (MaterialRate("BLOCK", "Klocek", "szt.", 2600, 0),))
    return Job.open("TEST-JOB-1", "TEST-FARM-1", "operator-pawel", OPENED, pricing, 40)


def closed_job_fixture() -> Job:
    job = open_job_fixture()
    for index in range(1, 41):
        session = completed_session(f"TEST-COW-{index:03d}", f"TEST-SESSION-{index:03d}")
        job = job.record_completed_session(session, f"job-complete-{index}")
    for index, session_id in enumerate(job.completed_session_ids[:6], start=1):
        job = job.record_material(f"block-{index}", session_id, "BLOCK", Decimal("1"))
    return job.close(CLOSED, ())


def closed_job(job_id: str, operator_id: str, cow_count: int,
               expected_total_grosz: int, farm_id: str = "TEST-FARM-1") -> Job:
    if cow_count <= 0 or expected_total_grosz % cow_count:
        raise ValueError("fixture total must divide exactly by positive cow_count")
    job = Job.open(job_id, farm_id, operator_id, OPENED,
                   JobPricingSnapshot(expected_total_grosz // cow_count, ()), cow_count)
    for index in range(1, cow_count + 1):
        session = completed_session(f"{job_id}-COW-{index}", f"{job_id}-SESSION-{index}")
        job = job.record_completed_session(session, f"{job_id}-EVENT-{index}")
    closed = job.close(CLOSED, ())
    if closed.settlement().total_net_grosz != expected_total_grosz:
        raise AssertionError("synthetic fixture total mismatch")
    return closed
```

- [ ] **Step 4: Run lifecycle GREEN and full regression**

Run: `PYTHONPATH=src python -m unittest tests.test_job_pricing tests.test_job_lifecycle -v`

Expected: all pricing and lifecycle tests PASS.

Run: `PYTHONPATH=src python -m unittest discover -s tests -q`

Expected: full suite PASS.

- [ ] **Step 5: Commit GREEN**

```bash
git add src/hoofcare/domain/jobs.py tests/test_job_lifecycle.py tests/job_fixtures.py
git commit -m "feat(jobs): add idempotent job lifecycle and settlement"
```

---

### Task 3: Durable Job Store and Session-to-Job Commit Ordering

**Files:**
- Create: `src/hoofcare/persistence/job_store.py`
- Create: `src/hoofcare/application/job_service.py`
- Create: `tests/test_job_persistence.py`

**Interfaces:**
- Consumes: `Job` from Task 2 and existing `LocalSessionStore`.
- Produces: `LocalJobStore.save(job)`, `load(job_id)` and `list_jobs()`.
- Produces: `JobService.commit_completed_session(job_id, session, event_id) -> Job` with durable ordering session first, job second.

- [ ] **Step 1: Write failing durability tests**

```python
import importlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from hoofcare.persistence.local_store import LocalSessionStore
from tests.job_fixtures import closed_job_fixture, completed_session, open_job_fixture


def require_symbol(case: unittest.TestCase, module_name: str, symbol: str):
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        case.fail(f"{module_name} must exist")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


class JobPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.LocalJobStore = require_symbol(self, "hoofcare.persistence.job_store", "LocalJobStore")
        self.JobService = require_symbol(self, "hoofcare.application.job_service", "JobService")

    def test_job_round_trip_preserves_pricing_and_settlement(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.LocalJobStore(Path(tmp))
            store.save(closed_job_fixture())
            loaded = store.load("TEST-JOB-1")
            self.assertEqual(loaded, closed_job_fixture())

    def test_corrupt_job_snapshot_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = self.LocalJobStore(root)
            store.save(open_job_fixture())
            path = root / "TEST-JOB-1.job.json"
            path.write_text(path.read_text().replace("3500", "9999"), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid persisted job"):
                store.load("TEST-JOB-1")

    def test_list_jobs_is_stable_and_uses_verified_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.LocalJobStore(Path(tmp))
            store.save(open_job_fixture())
            self.assertEqual(store.list_jobs(), (open_job_fixture(),))

    def test_failed_replace_preserves_previous_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.LocalJobStore(Path(tmp))
            store.save(open_job_fixture())
            with mock.patch("hoofcare.persistence.job_store.os.replace", side_effect=OSError("synthetic replace failure")):
                with self.assertRaises(OSError):
                    store.save(closed_job_fixture())
            self.assertEqual(store.load("TEST-JOB-1"), open_job_fixture())

    def test_session_is_durable_before_cow_count_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            jobs = self.LocalJobStore(root / "jobs")
            sessions = LocalSessionStore(root / "sessions")
            jobs.save(open_job_fixture())
            service = self.JobService(jobs, sessions)
            updated = service.commit_completed_session("TEST-JOB-1", completed_session("TEST-COW-1", "TEST-SESSION-1"), "event-1")
            self.assertEqual(sessions.load(updated.completed_session_ids[0]).state.value, "COMPLETED")
            self.assertEqual(jobs.load("TEST-JOB-1").completed_cows, 1)

    def test_recovery_reports_but_does_not_bill_unlinked_durable_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            jobs = self.LocalJobStore(Path(tmp) / "jobs")
            jobs.save(open_job_fixture())
            service = self.JobService(jobs, LocalSessionStore(Path(tmp) / "sessions"))
            missing = service.reconciliation_required("TEST-JOB-1", ("TEST-SESSION-9",))
            self.assertEqual(missing, ("TEST-SESSION-9",))
            self.assertEqual(jobs.load("TEST-JOB-1").completed_cows, 0)
```

- [ ] **Step 2: Run and record RED**

Run: `PYTHONPATH=src python -m unittest tests.test_job_persistence -v`

Expected: clean assertion failures on missing store/service behavior; zero environment or filesystem setup errors.

- [ ] **Step 3: Implement store using the existing integrity pattern**

```python
class LocalJobStore:
    SNAPSHOT_SCHEMA_VERSION = 1
    REVISION_SCHEMA_VERSION = 1

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, job: Job) -> None:
        payload = serialize_job(job)
        envelope = {
            "schema_version": self.SNAPSHOT_SCHEMA_VERSION,
            "job": payload,
            "integrity": {"algorithm": "sha256", "digest": digest(payload)},
        }
        atomic_json_replace(self.root / f"{safe_id(job.job_id)}.job.json", envelope)

    def load(self, job_id: str) -> Job:
        path = self.root / f"{safe_id(job_id)}.job.json"
        if not path.is_file():
            raise KeyError(job_id)
        try:
            envelope = json.loads(path.read_text(encoding="utf-8"))
            payload = envelope["job"]
            if envelope["schema_version"] != self.SNAPSHOT_SCHEMA_VERSION:
                raise ValueError("unsupported job schema")
            if envelope["integrity"] != {"algorithm": "sha256", "digest": digest(payload)}:
                raise ValueError("job snapshot integrity mismatch")
            return deserialize_job(payload)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid persisted job: {job_id}") from exc

    def list_jobs(self) -> tuple[Job, ...]:
        suffix = ".job.json"
        job_ids = tuple(sorted(path.name[:-len(suffix)] for path in self.root.glob(f"*{suffix}")))
        return tuple(self.load(job_id) for job_id in job_ids)
```

Implement `serialize_job()` and `deserialize_job()` with one-to-one fields: job identifiers and state as strings; `opened_at`/settlement `closed_at` as timezone-aware ISO-8601; pricing with integer `cow_unit_price_grosz` and every `MaterialRate` field; `completed_links` as ordered `event_id`/`session_id`/`animal_id` records; usages as ordered records with `quantity` formatted using `format(decimal, "f")`; settlement lines and total as their exact stored snapshot. Reject unknown enum values, naive datetimes, non-string quantities and any reconstructed object that violates its dataclass validation. Copy the path-safety validation, temporary sibling file, file `flush`+`fsync`, `os.replace`, and directory `fsync` sequence from `LocalSessionStore` into module-level job-store helpers; do not call its private methods.

- [ ] **Step 4: Implement service commit ordering**

```python
class JobService:
    def __init__(self, jobs: LocalJobStore, sessions: LocalSessionStore) -> None:
        self.jobs = jobs
        self.sessions = sessions

    def commit_completed_session(self, job_id: str, session: Session, event_id: str) -> Job:
        if session.state is not SessionState.COMPLETED:
            raise ValueError("session must be completed before job counting")
        self.sessions.save(session)
        current = self.jobs.load(job_id)
        updated = current.record_completed_session(session, event_id)
        self.jobs.save(updated)
        return updated

    def reconciliation_required(self, job_id: str, durable_completed_session_ids: tuple[str, ...]) -> tuple[str, ...]:
        job = self.jobs.load(job_id)
        durable = tuple(dict.fromkeys(durable_completed_session_ids))
        return tuple(session_id for session_id in durable if session_id not in job.completed_session_ids)
```

The recovery query is read-only: callers discover durable completed sessions explicitly, pass only those IDs, and receive an ordered tuple of unlinked IDs. It never updates cow counts.

- [ ] **Step 5: Run GREEN, corruption tests and regression**

Run: `PYTHONPATH=src python -m unittest tests.test_job_persistence tests.test_persistence tests.test_persistence_path_safety -v`

Expected: all tests PASS.

Run: `PYTHONPATH=src python -m unittest discover -s tests -q`

Expected: full suite PASS.

- [ ] **Step 6: Commit GREEN**

```bash
git add src/hoofcare/persistence/job_store.py src/hoofcare/application/job_service.py tests/test_job_persistence.py
git commit -m "feat(jobs): persist job snapshots and durable counters"
```

---

### Task 4: Role-Based Menu and Price Visibility

**Files:**
- Create: `src/hoofcare/hmi/job_menu.py`
- Create: `src/hoofcare/hmi/owner_access.py`
- Create: `tests/test_job_menu.py`
- Modify: `src/hoofcare/physical/layout.py`

**Interfaces:**
- Produces: `UserRole`, `JobScreen`, `JobMenuViewModel.for_role(role)`, `JobScreenView.from_job(...)` and `OwnerPinGate`.
- Consumes: read-only `Job` and `Settlement`; no persistence and no machine adapter.

- [ ] **Step 1: Write failing role and visibility tests**

```python
from datetime import datetime, timedelta, timezone
import importlib
import unittest

from tests.job_fixtures import closed_job_fixture, open_job_fixture

def require_symbol(case: unittest.TestCase, module_name: str, symbol: str):
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        case.fail(f"{module_name} must exist")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


class JobMenuTests(unittest.TestCase):
    def setUp(self):
        self.JobMenuViewModel = require_symbol(self, "hoofcare.hmi.job_menu", "JobMenuViewModel")
        self.JobScreen = require_symbol(self, "hoofcare.hmi.job_menu", "JobScreen")
        self.UserRole = require_symbol(self, "hoofcare.hmi.job_menu", "UserRole")
        self.JobScreenView = require_symbol(self, "hoofcare.hmi.job_menu", "JobScreenView")
        self.OwnerPinGate = require_symbol(self, "hoofcare.hmi.owner_access", "OwnerPinGate")

    def test_operator_and_owner_have_distinct_four_item_menus(self):
        operator = self.JobMenuViewModel.for_role(self.UserRole.OPERATOR)
        owner = self.JobMenuViewModel.for_role(self.UserRole.OWNER)
        self.assertEqual(operator.menu_labels, ("START", "KONTROLE", "HISTORIA", "WIĘCEJ"))
        self.assertEqual(owner.menu_labels, ("PULPIT", "DANE", "RAPORTY", "ZARZĄDZANIE"))

    def test_prices_are_hidden_during_treatment_but_visible_at_open_and_close(self):
        model = self.JobMenuViewModel.for_role(self.UserRole.OPERATOR)
        self.assertTrue(model.price_visible(self.JobScreen.JOB_OPEN))
        self.assertFalse(model.price_visible(self.JobScreen.TREATMENT))
        self.assertFalse(model.price_visible(self.JobScreen.JOB_COUNTERS))
        self.assertTrue(model.price_visible(self.JobScreen.JOB_CLOSE))

    def test_screen_view_exposes_total_only_on_close_surfaces(self):
        treatment = self.JobScreenView.from_job(self.JobScreen.TREATMENT, open_job_fixture())
        closed = self.JobScreenView.from_job(self.JobScreen.JOB_CLOSE, closed_job_fixture())
        self.assertNotIn("cow_unit_price_grosz", treatment.fields)
        self.assertNotIn("total_net_grosz", treatment.fields)
        self.assertEqual(closed.fields["total_net_grosz"], 155600)

    def test_no_role_exports_machine_control_actions(self):
        for role in self.UserRole:
            actions = self.JobMenuViewModel.for_role(role).all_actions
            self.assertTrue({"kvk_command", "plc_write", "open_valve", "motor_start"}.isdisjoint(actions))

    def test_four_bottom_targets_fit_1024_by_600_without_overlap(self):
        model = self.JobMenuViewModel.for_role(self.UserRole.OPERATOR)
        self.assertEqual(len(model.bottom_targets), 4)
        self.assertTrue(all(target.width_px >= 48 and target.height_px >= 48 for target in model.bottom_targets))

    def test_owner_pin_is_six_digits_and_expires(self):
        now = datetime(2026, 8, 23, 8, tzinfo=timezone.utc)
        gate = self.OwnerPinGate.from_test_pin("123456", timeout_seconds=300)
        self.assertFalse(gate.unlock("12345", now))
        self.assertTrue(gate.unlock("123456", now))
        self.assertTrue(gate.touch(now + timedelta(seconds=200)))
        self.assertTrue(gate.is_unlocked(now + timedelta(seconds=499)))
        self.assertFalse(gate.is_unlocked(now + timedelta(seconds=500)))
```

- [ ] **Step 2: Run and record RED**

Run: `PYTHONPATH=src python -m unittest tests.test_job_menu -v`

Expected: clean assertion failures because role-aware menu behavior is absent.

- [ ] **Step 3: Implement pure role/menu view models**

```python
from dataclasses import dataclass
from enum import Enum

from hoofcare.domain.jobs import Job
from hoofcare.physical.layout import ScreenId, TouchTarget


class UserRole(str, Enum):
    OPERATOR = "OPERATOR"
    OWNER = "OWNER"


class JobScreen(str, Enum):
    JOB_OPEN = "JOB_OPEN"
    TREATMENT = "TREATMENT"
    JOB_COUNTERS = "JOB_COUNTERS"
    LOCAL_MATERIAL_PRICE = "LOCAL_MATERIAL_PRICE"
    JOB_CLOSE = "JOB_CLOSE"
    CLOSED_JOB = "CLOSED_JOB"


@dataclass(frozen=True)
class JobMenuViewModel:
    role: UserRole
    menu_labels: tuple[str, ...]
    all_actions: frozenset[str]
    bottom_targets: tuple[TouchTarget, ...]

    @classmethod
    def for_role(cls, role: UserRole) -> "JobMenuViewModel":
        labels = {
            UserRole.OPERATOR: ("START", "KONTROLE", "HISTORIA", "WIĘCEJ"),
            UserRole.OWNER: ("PULPIT", "DANE", "RAPORTY", "ZARZĄDZANIE"),
        }[role]
        targets = tuple(TouchTarget(ScreenId.DASHBOARD, label.lower(), x, 500, 180, 64) for label, x in zip(labels, (62, 282, 502, 722), strict=True))
        return cls(role, labels, frozenset(label.lower() for label in labels), targets)

    @staticmethod
    def price_visible(screen: JobScreen) -> bool:
        return screen in {JobScreen.JOB_OPEN, JobScreen.LOCAL_MATERIAL_PRICE, JobScreen.JOB_CLOSE, JobScreen.CLOSED_JOB}


@dataclass(frozen=True)
class JobScreenView:
    screen: JobScreen
    fields: dict[str, int | str | None]

    @classmethod
    def from_job(cls, screen: JobScreen, job: Job) -> "JobScreenView":
        fields: dict[str, int | str | None] = {
            "job_id": job.job_id,
            "farm_id": job.farm_id,
            "completed_cows": job.completed_cows,
            "planned_cows": job.planned_cows,
        }
        if JobMenuViewModel.price_visible(screen):
            fields["cow_unit_price_grosz"] = job.pricing.cow_unit_price_grosz
            if job.closed_settlement is not None:
                fields["total_net_grosz"] = job.closed_settlement.total_net_grosz
        return cls(screen, fields)
```

Implement the synthetic local PIN gate without persisting the clear PIN:

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import hmac
import secrets


@dataclass
class OwnerPinGate:
    salt: bytes
    pin_digest: bytes
    timeout_seconds: int
    iterations: int = 200_000
    unlocked_until: datetime | None = None

    @classmethod
    def from_test_pin(cls, pin: str, timeout_seconds: int) -> "OwnerPinGate":
        if len(pin) != 6 or not pin.isascii() or not pin.isdigit():
            raise ValueError("owner PIN must contain exactly six ASCII digits")
        if type(timeout_seconds) is not int or timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac("sha256", pin.encode("ascii"), salt, 200_000)
        return cls(salt, digest, timeout_seconds)

    def unlock(self, pin: str, now: datetime) -> bool:
        self.unlocked_until = None
        if now.tzinfo is None or len(pin) != 6 or not pin.isascii() or not pin.isdigit():
            return False
        candidate = hashlib.pbkdf2_hmac("sha256", pin.encode("ascii"), self.salt, self.iterations)
        if not hmac.compare_digest(self.pin_digest, candidate):
            return False
        self.unlocked_until = now + timedelta(seconds=self.timeout_seconds)
        return True

    def is_unlocked(self, now: datetime) -> bool:
        if now.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        return self.unlocked_until is not None and now < self.unlocked_until

    def touch(self, now: datetime) -> bool:
        if not self.is_unlocked(now):
            return False
        self.unlocked_until = now + timedelta(seconds=self.timeout_seconds)
        return True

    def lock(self) -> None:
        self.unlocked_until = None
```

Extend `ScreenId` with these exact enum members:

```python
    JOB_OPEN = "JOB_OPEN"
    JOB_COUNTERS = "JOB_COUNTERS"
    LOCAL_MATERIAL_PRICE = "LOCAL_MATERIAL_PRICE"
    JOB_CLOSE = "JOB_CLOSE"
    CLOSED_JOB = "CLOSED_JOB"
    OWNER_DASHBOARD = "OWNER_DASHBOARD"
    OWNER_DATA = "OWNER_DATA"
    OWNER_REPORTS = "OWNER_REPORTS"
    OWNER_MANAGEMENT = "OWNER_MANAGEMENT"
```

Insert these exact entries at the end of the `screens` dictionary before the existing geometry loop; do not add or rename controls on existing treatment screens:

```python
            ScreenId.JOB_OPEN: ScreenLayout(
                ScreenId.JOB_OPEN,
                data_bindings=("farm_id", "planned_cows", "cow_unit_price_grosz"),
                control_ids=("save_job", "cancel"),
            ),
            ScreenId.JOB_COUNTERS: ScreenLayout(
                ScreenId.JOB_COUNTERS,
                data_bindings=("completed_cows", "planned_cows", "material_quantities"),
                control_ids=("new_session", "add_material", "close_job", "back"),
            ),
            ScreenId.LOCAL_MATERIAL_PRICE: ScreenLayout(
                ScreenId.LOCAL_MATERIAL_PRICE,
                data_bindings=("material_label", "unit", "unit_price_grosz"),
                control_ids=("save_local_material", "cancel"),
            ),
            ScreenId.JOB_CLOSE: ScreenLayout(
                ScreenId.JOB_CLOSE,
                data_bindings=("settlement_lines", "total_net_grosz"),
                control_ids=("confirm_close", "back"),
            ),
            ScreenId.CLOSED_JOB: ScreenLayout(
                ScreenId.CLOSED_JOB,
                data_bindings=("settlement_id", "settlement_lines", "total_net_grosz"),
                control_ids=("generate_settlement_pdf", "back_to_dashboard"),
            ),
            ScreenId.OWNER_DASHBOARD: ScreenLayout(
                ScreenId.OWNER_DASHBOARD,
                data_bindings=("job_count", "completed_cows", "total_net_grosz"),
                control_ids=("open_operator_view", "lock_owner"),
            ),
            ScreenId.OWNER_DATA: ScreenLayout(
                ScreenId.OWNER_DATA,
                data_bindings=("farm_filter", "operator_filter", "date_filter"),
                control_ids=("apply_filters", "back"),
            ),
            ScreenId.OWNER_REPORTS: ScreenLayout(
                ScreenId.OWNER_REPORTS,
                data_bindings=("job_statistics", "material_quantities"),
                control_ids=("open_job", "back"),
            ),
            ScreenId.OWNER_MANAGEMENT: ScreenLayout(
                ScreenId.OWNER_MANAGEMENT,
                data_bindings=("owner_access_state",),
                control_ids=("open_operator_view", "lock_owner"),
            ),
```

- [ ] **Step 4: Run geometry, navigation and security GREEN**

Run: `PYTHONPATH=src python -m unittest tests.test_job_menu tests.test_physical_hmi_layout tests.test_r2_hmi_navigation_geometry tests.test_physical_navigation -v`

Expected: all tests PASS.

Run: `PYTHONPATH=src python -m unittest discover -s tests -q`

Expected: full suite PASS.

- [ ] **Step 5: Commit GREEN**

```bash
git add src/hoofcare/hmi/job_menu.py src/hoofcare/hmi/owner_access.py src/hoofcare/physical/layout.py tests/test_job_menu.py
git commit -m "feat(hmi): add role-aware job menus and price visibility"
```

---

### Task 5: Derived Statistics and Settlement PDF

**Files:**
- Create: `src/hoofcare/application/job_statistics.py`
- Create: `src/hoofcare/reporting/pdf.py`
- Create: `src/hoofcare/reporting/settlement.py`
- Modify: `src/hoofcare/reporting/report.py`
- Create: `tests/test_job_statistics_reporting.py`

**Interfaces:**
- Produces: `JobStatisticsQuery` and `JobStatistics.from_jobs(jobs, role, query)` with date, farm and operator filters.
- Produces: `SettlementDocument.from_job(job, generated_at)` and `to_pdf_bytes()`.
- Extracts existing PDF rendering into `render_minimal_pdf(lines: tuple[str, ...]) -> bytes` without changing current report bytes contract.

- [ ] **Step 1: Write failing statistics and PDF tests**

```python
from datetime import datetime, timezone
import importlib
import unittest

from hoofcare.domain.jobs import JobState
from hoofcare.hmi.job_menu import UserRole
from tests.job_fixtures import closed_job, closed_job_fixture, open_job_fixture


def require_symbol(case: unittest.TestCase, module_name: str, symbol: str):
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        case.fail(f"{module_name} must exist")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


class JobStatisticsReportingTests(unittest.TestCase):
    def setUp(self):
        self.JobStatistics = require_symbol(self, "hoofcare.application.job_statistics", "JobStatistics")
        self.JobStatisticsQuery = require_symbol(self, "hoofcare.application.job_statistics", "JobStatisticsQuery")
        self.SettlementDocument = require_symbol(self, "hoofcare.reporting.settlement", "SettlementDocument")
        self.format_pln = require_symbol(self, "hoofcare.reporting.settlement", "format_pln")

    def test_operator_statistics_are_scoped_to_operator(self):
        jobs = (closed_job("TEST-J1", "operator-pawel", 2, 7000), closed_job("TEST-J2", "other", 3, 10500))
        query = self.JobStatisticsQuery(operator_id="operator-pawel")
        stats = self.JobStatistics.from_jobs(jobs, UserRole.OPERATOR, query)
        self.assertEqual(stats.completed_cows, 2)
        self.assertEqual(stats.total_net_grosz, 7000)

    def test_owner_statistics_cover_all_jobs(self):
        jobs = (closed_job("TEST-J1", "operator-pawel", 2, 7000), closed_job("TEST-J2", "other", 3, 10500, farm_id="TEST-FARM-2"))
        stats = self.JobStatistics.from_jobs(jobs, UserRole.OWNER, self.JobStatisticsQuery())
        self.assertEqual(stats.completed_cows, 5)
        self.assertEqual(stats.total_net_grosz, 17500)

    def test_owner_can_filter_by_farm_and_date(self):
        jobs = (closed_job("TEST-J1", "operator-pawel", 2, 7000), closed_job("TEST-J2", "other", 3, 10500, farm_id="TEST-FARM-2"))
        query = self.JobStatisticsQuery(
            farm_id="TEST-FARM-2",
            opened_from=datetime(2026, 8, 23, tzinfo=timezone.utc),
            opened_through=datetime(2026, 8, 24, tzinfo=timezone.utc),
        )
        stats = self.JobStatistics.from_jobs(jobs, UserRole.OWNER, query)
        self.assertEqual((stats.job_count, stats.completed_cows), (1, 3))

    def test_status_filter_includes_open_job_without_inventing_net_total(self):
        query = self.JobStatisticsQuery(state=JobState.OPEN)
        stats = self.JobStatistics.from_jobs((open_job_fixture(),), UserRole.OWNER, query)
        self.assertEqual((stats.job_count, stats.total_net_grosz), (1, 0))

    def test_settlement_pdf_is_local_summary_not_invoice(self):
        document = self.SettlementDocument.from_job(closed_job_fixture(), datetime(2026, 8, 23, 19, tzinfo=timezone.utc))
        pdf = document.to_pdf_bytes()
        self.assertTrue(pdf.startswith(b"%PDF-1.4"))
        self.assertIn("NOT AN INVOICE", document.disclaimer)
        self.assertEqual(document.total_net_grosz, 155600)
        self.assertEqual(self.format_pln(document.total_net_grosz), "1 556,00 zł")
```

- [ ] **Step 2: Run and record RED**

Run: `PYTHONPATH=src python -m unittest tests.test_job_statistics_reporting -v`

Expected: clean assertion failures because derived statistics and settlement report do not exist.

- [ ] **Step 3: Implement derived statistics**

```python
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Iterable

from hoofcare.domain.jobs import Job, JobState
from hoofcare.hmi.job_menu import UserRole


@dataclass(frozen=True)
class JobStatisticsQuery:
    operator_id: str | None = None
    farm_id: str | None = None
    opened_from: datetime | None = None
    opened_through: datetime | None = None
    state: JobState | None = None


@dataclass(frozen=True)
class JobStatistics:
    job_count: int
    completed_cows: int
    material_quantities: dict[str, Decimal]
    total_net_grosz: int

    @classmethod
    def from_jobs(cls, jobs: Iterable[Job], role: UserRole, query: JobStatisticsQuery) -> "JobStatistics":
        if role is UserRole.OPERATOR and not query.operator_id:
            raise ValueError("operator statistics require operator_id")
        if query.opened_from is not None and query.opened_from.tzinfo is None:
            raise ValueError("opened_from must be timezone-aware")
        if query.opened_through is not None and query.opened_through.tzinfo is None:
            raise ValueError("opened_through must be timezone-aware")
        selected = tuple(
            job for job in jobs
            if (role is UserRole.OWNER or job.operator_id == query.operator_id)
            and (query.operator_id is None or job.operator_id == query.operator_id)
            and (query.farm_id is None or job.farm_id == query.farm_id)
            and (query.opened_from is None or job.opened_at >= query.opened_from)
            and (query.opened_through is None or job.opened_at < query.opened_through)
            and (query.state is None or job.state is query.state)
        )
        quantities: dict[str, Decimal] = {}
        for job in selected:
            for usage in job.usages:
                quantities[usage.material_code] = quantities.get(usage.material_code, Decimal("0")) + usage.quantity
        return cls(
            len(selected),
            sum(job.completed_cows for job in selected),
            quantities,
            sum(job.settlement().total_net_grosz for job in selected if job.state is JobState.CLOSED),
        )
```

- [ ] **Step 4: Extract renderer and implement settlement document**

Copy `_pdf_escape`, `_pdf_ascii`, and the complete existing `_build_minimal_pdf` body byte-for-byte from `report.py` to `pdf.py`; rename only the public function to `render_minimal_pdf`. In `report.py`, delete those three local helpers, add `from hoofcare.reporting.pdf import render_minimal_pdf`, and replace `return _build_minimal_pdf(tuple(lines))` with `return render_minimal_pdf(tuple(lines))`. This mechanical extraction must leave every existing report byte assertion unchanged.

```python
from dataclasses import dataclass
from datetime import datetime

from hoofcare.domain.jobs import Job, SettlementLine
from hoofcare.reporting.pdf import render_minimal_pdf


def format_pln(grosz: int) -> str:
    if type(grosz) is not int or grosz < 0:
        raise ValueError("PLN value must be non-negative integer grosze")
    whole = f"{grosz // 100:,}".replace(",", " ")
    return f"{whole},{grosz % 100:02d} zł"


@dataclass(frozen=True)
class SettlementDocument:
    settlement_id: str
    job_id: str
    farm_id: str
    operator_id: str
    generated_at_iso: str
    lines: tuple[SettlementLine, ...]
    total_net_grosz: int
    disclaimer: str = "LOCAL NET SERVICE SUMMARY — NOT AN INVOICE"

    @classmethod
    def from_job(cls, job: Job, generated_at: datetime) -> "SettlementDocument":
        if generated_at.tzinfo is None:
            raise ValueError("generated_at must be timezone-aware")
        settlement = job.settlement()
        return cls(settlement.settlement_id, job.job_id, job.farm_id, job.operator_id, generated_at.isoformat(), settlement.lines, settlement.total_net_grosz)

    def to_pdf_bytes(self) -> bytes:
        rows = tuple(f"{line.label}: {line.quantity} {line.unit} x {line.unit_price_grosz} gr = {line.total_net_grosz} gr" for line in self.lines)
        heading = (f"Settlement-ID: {self.settlement_id}", f"Job-ID: {self.job_id}", f"Farm-ID: {self.farm_id}", f"Operator-ID: {self.operator_id}", self.disclaimer)
        total = (f"RAZEM NETTO: {format_pln(self.total_net_grosz)}",)
        return render_minimal_pdf(heading + rows + total)
```

- [ ] **Step 5: Run GREEN and regression**

Run: `PYTHONPATH=src python -m unittest tests.test_job_statistics_reporting tests.test_reporting -v`

Expected: all tests PASS.

Run: `PYTHONPATH=src python -m unittest discover -s tests -q`

Expected: full suite PASS.

- [ ] **Step 6: Commit GREEN**

```bash
git add src/hoofcare/application/job_statistics.py src/hoofcare/reporting/pdf.py src/hoofcare/reporting/settlement.py src/hoofcare/reporting/report.py tests/test_job_statistics_reporting.py
git commit -m "feat(jobs): derive statistics and local settlement PDF"
```

---

### Task 6: Synthetic End-to-End Job Workflow and Reconciliation

**Files:**
- Create: `src/hoofcare/integration/job_settlement.py`
- Create: `tests/test_job_settlement_integration.py`
- Modify: `docs/traceability/HC-REQ-TRACE-001_Requirement_Level_Matrix_v0.1.md`
- Modify: `docs/traceability/HC-TRACE-001_Traceability.md`
- Modify: `project_context/CURRENT_STATE.md`

**Interfaces:**
- Consumes: domain, stores, service, menu, statistics and reporting from Tasks 1–5.
- Produces: `SyntheticJobSettlementScenario.run(root: Path) -> SyntheticJobSettlementResult`.

- [ ] **Step 1: Write failing end-to-end test**

```python
import importlib
import tempfile
import unittest
from pathlib import Path


def require_symbol(case: unittest.TestCase, module_name: str, symbol: str):
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        case.fail(f"{module_name} must exist")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


class JobSettlementIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.Scenario = require_symbol(self, "hoofcare.integration.job_settlement", "SyntheticJobSettlementScenario")

    def test_synthetic_job_survives_restart_and_closes_with_exact_net_total(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.Scenario().run(Path(tmp))
        self.assertEqual(result.completed_cows, 40)
        self.assertEqual(result.material_quantities["BLOCK"], "6")
        self.assertEqual(result.total_net_grosz, 155600)
        self.assertTrue(result.pdf.startswith(b"%PDF-1.4"))
        self.assertFalse(result.kvk_connection_allowed)
        self.assertFalse(result.real_farm_data_used)

    def test_incomplete_session_blocks_job_close_without_changing_total(self):
        with tempfile.TemporaryDirectory() as tmp:
            scenario = self.Scenario()
            with self.assertRaisesRegex(ValueError, "unresolved sessions"):
                scenario.run_with_incomplete_session(Path(tmp))
```

- [ ] **Step 2: Run and record RED**

Run: `PYTHONPATH=src python -m unittest tests.test_job_settlement_integration -v`

Expected: clean assertion failures because the integration scenario does not exist.

- [ ] **Step 3: Implement the bounded synthetic scenario**

```python
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from hoofcare.application.job_service import JobService
from hoofcare.domain.jobs import Job, JobPricingSnapshot, MaterialRate
from hoofcare.domain.session import AnimalIdentityResolution, Session, SessionState
from hoofcare.persistence.job_store import LocalJobStore
from hoofcare.persistence.local_store import LocalSessionStore
from hoofcare.reporting.settlement import SettlementDocument


@dataclass(frozen=True)
class SyntheticJobSettlementResult:
    completed_cows: int
    material_quantities: dict[str, str]
    total_net_grosz: int
    pdf: bytes
    kvk_connection_allowed: bool = False
    real_farm_data_used: bool = False


class SyntheticJobSettlementScenario:
    NOW = datetime(2026, 8, 23, 8, tzinfo=timezone.utc)

    @staticmethod
    def _build_job() -> Job:
        pricing = JobPricingSnapshot(
            cow_unit_price_grosz=3500,
            additional_materials=(MaterialRate("BLOCK", "Klocek", "szt.", 2600, 0),),
        )
        return Job.open("TEST-JOB-001", "TEST-FARM-001", "operator-pawel",
                        SyntheticJobSettlementScenario.NOW, pricing, 40)

    @staticmethod
    def _completed_session(index: int) -> Session:
        animal_id = f"TEST-COW-{index:03d}"
        return Session(
            session_id=f"TEST-SESSION-{index:03d}",
            state=SessionState.COMPLETED,
            identity=AnimalIdentityResolution.confirmed(animal_id),
            animal_id=animal_id,
            applied_event_ids=(f"identity-{index}", f"complete-{index}"),
        )

    def run(self, root: Path) -> SyntheticJobSettlementResult:
        jobs = LocalJobStore(root / "jobs")
        sessions = LocalSessionStore(root / "sessions")
        service = JobService(jobs, sessions)
        job = self._build_job()
        jobs.save(job)
        for index in range(1, 41):
            service.commit_completed_session(job.job_id, self._completed_session(index), f"job-complete-{index}")
        current = jobs.load(job.job_id)
        for index in range(6):
            current = current.record_material(f"block-{index + 1}", current.completed_session_ids[index], "BLOCK", Decimal("1"))
        jobs.save(current)
        restarted = LocalJobStore(root / "jobs").load(job.job_id)
        closed = restarted.close(datetime(2026, 8, 23, 18, tzinfo=timezone.utc), unresolved_session_ids=())
        jobs.save(closed)
        document = SettlementDocument.from_job(jobs.load(job.job_id), datetime(2026, 8, 23, 19, tzinfo=timezone.utc))
        quantities: dict[str, Decimal] = {}
        for usage in closed.usages:
            quantities[usage.material_code] = quantities.get(usage.material_code, Decimal("0")) + usage.quantity
        return SyntheticJobSettlementResult(
            closed.completed_cows,
            {code: format(quantity, "f") for code, quantity in sorted(quantities.items())},
            closed.settlement().total_net_grosz,
            document.to_pdf_bytes(),
        )

    def run_with_incomplete_session(self, root: Path) -> None:
        jobs = LocalJobStore(root / "jobs")
        job = self._build_job()
        jobs.save(job)
        unresolved = Session.new()
        LocalSessionStore(root / "sessions").save(unresolved)
        current = jobs.load(job.job_id)
        current.close(datetime(2026, 8, 23, 18, tzinfo=timezone.utc), (unresolved.session_id,))
        raise AssertionError("close unexpectedly accepted an unresolved session")
```

The fixed prices satisfy the expected total exactly: `40 × 3500 gr + 6 × 2600 gr = 155600 gr`. Keep every identifier explicitly prefixed `TEST-`.

- [ ] **Step 4: Run targeted and full verification**

Run: `PYTHONPATH=src python -m unittest tests.test_job_pricing tests.test_job_lifecycle tests.test_job_persistence tests.test_job_menu tests.test_job_statistics_reporting tests.test_job_settlement_integration -v`

Expected: all UX-HC-001 tests PASS.

Run: `python -m compileall -q src tests scripts && PYTHONPATH=src python -m unittest discover -s tests -v && PYTHONPATH=src python scripts/run_coverage.py && python scripts/check_foundation.py && python scripts/check_semantic_governance.py && git diff --check`

Expected: compileall, full regression, coverage, foundation governance, semantic governance and diff check PASS.

- [ ] **Step 5: Reconcile only verified status**

Update traceability and current state with exact RED, GREEN and final SHAs. Record `UX-HC-001 = IMPLEMENTED / VERIFICATION PENDING` before merge and do not claim closure, real-data readiness, production authentication, invoicing or deployment.

- [ ] **Step 6: Commit final reconciliation**

```bash
git add src/hoofcare/integration/job_settlement.py tests/test_job_settlement_integration.py docs/traceability/HC-REQ-TRACE-001_Requirement_Level_Matrix_v0.1.md docs/traceability/HC-TRACE-001_Traceability.md project_context/CURRENT_STATE.md
git commit -m "docs(ux-hc-001): reconcile synthetic job settlement evidence"
```

---

## Final Verification Gate

- [ ] Confirm PR base is the then-current verified `main`.
- [ ] Confirm all intended RED commits exist remotely and contain clean assertion failures.
- [ ] Confirm every GREEN is a descendant of its corresponding RED.
- [ ] Confirm remote final tree equals the independently verified local tree.
- [ ] Confirm runtime-ci and docs-ci are green on the exact final head.
- [ ] Confirm review threads are empty or resolved and no foreign approval is relied upon.
- [ ] Confirm the PR remains Draft until Project Owner approves its exact final head.
- [ ] Merge only with `expected_head_sha` after explicit exact-head approval.
- [ ] Run Repository Verification on the exact merge commit before changing lifecycle status.
