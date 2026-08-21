# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. Final commercial/product name remains `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`F90 / PHYSICAL PROTOTYPE — P5 MERGED / VERIFIED / P6 IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`

## Canonical repository
`marekmossakowski-droid/PawelHumieckiHMI`

## Canonical checkpoints
- Bench MVP closure PR #17 → `36ffda3b2363597b8a8aae3746e9d555450c625c`.
- IA-HC-002 activation PR #27 → `3eb278f7a480734045027393a53a76f6cdc03f03`.
- P1 PR #29 → `ec2cea9b144256baca29cd1ea2f03bf0dfcf6def`.
- P2 PR #31 → `047e5bba348eaea0b52103230ec589df6f857036`.
- P3 PR #33 → `a48eb7a8b1de94758e6c74945f710ff5084a4b8f`.
- P4 approved PR #35 → merge `c5101eb15933bc76b76a86dd3e8ed4f78141875f`; corrected/restored through approved PR #43 → `e6b62b4ffaf73103d57af24b8b60b5886643bb1c`.
- P5 approved head `20a2a7324e76a2feeedfe5a864320159f36b82d4` → PR #45 merge `0676c5dd2f68f0e7a9322b003b1fa2da861d506e`.

## Governance state
- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-001`: `FULFILLED FOR AUTHORIZED BENCH SCOPE`.
- `HC-S1-001` through `HC-S7-001`: `MERGED / VERIFIED`.
- `HC-BENCH-MVP-CLOSURE-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-002`: `APPROVED / ACTIVE` only for isolated off-machine / non-actuating / synthetic-test physical-prototype work.
- `HC-P1-001` through `HC-P5-001`: `MERGED / VERIFIED`.
- `HC-P6-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`.

## Active authority boundaries
Authorized: isolated physical HMI prototype work, low-voltage bench work, synthetic/test data, simulated RFID/KVK sources, local persistence/reporting/navigation, and serial/RS-485/Modbus only against dedicated simulators/test equipment.

Not authorized: any electrical or logical connection to real KVK 801-1; live RFID with real-farm data; live KVK I/O; CAN/RS-485/Modbus/serial to the machine; KVK commands/writes/configuration/actuation; hydraulics; PLC/safety mutation; autonomous veterinary diagnosis; real-farm data; network/cloud exposure; external report delivery; deployment/signing/release/public distribution.

## P5 verified invariants
- local operator navigation follows dashboard → animal session → limb/claw → zone/lesion → treatment → report summary;
- identity must be exactly `CONFIRMED` before advancing;
- selections are order constrained and invalid transitions fail closed;
- machine-control-like actions are explicitly rejected;
- KVK connection and real-farm data remain disabled.

## P6 current invariants
- committed synthetic sessions round-trip through local durable storage and recover after restart;
- local canonical PDF is generated only from committed session data;
- missing/uncommitted session fails closed;
- report preserves source-session provenance and synthetic-test-only marking;
- no KVK, cloud, real-farm or actuation path is added.

TDD lineage: RED `02e1468e6b3103f23fecabee7b25862647f0bd62` → GREEN `0e002a4f336f87a14cf377e56d390e2da57746fc`.

## Current workstream
`HC-P6-001 — Physical persistence and reporting validation`

## Explicit blockers
- Any live KVK integration remains blocked until the actual circa-2013 KVK 801-1 is inspected and photographed and a separate live observation authority is approved.
- Commercial/product naming remains undecided.
