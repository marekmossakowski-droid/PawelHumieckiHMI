# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` i `HoofCare` są wyłącznie wewnętrznymi nazwami kodowymi. Finalna nazwa komercyjna pozostaje `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`PHYSICAL PROTOTYPE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`

`WAVE R0 SOFTWARE/DOCUMENTATION REMEDIATION = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`

`WAVE R1 DATA INTEGRITY AND CLINICAL PROVENANCE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`

`WAVE R2 GOVERNANCE RECOVERY = CLOSED / MERGED / VERIFIED`

`WAVE R2 REMEDIATION = ACTIVE / R2-D/E REBASE AND REVERIFICATION REQUIRED`

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
- `AUD-HC-007`–`AUD-HC-014`: `CLOSED / VERIFIED`.
- `IMP-HC-005`: `APPROVED / RECOVERY ACTIVE`.
- `IA-HC-006`: `APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-006-RECOVERY-ACTIVATION-001`.
- `UX-HC-001 / ADR-HC-008 / REQ-HC-002`: `APPROVED / BASELINED FOR BOUNDED V0.1 SLICE`.
- `IMP-UX-HC-001`: `APPROVED / ACTIVE`.
- `IA-HC-007`: `APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-007-ACTIVATION-001`.
- `REQ-HC-002-A1`: `APPROVED / BASELINED`.
- `IA-HC-007-A1`: `APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-007-A1-ACTIVATION-001`.
- `IA-HC-007-A1 runtime`: `BOUNDED SYNTHETIC IMPLEMENTATION / A1-5 MERGED AND REPOSITORY VERIFIED / CLOSURE READY`.
- `REQ-HC-002-A1 closure`: `CLOSURE READY — PROJECT OWNER MERGE REQUIRED`.
- `Job statistics and final settlement plan`: `PROPOSED / NOT ACTIVE — NEW OR EXTENDED AUTHORITY REQUIRED`.
- `REQ-HC-002-S1`: `APPROVED / BASELINED — PROJECT OWNER APPROVED VIA PR #94`.
- `IA-HC-007-S1`: `APPROVED / ACTIVE — PROSPECTIVELY VIA HC-IA-HC-007-S1-ACTIVATION-001`.
- `IA-HC-007-S1 runtime`: `S1-1/S1-2 MERGED / VERIFIED; S1-3 BOUNDED SYNTHETIC IMPLEMENTATION / OWNER MERGE REQUIRED`.

Compatibility marker retained: `WAVE R0 SOFTWARE/DOCUMENTATION REMEDIATION = CLOSURE READY / OWNER MERGE REQUIRED`.
Compatibility marker retained: `IMP-HC-003 = FULFILLED FOR AUTHORIZED R0 SCOPE — CLOSURE PENDING OWNER MERGE`.
Compatibility marker retained: `IA-HC-004` remains active until `HC-R0-CLOSURE-001` controlled merge + Repository Verification.
Compatibility marker retained: `WAVE R1 DATA INTEGRITY AND CLINICAL PROVENANCE = CLOSURE READY / OWNER MERGE REQUIRED`.
Compatibility marker retained: `IMP-HC-004 = FULFILLED FOR AUTHORIZED R1 SCOPE — CLOSURE PENDING OWNER MERGE`.
Compatibility marker retained: `IA-HC-005` remains active until `HC-R1-CLOSURE-001` controlled merge + Repository Verification.

## Wave R1 verified results
- R1-A: persistence path safety.
- R1-B/C: durable/versioned persistence, SHA-256 integrity and canonical amendment provenance.
- R1-D/E: domain invariants and operation/resource-scoped idempotency isolation.
- R1-F/G/H: canonical lesion/treatment/material/media records, explicit media provenance and report derivation from committed canonical clinical data.

## Wave R2 governance recovery
- PR #73 pozostawił formalny `IA-HC-006` jako `PROPOSED / NOT ACTIVE`.
- PR #74–#76 są istniejącym stanem `main`, lecz nie stanowią dowodu wcześniejszego authority.
- ich zawartość przeszła świeżą weryfikację recovery: 15/15 testów celowanych i 103/103 pełnej regresji — PASS;
- R2-C semantic status gate jest naprawiany w recovery PR;
- PR #77 pozostaje `OPEN / REBASE AND TDD REVERIFICATION REQUIRED`;
- R2 closure nie jest ustanowione.

## Explicit unresolved dependencies
- `edge_host = EDGE_HOST_REQUIRED / NOT YET SELECTED`.
- `native_dtools_artifact = REQUIRED / NOT YET EVIDENCED`.
- `HW-A1 = WAITING FOR PHYSICAL HARDWARE`.
- `HW-A2 = NOT STARTED / NOT PASS`.
- `HW-A3 = NOT STARTED / NOT PASS`.
- R2 governance recovery i formalne closure pozostają otwarte.

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
