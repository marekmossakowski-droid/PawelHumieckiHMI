# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` i `HoofCare` są wyłącznie wewnętrznymi nazwami kodowymi. Finalna nazwa komercyjna pozostaje `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`PHYSICAL PROTOTYPE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`

`F75 / ISOLATED BENCH HARDWARE ASSEMBLY = ACTIVE`

`CURRENT STEP = HW-A1 — GOODS-IN VERIFICATION / WAITING FOR PHYSICAL HARDWARE`

## Canonical repository
`marekmossakowski-droid/PawelHumieckiHMI`

## Governance state
- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-001`: `FULFILLED FOR AUTHORIZED BENCH SCOPE`.
- `HC-S1-001` through `HC-S7-001`: `MERGED / VERIFIED`.
- `HC-BENCH-MVP-CLOSURE-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `HC-P1-001` through `HC-P7-001`: `MERGED / VERIFIED`.
- `HC-PHYSICAL-PROTOTYPE-CLOSURE-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-002`: `FULFILLED FOR AUTHORIZED PHYSICAL-PROTOTYPE SCOPE`.
- `IMP-HC-002 — Isolated Bench Hardware Assembly Plan`: `APPROVED / ACTIVE`.
- `IA-HC-003 — Isolated Bench Hardware Assembly Authority`: `APPROVED / ACTIVE`.

## Canonical activation checkpoint
PR #57 approved head `15aea194107cebc2fada2c857f90227fd0a8a1e6` → merge `52d65b18f966f553501a7829855f23b7390762a6` → Repository Verification.

## Selected bench hardware target
- `Kinco GL100E` HMI;
- `Kinco KS123-14DR` I/O;
- istniejące izolowane zasilanie 24 VDC;
- RFID pozostaje odłożone.

Bench architecture: `24 VDC → GL100E ↔ RS485 / Modbus RTU ↔ KS123-14DR → dedicated test buttons/lamps/test loads`.

## Current execution state
`HW-A1 — Goods-in verification` jest aktywnym krokiem, ale nie może być oznaczony jako wykonany do czasu fizycznego otrzymania GL100E i KS123-14DR oraz zebrania evidence z rzeczywistych urządzeń.

Po pozytywnym HW-A1 następny krok to `HW-A2 — Isolated 24 VDC bench wiring`.

## Active authority boundaries
Authorized: wyłącznie izolowany off-machine bench w granicach `IA-HC-003`, synthetic/test data, GL100E, KS123-14DR, local RS485/Modbus między tymi dwoma urządzeniami, testowe DI/DO i dedicated non-machine test loads.

Not authorized: jakiekolwiek elektryczne/logiczne połączenie z KVK 801-1; KVK PLC/safety/sensors/actuators/cabinet/machine buses; CAN/RS485/Modbus/serial do KVK; commands/writes/configuration/actuation do KVK; hydraulika; PLC/safety mutation; live RFID/real-farm data; network/cloud; external report delivery; deployment/signing/release/public distribution.

## Explicit fail-closed state
- `field_kvk_verified = false`.
- `real_farm_data_used = false`.
- `deployment_ready = false`.
- `kvk_connected = false`.

## Next external dependency
Do zamknięcia `HW-A1` Project Owner musi dostarczyć rzeczywiste urządzenia lub zdjęcia po dostawie:
- GL100E front/back + tabliczka/model/serial;
- KS123-14DR front/terminals + tabliczka/model/serial;
- widoczne zaciski zasilania i komunikacji;
- zdjęcie stanu opakowania/akcesoriów.

## F80
Audyt realnego KVK 801-1 generacji około 2013 pozostaje `BLOCKED_BY_SITE_ACCESS`. Żadna live integration authority nie jest aktywna.
