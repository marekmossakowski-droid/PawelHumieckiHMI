# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. Final commercial/product name remains `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`F90 / PHYSICAL PROTOTYPE — P2 HMI LAYOUT IN PROGRESS`

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
- S1 PR #9 → `7467ec4e30b5ecd8831c094bd90ba7d1fe0ad7b2`.
- S2 PR #10 → `c5f60dbf11b04b680c6f51f2e610d33906b08637`.
- S3 PR #11 → `003c8d5d0ab9e026a76e4a519e8b1c246458bc8a`.
- S4 PR #12 → `e4d7d3b21e8baa17c239c6008fdac17a7cbe2e34`.
- S5 PR #13 → `30acc2d9a0833844e7279c68d9884cf9dd124cea`.
- S6 PR #14 → `56da4eaf1316c930ca6095cd068e90bd66e2f624`.
- S7 PR #16 → `0827d0d4b51a0a63c773a1f8ce178d7954dc25a5`.
- Bench MVP closure + IA-HC-002 activation PR #17 → `36ffda3b2363597b8a8aae3746e9d555450c625c`.
- P1 Physical prototype hardware profile PR #18 approved head `452666bfbb5d50d5b3d78bd27f44b739a69e6569` → merge `3425b2be7e581fcb079c8b3688b48533b780a06b`.

## Governance state
- `BENCH MVP`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IMP-HC-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-001`: `FULFILLED FOR AUTHORIZED BENCH SCOPE`.
- `IA-HC-002`: `ACTIVE` for isolated physical HMI prototype work only.
- `HC-P1-001`: `MERGED / VERIFIED`.
- `HC-P2-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`.

## Active authority boundaries
Authorized: isolated synthetic/test-only physical HMI prototype work, 10-inch-class panel profile, low-voltage bench power/wiring isolated from KVK, physical HMI screen/ergonomics work, local persistence/reporting tests, simulator-only serial/RS-485/Modbus tests, BOM and mounting mock-ups.

Not authorized: any electrical/logical connection to real KVK 801-1; live RFID with real farm data; live KVK I/O; CAN/RS-485/Modbus/serial to the machine; KVK commands/writes/configuration/actuation; hydraulics; PLC/safety mutation; autonomous veterinary diagnosis; medication dosing; real farm data; network/cloud service exposure; deployment/signing/release/public distribution.

## Current workstream
`HC-P2-001 — Physical HMI layout and touch mapping`

TDD lineage:
- RED head `8c243af4b136ac7eb5abe30d4dd326f977302a92` — layout tests failed before `hoofcare.physical.layout` existed;
- GREEN head `153a449903ffbb1a66cb237a4454437362f6fe80` — runtime-ci and docs-ci succeeded before reconciliation.

## P2 invariants
- target panel profile is 10.1 inch at 1024×600;
- primary touch targets are at least 48×48 px;
- mapped screens cover dashboard, animal session, limb/claw, zone/lesion, treatment and report summary;
- dashboard preserves `Paweł Humięcki the best zootechnik`, completed-animal counter and consumed-dressings counter;
- layout is isolated synthetic/test-only;
- no machine-control affordance or KVK actuation surface is present.

## Next dependency-ordered step
After controlled merge and repository verification of P2, continue with isolated physical-prototype screen realization and local bench wiring/BOM work under active `IA-HC-002`.

## Explicit blockers
- Physical/live KVK integration remains blocked until the actual circa-2013 KVK 801-1 is inspected and photographed and a separate live observation authority is approved.
- Commercial/product naming remains undecided.
