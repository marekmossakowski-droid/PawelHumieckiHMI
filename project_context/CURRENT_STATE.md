# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` i `HoofCare` są wyłącznie wewnętrznymi nazwami kodowymi. Finalna nazwa komercyjna pozostaje `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`PHYSICAL PROTOTYPE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`

`WAVE R0 REMEDIATION = ACTIVE / R0-A..R0-C IMPLEMENTED / R0-D CURRENT`

`F75 / ISOLATED BENCH HARDWARE ASSEMBLY = ACTIVE`

`CURRENT PHYSICAL STEP = HW-A1 — GOODS-IN VERIFICATION / WAITING FOR PHYSICAL HARDWARE`

Compatibility marker for canonical governance CI: `CURRENT STEP = HW-A1 — GOODS-IN VERIFICATION / WAITING FOR PHYSICAL HARDWARE`.

## Canonical repository
`marekmossakowski-droid/PawelHumieckiHMI`

## Governance state
- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-001`: `FULFILLED FOR AUTHORIZED BENCH SCOPE`.
- `HC-BENCH-MVP-CLOSURE-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `HC-PHYSICAL-PROTOTYPE-CLOSURE-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-002`: `FULFILLED FOR AUTHORIZED PHYSICAL-PROTOTYPE SCOPE`.
- `IMP-HC-002 — Isolated Bench Hardware Assembly Plan`: `APPROVED / ACTIVE`.
- `IA-HC-003 — Isolated Bench Hardware Assembly Authority`: `APPROVED / ACTIVE`.
- `IMP-HC-003 — Wave R0 Remediation Plan`: `APPROVED / ACTIVE`.
- `IA-HC-004 — Wave R0 Remediation Authority`: `APPROVED / ACTIVE`.

## Audit/remediation state
`HC-AUDIT-001` recorded 25 P0/P1/P2 findings.

R0 completed technical slices:
- `R0-A / AUD-HC-006`: exact hardware profile = Kinco GL100E + KS123-14DR, 8DI/6 relay DO, existing isolated 24 VDC;
- `R0-B / AUD-HC-003`: structurally valid deterministic local PDF;
- `R0-C / AUD-HC-004/005`: durable completion and evidence-derived acceptance.

Current R0-D work establishes:
- deterministic `GL100E-DTOOLS-SPEC-001`;
- requirement-level matrix `HC-REQ-TRACE-001`;
- documentation/lifecycle reconciliation `HC-R0-D-DOC-RECON-001`.

## Selected bench hardware target
- `Kinco GL100E`, 10.1 inch, 1024×600;
- `Kinco KS123-14DR`, 8 DI + 6 relay DO;
- istniejące izolowane zasilanie 24 VDC, wymagające fizycznej weryfikacji;
- RFID pozostaje odłożone.

Bench I/O architecture: `24 VDC → GL100E ↔ RS485 / Modbus RTU ↔ KS123-14DR → dedicated test buttons/lamps/test loads`.

Canonical persistence/reporting architecture remains HMI-independent. Concrete edge/application runtime host remains `EDGE_HOST_REQUIRED / NOT YET SELECTED`.

## DTools / application state
`GL100E-DTOOLS-SPEC-001` defines exact 1024×600 screens, widget geometry, navigation and bench Modbus realization rules.

A real Kinco DTools project/export does **not** yet exist in canonical evidence and remains `NATIVE_DTOOLS_ARTIFACT_REQUIRED BEFORE HW-A3 PASS`.

## Current execution state
`HW-A1 — Goods-in verification` cannot PASS until physical GL100E and KS123-14DR are received and evidenced.

After positive HW-A1 the physical sequence remains:
`HW-A2 — isolated 24 VDC bench wiring → HW-A3 — GL100E project compile/upload and first real panel test`.

## Active authority boundaries
Authorized: isolated off-machine bench and approved R0 local synthetic/test-only remediation only.

Not authorized: any electrical/logical connection with real KVK 801-1; KVK PLC/safety/sensors/actuators/cabinet/machine buses; CAN/RS485/Modbus/serial to KVK; KVK commands/writes/configuration/actuation; hydraulics; PLC/safety mutation; live RFID/real-farm data; network/cloud; external report delivery; deployment/signing/release/public distribution.

## Explicit fail-closed state
- `field_kvk_verified = false`.
- `real_farm_data_used = false`.
- `deployment_ready = false`.
- `kvk_connected = false`.
- `edge_host = EDGE_HOST_REQUIRED`.
- `native_dtools_artifact = REQUIRED / NOT YET EVIDENCED`.

## Next external dependency
For HW-A1 Project Owner must provide real-device evidence after delivery:
- GL100E front/back + model/serial label;
- KS123-14DR front/terminals + model/serial label;
- visible power/communication terminals;
- packaging/accessories state.

## F80
Audit of the real KVK 801-1 circa-2013 remains `BLOCKED_BY_SITE_ACCESS`. No live integration authority is active.
