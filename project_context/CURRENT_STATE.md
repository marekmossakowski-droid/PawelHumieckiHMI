# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` i `HoofCare` są wyłącznie wewnętrznymi nazwami kodowymi. Finalna nazwa komercyjna pozostaje `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`PHYSICAL PROTOTYPE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`

`WAVE R0 SOFTWARE/DOCUMENTATION REMEDIATION = CLOSURE READY / OWNER MERGE REQUIRED`

`F75 / ISOLATED BENCH HARDWARE ASSEMBLY = ACTIVE`

`CURRENT PHYSICAL STEP = HW-A1 — GOODS-IN VERIFICATION / WAITING FOR PHYSICAL HARDWARE`

Compatibility marker for canonical governance CI: `CURRENT STEP = HW-A1 — GOODS-IN VERIFICATION / WAITING FOR PHYSICAL HARDWARE`.

## Governance state
- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-001`: `FULFILLED FOR AUTHORIZED BENCH SCOPE`.
- `IA-HC-002`: `FULFILLED FOR AUTHORIZED PHYSICAL-PROTOTYPE SCOPE`.
- `IMP-HC-002`: `APPROVED / ACTIVE`.
- `IA-HC-003`: `APPROVED / ACTIVE`.
- `IMP-HC-003`: `FULFILLED FOR AUTHORIZED R0 SCOPE — CLOSURE PENDING OWNER MERGE`.
- `IA-HC-004`: remains active until `HC-R0-CLOSURE-001` controlled merge + Repository Verification.

## Wave R0 verified results
- R0-A: exact Kinco GL100E + KS123-14DR hardware profile.
- R0-B: structurally valid deterministic local PDF.
- R0-C: durable completion + evidence-derived acceptance.
- R0-D: exact GL100E/DTools realization specification + requirement-level traceability + lifecycle/documentation reconciliation.

## Explicit unresolved dependencies
- `edge_host = EDGE_HOST_REQUIRED / NOT YET SELECTED`.
- `native_dtools_artifact = REQUIRED / NOT YET EVIDENCED`.
- `HW-A1 = WAITING FOR PHYSICAL HARDWARE`.
- `HW-A2 = NOT STARTED / NOT PASS`.
- `HW-A3 = NOT STARTED / NOT PASS`.
- R1/R2 audit findings remain open.

## Selected bench hardware target
- Kinco GL100E, 10.1 inch, 1024×600;
- Kinco KS123-14DR, 8 DI + 6 relay DO;
- existing isolated 24 VDC subject to physical verification;
- RFID deferred;
- local RS485/Modbus only between GL100E and KS123-14DR.

## Next physical dependency
For HW-A1 Project Owner must provide real-device evidence after delivery:
- GL100E front/back + model/serial label;
- KS123-14DR front/terminals + model/serial label;
- visible power/communication terminals;
- packaging/accessories state.

## Authority boundary
No real KVK I/O, machine CAN/RS-485/Modbus/serial, commands/writes/configuration/actuation, hydraulics, PLC/safety mutation, live RFID/real-farm data, network/cloud exposure, external report delivery, deployment, signing, release or public distribution is authorized.

## F80
Audit of the real KVK 801-1 circa-2013 remains `BLOCKED_BY_SITE_ACCESS`. No live integration authority is active.
