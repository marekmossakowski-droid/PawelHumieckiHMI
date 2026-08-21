# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. Final commercial/product name remains `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`F80 / BENCH IMPLEMENTATION — S4 HMI PROTOTYPE WORKFLOW IN PROGRESS`

## Canonical repository
`marekmossakowski-droid/PawelHumieckiHMI`

## Canonical main checkpoints
- Foundation PR #1 → `de68522e4851f645d65dee7dda08ef8fed6af955`.
- ARS PR #2 → `b0286b73b90c95f05b1d99ef58ac9a9fae197880`.
- ARB PR #3 → `9144a6a003f58ea12c5a6c3d4ff26c26527d0292`.
- ADR PR #4 → `c2493ef39a1b45b934cd2dc001279db110a17fc0`.
- System Architecture PR #5 → `5a0761dec9dbbca538be787839d93017f5c501df`.
- LEL PR #6 → `a7d031317cf25934218cd09a4916449f2bf5b634`.
- Requirements PR #7 → `e34e2a2ae3f709d83c24d528f8930b1b72060961`.
- IMP + IA activation PR #8 → `0d58eb2921df298114c304295a061547598ae541`.
- S1 Domain/session core PR #9 → `7467ec4e30b5ecd8831c094bd90ba7d1fe0ad7b2`.
- S2 Durable persistence PR #10 → `c5f60dbf11b04b680c6f51f2e610d33906b08637`.
- S3 Local HMI-edge contract PR #11 approved head `707c42cc23fbff1193971db5960e0e216402faa2`, merged as `003c8d5d0ab9e026a76e4a519e8b1c246458bc8a`.

## Governance state
- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `APPROVED / BASELINED`.
- `IA-HC-001`: `ACTIVE` for bounded local bench MVP only.
- Runtime implementation authority: `ESTABLISHED — BOUNDED BENCH ONLY`.
- `HC-S1-001`: `MERGED / VERIFIED`.
- `HC-S2-001`: `MERGED / VERIFIED`.
- `HC-S3-001`: `MERGED / VERIFIED`.
- `HC-S4-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`.

## Active authority boundaries
Authorized: synthetic/test data, domain/session core, local persistence/recovery, local HMI↔edge contract, HMI prototype workflow, local PDF, simulated RFID/KVK observations, tests.

Not authorized: live KVK I/O of any kind; KVK commands/writes/configuration; hydraulics or actuation; PLC/safety mutation; autonomous veterinary diagnosis; medication dosing; real farm data without separate authority; deployment/signing/release/public distribution.

## Current workstream
`HC-S4-001 — HMI prototype workflow and dashboard`

TDD lineage:
- RED head `36608bfcdf02ef4585ee177519d8966ca143dd4b` — HMI workflow tests failed before HMI workflow implementation existed;
- GREEN implementation head `a702a10c366f24178841803e8f55ae2293d4bebc` — awaiting/followed by runtime and docs verification on the PR branch.

## S4 invariants
- dashboard exposes completed-animal and consumed-dressing counters derived from supplied committed values;
- dashboard banner is exactly `Paweł Humięcki the best zootechnik`;
- workflow order is limb → claw → anatomical zone → lesion → treatment;
- selectable zones include toe, sole, white line, axial wall, abaxial wall, heel/bulb, soft heel tissue and interdigital space;
- controlled lesion options include digital dermatitis, interdigital dermatitis, interdigital phlegmon and heel horn erosion;
- out-of-order selections fail closed;
- no KVK machine-control affordance exists in the HMI workflow model.

## Next dependency-ordered step
After controlled merge and repository verification of S4, begin `S5 — local PDF reporting from canonical records` under active `IA-HC-001`.

## Explicit blockers
- Physical KVK integration remains blocked until the actual 2013-generation KVK 801-1 is inspected and photographed.
- Commercial/product naming remains undecided.
