# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. Final commercial/product name remains `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`F90 / PHYSICAL PROTOTYPE — P5 IMPLEMENTED / GREEN / AWAITING PROJECT OWNER APPROVAL`

## Canonical repository
`marekmossakowski-droid/PawelHumieckiHMI`

## Governance state
- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-001`: `FULFILLED FOR AUTHORIZED BENCH SCOPE`.
- `HC-S1-001` through `HC-S7-001`: `MERGED / VERIFIED`.
- `HC-BENCH-MVP-CLOSURE-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-002`: `APPROVED / ACTIVE` only for its literal isolated off-machine / non-actuating / synthetic-test physical-prototype scope.
- `HC-P1-001` through `HC-P4-001`: `MERGED / VERIFIED`.
- `HC-P5-001`: `IMPLEMENTED / GREEN / NOT YET MERGED`.

## Canonical approved checkpoint before P5
PR #43 merge `e6b62b4ffaf73103d57af24b8b60b5886643bb1c`; tree `c3bb64e394df8bb287fef5108dffa9210d8d4cb6`. PR #51 restored this exact tree on `main` before fresh P5 work began.

## P5 TDD lineage
- RED `3f4db8258a85b6e2cc6349a5bb03d982066db732` — navigation contract added before implementation.
- GREEN `de8dec19bc820b90bfebe4df669eb661e0af2add` — minimal isolated physical navigation controller.

## P5 verified invariants
- local navigation follows dashboard → animal session → limb/claw → zone/lesion → treatment → report summary;
- identity advances only when status is exactly `CONFIRMED`;
- limb/claw, zone/lesion and treatment selections are order constrained;
- machine-control-like actions fail closed;
- synthetic/test-only remains true;
- KVK connection and real-farm data remain false.

## Active authority boundaries
Authorized: isolated physical HMI prototype work, low-voltage bench work, synthetic/test data, simulated RFID/KVK sources, local persistence/reporting/navigation, and serial/RS-485/Modbus only against dedicated simulators/test equipment.

Not authorized: any electrical or logical connection to real KVK 801-1; live RFID with real-farm data; live KVK I/O; CAN/RS-485/Modbus/serial to the machine; KVK commands/writes/configuration/actuation; hydraulics; PLC/safety mutation; autonomous veterinary diagnosis; real-farm data; network/cloud exposure; deployment/signing/release/public distribution.

## Next state after approved P5 merge
`HC-P6-001 — Physical persistence and reporting validation` may become NEXT only after controlled merge and repository verification of P5.

## Explicit blockers
- Any live KVK integration remains blocked until the actual circa-2013 KVK 801-1 is inspected and photographed and a separate live observation authority is approved.
- Commercial/product naming remains undecided.
