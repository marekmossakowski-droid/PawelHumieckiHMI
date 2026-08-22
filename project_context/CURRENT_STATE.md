# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. Final commercial/product name remains `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`F90 / PHYSICAL PROTOTYPE — P6 MERGED / VERIFIED / P7 IMPLEMENTED / GREEN / AWAITING PROJECT OWNER APPROVAL`

## Canonical repository
`marekmossakowski-droid/PawelHumieckiHMI`

## Governance state
- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-001`: `FULFILLED FOR AUTHORIZED BENCH SCOPE`.
- `HC-S1-001` through `HC-S7-001`: `MERGED / VERIFIED`.
- `HC-BENCH-MVP-CLOSURE-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-002`: `APPROVED / ACTIVE` only for its literal isolated off-machine / non-actuating / synthetic-test physical-prototype scope.
- `HC-P1-001` through `HC-P6-001`: `MERGED / VERIFIED`.
- `HC-P7-001`: `IMPLEMENTED / GREEN / NOT YET MERGED`.

## Canonical P6 checkpoint
PR #53 approved head `4ab76ad972ccef8c74dabb75c9368d4ae3adcaa9` → merge `b4a4417c6d719d8f9db0a14db48871f863cb4440`.

## P7 TDD lineage
- RED `db7b91525cc59a38207db8b8eb40320355ab8c12` — physical-prototype acceptance contract added before implementation; runtime-ci failed as expected because the acceptance module did not exist.
- implementation attempt `28a97276bf3eb43c977711b7670e6600db87f4fb` — acceptance harness added, but runtime-ci remained red because the new test used an undeclared `pytest` dependency; implementation scope was unchanged.
- corrected GREEN `17bb4d430fdc96fea7a108b1e5b3152cc5be117a` — project-native `unittest` harness; runtime-ci and docs-ci passed.

## P7 verified invariants
- physical acceptance verifies the existing 10.1-inch / 1024×600 screen and touch-target invariants;
- local operator navigation reaches report summary through the P5 fail-closed state model;
- committed synthetic session persists and recovers through the P6 local store;
- canonical local PDF report is generated from committed session provenance;
- synthetic/test-only remains true;
- KVK connection and real-farm data remain false;
- machine-control actions and controls remain absent / rejected;
- `field_kvk_verified = false`, `real_farm_data_used = false`, `deployment_ready = false` remain explicit.

## Active authority boundaries
Authorized: isolated physical HMI prototype work, low-voltage bench work, synthetic/test data, simulated RFID/KVK sources, local persistence/reporting/navigation, and serial/RS-485/Modbus only against dedicated simulators/test equipment.

Not authorized: any electrical or logical connection to real KVK 801-1; live RFID with real-farm data; live KVK I/O; CAN/RS-485/Modbus/serial to the machine; KVK commands/writes/configuration/actuation; hydraulics; PLC/safety mutation; autonomous veterinary diagnosis; real-farm data; network/cloud exposure; deployment/signing/release/public distribution.

## Next state after approved P7 merge
After controlled merge and Repository Verification, the isolated physical-prototype implementation may be declared `CLOSURE READY` and a separate closure record may be prepared. This does not authorize field/KVK integration.

## Explicit blockers
- Any live KVK integration remains blocked until the actual circa-2013 KVK 801-1 is inspected and photographed and a separate live observation authority is approved.
- Commercial/product naming remains undecided.
