# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. Final commercial/product name remains `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`F90 / PHYSICAL PROTOTYPE — P5 MERGED / VERIFIED / P6 IMPLEMENTED / GREEN / AWAITING PROJECT OWNER APPROVAL`

## Canonical repository
`marekmossakowski-droid/PawelHumieckiHMI`

## Governance state
- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-001`: `FULFILLED FOR AUTHORIZED BENCH SCOPE`.
- `HC-S1-001` through `HC-S7-001`: `MERGED / VERIFIED`.
- `HC-BENCH-MVP-CLOSURE-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-002`: `APPROVED / ACTIVE` only for its literal isolated off-machine / non-actuating / synthetic-test physical-prototype scope.
- `HC-P1-001` through `HC-P5-001`: `MERGED / VERIFIED`.
- `HC-P6-001`: `IMPLEMENTED / GREEN / NOT YET MERGED`.

## Canonical P5 checkpoint
PR #52 approved head `c1d01f66c17be44c07cf3bf3c26e935fd6e368f1` → merge `4484ed4a00c7a756e0663c3cb03c329a6d7dd2c5`.

## P6 TDD lineage
- RED `d78cd81c7bd35e3b2fe632febca104f074214900` — persistence/reporting validation tests added before implementation; runtime-ci failed as expected.
- GREEN `bc3f9301c9e4743b93ec1d3d25970ea8127ba617` — minimal local synthetic/test-only persistence/reporting validator; runtime-ci and docs-ci passed.

## P6 verified invariants
- committed synthetic session snapshots round-trip through the existing local durable store and recover after restart;
- report generation loads the committed session first and fails closed when the session is missing;
- generated report preserves exact `source_session_id` provenance and confirmed animal identity;
- existing canonical local report builder remains the only report-generation path;
- synthetic/test-only remains true;
- KVK connection and real-farm data remain false;
- no network/cloud or external report delivery path exists.

## Active authority boundaries
Authorized: isolated physical HMI prototype work, low-voltage bench work, synthetic/test data, simulated RFID/KVK sources, local persistence/reporting/navigation, and serial/RS-485/Modbus only against dedicated simulators/test equipment.

Not authorized: any electrical or logical connection to real KVK 801-1; live RFID with real-farm data; live KVK I/O; CAN/RS-485/Modbus/serial to the machine; KVK commands/writes/configuration/actuation; hydraulics; PLC/safety mutation; autonomous veterinary diagnosis; real-farm data; network/cloud exposure; deployment/signing/release/public distribution.

## Next state after approved P6 merge
Physical-prototype integration / acceptance and closure-readiness may become NEXT only after controlled merge and Repository Verification of P6.

## Explicit blockers
- Any live KVK integration remains blocked until the actual circa-2013 KVK 801-1 is inspected and photographed and a separate live observation authority is approved.
- Commercial/product naming remains undecided.
