# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` i `HoofCare` są wyłącznie wewnętrznymi nazwami kodowymi. Finalna nazwa komercyjna pozostaje `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`PHYSICAL PROTOTYPE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`

`WAVE R0 SOFTWARE/DOCUMENTATION REMEDIATION = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`

`WAVE R1 DATA INTEGRITY AND CLINICAL PROVENANCE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`

`WAVE R2 UX, OBSERVABILITY AND ENGINEERING QUALITY = REMEDIATED / CLOSURE PENDING`

`F75 / ISOLATED BENCH HARDWARE ASSEMBLY = ACTIVE`

`CURRENT PHYSICAL STEP = HW-A1 — GOODS-IN VERIFICATION / WAITING FOR PHYSICAL HARDWARE`

Compatibility marker for canonical governance CI: `CURRENT STEP = HW-A1 — GOODS-IN VERIFICATION / WAITING FOR PHYSICAL HARDWARE`.

## Governance state
- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-001`: `FULFILLED FOR AUTHORIZED BENCH SCOPE`.
- `IA-HC-002`: `FULFILLED FOR AUTHORIZED PHYSICAL-PROTOTYPE SCOPE`.
- `IMP-HC-002`: `APPROVED / ACTIVE`.
- `IA-HC-003 — Isolated Bench Hardware Assembly Authority`: `APPROVED / ACTIVE`.
- `IMP-HC-003`: `FULFILLED FOR AUTHORIZED R0 SCOPE`.
- `IA-HC-004`: `FULFILLED FOR AUTHORIZED R0 SCOPE`.
- `IMP-HC-004`: `FULFILLED FOR AUTHORIZED R1 SCOPE`.
- `IA-HC-005`: `FULFILLED FOR AUTHORIZED R1 SCOPE`.
- `IMP-HC-005 — Wave R2 UX, Observability and Engineering Quality`: `APPROVED / ACTIVE — CLOSURE PENDING`.
- `IA-HC-006`: `APPROVED / ACTIVE — CLOSURE PENDING`.
- `AUD-HC-007`–`AUD-HC-014`: `CLOSED / VERIFIED`.
- `AUD-HC-018`–`AUD-HC-025`: `REMEDIATED / CLOSURE PENDING`.

Compatibility marker retained: `WAVE R0 SOFTWARE/DOCUMENTATION REMEDIATION = CLOSURE READY / OWNER MERGE REQUIRED`.
Compatibility marker retained: `IMP-HC-003 = FULFILLED FOR AUTHORIZED R0 SCOPE — CLOSURE PENDING OWNER MERGE`.
Compatibility marker retained: `IA-HC-004` remains active until `HC-R0-CLOSURE-001` controlled merge + Repository Verification.
Compatibility marker retained: `WAVE R1 DATA INTEGRITY AND CLINICAL PROVENANCE = CLOSURE READY / OWNER MERGE REQUIRED`.
Compatibility marker retained: `IMP-HC-004 = FULFILLED FOR AUTHORIZED R1 SCOPE — CLOSURE PENDING OWNER MERGE`.
Compatibility marker retained: `IA-HC-005` remains active until `HC-R1-CLOSURE-001` controlled merge + Repository Verification.

## Wave R2 verified results
- R2-A: complete local HMI navigation semantics and concrete GL100E 1024×600 geometry checks.
- R2-B: typed observation provenance/quality/staleness and allowlisted local bench capabilities.
- R2-C: runtime regression on `main`, bounded static/coverage checks and stronger semantic documentation CI.
- R2-D/E: reproducible synthetic-only local runtime package/config/entrypoint/restart procedure and RFID identity derived from observation payload with fail-closed mismatch behavior.

## Explicit unresolved dependencies
- `edge_host = EDGE_HOST_REQUIRED / NOT YET SELECTED` for physical deployment; the R2 local runtime package does not select a physical host.
- `native_dtools_artifact = REQUIRED / NOT YET EVIDENCED`.
- `HW-A1 = WAITING FOR PHYSICAL HARDWARE`.
- `HW-A2 = NOT STARTED / NOT PASS`.
- `HW-A3 = NOT STARTED / NOT PASS`.
- R2 formal closure/reconciliation remains pending Project Owner approval after final diff.

## Selected bench hardware target
- Kinco GL100E, 10.1 inch, 1024×600;
- Kinco KS123-14DR, 8 DI + 6 relay DO;
- existing isolated 24 VDC subject to physical verification;
- RFID deferred;
- local RS485/Modbus only between GL100E and KS123-14DR.

Order evidence exists for GL100E and KS123-14DR, but physical receipt/inspection remains required before HW-A1 PASS.

## Explicit fail-closed state
- `field_kvk_verified = false`.
- `deployment_ready = false`.
- `kvk_connected = false`.
- `real_farm_data_used = false`.

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
