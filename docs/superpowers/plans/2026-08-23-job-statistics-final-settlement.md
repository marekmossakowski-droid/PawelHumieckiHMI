# Job Statistics and Final Settlement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add trustworthy per-job and per-day statistics plus a final local `RAZEM NETTO` settlement summary from canonical persisted jobs.

**Architecture:** Derive all statistics from durable completed-session links and stored settlement snapshots; never maintain a second mutable counter. Keep calculations in the domain/application layer and expose presentation-only HMI models. Generate a local settlement summary that is explicitly not an invoice.

**Tech Stack:** Python 3 standard library, immutable dataclasses, `Decimal`, existing `LocalJobStore`, `unittest`, deterministic local PDF renderer.

**Spec:** `docs/requirements/REQ-HC-002_Role_Based_Jobs_Settlement_and_Statistics_v0.1.md`

## Status and authority

`FULFILLED FOR AUTHORIZED S1 SCOPE — CLOSURE READY / PROJECT OWNER MERGE REQUIRED`

Runtime wykonano prospektywnie pod aktywnym `IA-HC-007-S1` w czterech
kontrolowanych inkrementach S1-1..S1-4. Każdy inkrement zachował clean assertion
RED, zdalny test-only checkpoint, minimalny GREEN, pełną regresję, Draft PR,
zgodę Project Ownera na exact head, kontrolowany merge i Repository Verification.

## Global Constraints

- Standard materials are included in the per-cow rate; only additional materials create separate settlement lines.
- A cow counts only after a durable `COMPLETED` session-to-job assignment.
- Money is integer grosz; material quantities use declared decimal precision and `ROUND_HALF_UP` only at line valuation.
- Prices stay hidden during routine animal work and appear at job opening, permitted correction and final summary.
- Output is local `RAZEM NETTO` in PLN and is not an invoice; no VAT, accounting or payment behavior.
- Generation 1 HMI remains autonomous; computer, phone and tablet clients remain Generation 2 and out of scope.
- No real data, network/cloud, device I/O, KVK, control, deployment or release.

## File map

| File | Responsibility |
|---|---|
| `src/hoofcare/application/job_statistics.py` | immutable filters and derived aggregates |
| `src/hoofcare/reporting/settlement.py` | deterministic local settlement document model |
| `src/hoofcare/hmi/job_menu.py` | presentation-only daily/job counters and final summary bindings |
| `src/hoofcare/integration/job_settlement.py` | synthetic restart-to-summary scenario |
| `tests/test_job_statistics.py` | operator/farm/date filtering and provenance |
| `tests/test_job_settlement_report.py` | line values, formatting and non-invoice disclaimer |
| `tests/test_job_settlement_integration.py` | restart, counters, materials and close workflow |

---

### Task 1: Derived statistics query

**Requirements:** `REQ-HC-JOB-STAT-001..003`, `REQ-HC-JOB-COUNT-001..003`.

**Files:** Create `src/hoofcare/application/job_statistics.py`; create `tests/test_job_statistics.py`.

**Interfaces:** Produce `StatisticsFilter(operator_id: str | None, farm_id: str | None, date_from: date, date_to: date)` and `derive_job_statistics(jobs: Iterable[Job], filter: StatisticsFilter) -> JobStatistics`.

- [ ] Write tests proving completed-cow counts come from unique durable links, duplicate events do not increment, open/closed job counts are separated, and operator/farm/date filters do not leak rows.
- [ ] Run `PYTHONPATH=src python -m unittest tests.test_job_statistics -v`; expect clean assertion failures because the module is absent.
- [ ] Commit and publish the RED checkpoint before production code.
- [ ] Implement immutable `JobStatistics(completed_cows, additional_material_quantities, open_jobs, closed_jobs, total_net_grosz)`; include money only from closed stored settlements.
- [ ] Run targeted tests and full regression; commit minimal GREEN.

### Task 2: Deterministic final settlement summary

**Requirements:** `REQ-HC-JOB-PRICE-002..003`, `REQ-HC-JOB-CLOSE-001..003`.

**Files:** Create `src/hoofcare/reporting/settlement.py`; create `tests/test_job_settlement_report.py`; reuse the existing deterministic PDF primitive without changing clinical reports.

**Interfaces:** Produce `format_pln(grosz: int) -> str` and `SettlementDocument.from_closed_job(job: Job, generated_at: datetime) -> SettlementDocument` with `render_pdf() -> bytes`.

- [ ] Write tests for Polish money formatting, per-cow line, each additional-material line, exact sum equality, immutable stored values after restart, and visible `DOKUMENT ROZLICZENIOWY — NIE JEST FAKTURĄ`.
- [ ] Verify RED as assertion failures, publish the test-only checkpoint, then implement the smallest renderer adapter.
- [ ] Reject open jobs, naive timestamps, recalculation from a current catalogue, VAT/invoice fields and totals inconsistent with the stored snapshot.
- [ ] Run targeted tests, existing report tests, full regression and governance; commit GREEN.

### Task 3: Semantic HMI counters and close screen

**Requirements:** `REQ-HC-JOB-COUNT-003`, `REQ-HC-JOB-CLOSE-002`, `REQ-HC-JOB-STAT-001`.

**Files:** Modify `src/hoofcare/hmi/job_menu.py`; create `tests/test_job_statistics_hmi.py`.

**Interfaces:** Produce presentation-only `daily_work_view(...)` and `closed_job_summary_view(...)`; consume canonical `JobStatistics` and `SettlementDocument`, never compute money locally.

- [ ] Test that Paweł sees today’s completed cows and additional-material quantities, routine work screens contain no price bindings, and the closed screen contains line items plus dominant `total_net_grosz`.
- [ ] Verify and publish RED; add only semantic bindings and GL100E profile geometry with touch targets at least 64 px.
- [ ] Prove the geometry profile is separate from domain behavior and does not limit future presentation clients.
- [ ] Run targeted/full tests and commit GREEN.

### Task 4: Restart integration and traceability

**Requirements:** all requirements listed above.

**Files:** Create `src/hoofcare/integration/job_settlement.py` and `tests/test_job_settlement_integration.py`; modify `docs/traceability/HC-REQ-TRACE-001_Requirement_Level_Matrix_v0.1.md`, `docs/traceability/HC-TRACE-001_Traceability.md`, and `project_context/CURRENT_STATE.md` only after evidence exists.

**Interfaces:** Produce `SyntheticJobSettlementScenario.run() -> SettlementScenarioResult` containing persisted counters, material quantities, line values and `total_net_grosz`.

- [ ] Write a restart scenario: open job, complete distinct cows, add extra materials to completed sessions, restart stores/services, close job, derive daily statistics and render final summary.
- [ ] Assert count idempotency, exact material quantities, `total_net_grosz`, and identical results before/after the second restart.
- [ ] Verify and publish RED; implement only orchestration over existing canonical services.
- [ ] Run the full verification suite: unittest discovery, coverage, compileall, foundation governance, semantic governance and diff check.
- [ ] Reconcile traceability honestly: synthetic requirements may become implemented, while finished GUI, GL100E physical acceptance, Generation 2 and excluded financial functions remain partial/deferred.

## Self-review

- Spec coverage: counting, additional materials, close blocking, stored net total, operator/owner views and provenance are each mapped to a task.
- Placeholder scan: no unresolved placeholder, generic error-handling instruction, or unnamed test step remains.
- Type consistency: all later tasks consume `StatisticsFilter`, `JobStatistics`, `SettlementDocument` and canonical `Job` exactly as defined above.
