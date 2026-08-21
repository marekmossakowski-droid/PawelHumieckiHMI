# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. Final commercial/product name remains `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`F80 / BENCH IMPLEMENTATION — S5 LOCAL CANONICAL PDF REPORTING MERGED / VERIFIED; S6 NEXT`

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
- S3 Local HMI-edge contract PR #11 → `003c8d5d0ab9e026a76e4a519e8b1c246458bc8a`.
- S4 HMI prototype workflow PR #12 approved head `c0c925a8a5f8b52ad2eac6cb307f7304959f4229`, merged as `e4d7d3b21e8baa17c239c6008fdac17a7cbe2e34`.
- S5 Local canonical PDF reporting PR #13 approved head `c3a2117126ee44e3811441ee3fc0f2c494ed93ab`, merged as `30acc2d9a0833844e7279c68d9884cf9dd124cea`.

## Governance state
- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `APPROVED / BASELINED`.
- `IA-HC-001`: `ACTIVE` for bounded local bench MVP only.
- Runtime implementation authority: `ESTABLISHED — BOUNDED BENCH ONLY`.
- `HC-S1-001`: `MERGED / VERIFIED`.
- `HC-S2-001`: `MERGED / VERIFIED`.
- `HC-S3-001`: `MERGED / VERIFIED`.
- `HC-S4-001`: `MERGED / VERIFIED`.
- `HC-S5-001`: `MERGED / VERIFIED`.

## Active authority boundaries
Authorized: synthetic/test data, domain/session core, local persistence/recovery, local HMI↔edge contract, HMI prototype workflow, local PDF reporting, simulated RFID/KVK observations, tests.

Not authorized: live KVK I/O of any kind; KVK commands/writes/configuration; hydraulics or actuation; PLC/safety mutation; autonomous veterinary diagnosis; medication dosing; real farm data without separate authority; network/cloud delivery; deployment/signing/release/public distribution.

## Last closed workstream
`HC-S5-001 — Local canonical PDF reporting`

TDD lineage:
- RED head `1581c6393319e6ab3905e3132f8ead55c6f4bfb9` — report contract/PDF tests failed before reporting implementation existed;
- GREEN implementation head `6e9597a8b834f5b80a2ab55bfd931bd6d4b5dc01`;
- final approved head `c3a2117126ee44e3811441ee3fc0f2c494ed93ab`;
- merged / Repository Verified as `30acc2d9a0833844e7279c68d9884cf9dd124cea`.

## S5 invariants
- reports are generated only from committed canonical records;
- report provenance includes report ID, generation timestamp and source session ID;
- audience sections exist for farmer, veterinarian, zootechnician, nutritionist and technical service;
- report output carries an explicit non-diagnostic veterinary disclaimer;
- bench output is marked synthetic/test-only;
- media references are carried as explicit provenance references;
- output remains local; no email/cloud/network delivery is introduced.

## Next dependency-ordered step
Begin `S6 — simulated RFID and simulated KVK observation adapters` under active `IA-HC-001`, using synthetic/test data only and preserving the observation-only KVK boundary.

## Explicit blockers
- Physical KVK integration remains blocked until the actual 2013-generation KVK 801-1 is inspected and photographed.
- Commercial/product naming remains undecided.
