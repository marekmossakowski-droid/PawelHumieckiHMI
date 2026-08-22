# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` i `HoofCare` są wyłącznie wewnętrznymi nazwami kodowymi. Finalna nazwa komercyjna pozostaje `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`PHYSICAL PROTOTYPE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`

`NEXT = F75 / ISOLATED BENCH HARDWARE ASSEMBLY READINESS — PROPOSED / NOT ACTIVE`

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
- `IMP-HC-002 — Isolated Bench Hardware Assembly Plan`: `PROPOSED / NOT ACTIVE`.
- `IA-HC-003 — Isolated Bench Hardware Assembly Authority`: `PROPOSED / NOT ACTIVE`.

## Kanoniczne closure
PR #55 approved head `f7faea3620560ac409e23c0399a7f7f1c26a17dc` → merge `ad8b164ce3517064a1de92c986b27a8bfd024b8b` → Repository Verification.

## Zweryfikowany physical-prototype scope
- 10.1-inch / 1024×600 HMI layout i touch targets;
- dashboard oraz workflow operatora;
- fail-closed navigation/state binding;
- lokalna persistence i restart recovery;
- lokalny canonical PDF wraz z provenance;
- synthetic/test-only acceptance harness;
- brak machine-control surface.

## Selected bench hardware target
Project Owner wybrał do zakupu/uruchomienia bench:
- `Kinco GL100E` HMI;
- `Kinco KS123-14DR` I/O;
- istniejące zasilanie 24 VDC;
- RFID pozostaje odłożone na później.

Planowany bench link: `GL100E ↔ RS485 / Modbus RTU ↔ KS123-14DR`, wyłącznie z dedykowanymi przyciskami/lampkami/test load.

## Authority boundaries po closure
Brak aktywnego authority dla nowego hardware assembly ani dla live KVK integration. `IA-HC-003` jest wyłącznie proposed i wymaga osobnej Project Owner activation decision.

Not authorized: jakiekolwiek elektryczne lub logiczne połączenie z realnym KVK 801-1; live RFID z real-farm data; live KVK I/O; CAN/RS-485/Modbus/serial do maszyny; KVK commands/writes/configuration/actuation; hydraulika; PLC/safety mutation; autonomous veterinary diagnosis; real-farm data; network/cloud exposure; external report delivery; deployment/signing/release/public distribution.

## Next phase
Po aktywacji `IA-HC-003` można wykonać wyłącznie izolowany bench hardware assembly zgodnie z `IMP-HC-002`: goods-in verification → 24 VDC bench wiring → GL100E commissioning → RS485/Modbus link do KS123-14DR → operator workflow → restart/reporting → bench acceptance.

F80, czyli audyt realnego KVK 801-1 generacji około 2013, pozostaje `BLOCKED_BY_SITE_ACCESS` do czasu zdjęć i dostępu do maszyny.

## Explicit blockers
- `IA-HC-003 = PROPOSED / NOT ACTIVE`;
- `field_kvk_verified = false`;
- `real_farm_data_used = false`;
- `deployment_ready = false`;
- dostęp do fizycznego KVK 801-1 jest wymagany przed F80;
- osobne implementation plan i Project Owner authority są wymagane przed jakąkolwiek observation-only integracją;
- commercial/product naming pozostaje nierozstrzygnięte.
