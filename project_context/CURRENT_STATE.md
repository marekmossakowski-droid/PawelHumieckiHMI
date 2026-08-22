# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` i `HoofCare` są wyłącznie wewnętrznymi nazwami kodowymi. Finalna nazwa komercyjna pozostaje `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`F90 / PHYSICAL PROTOTYPE — P1-P7 MERGED / VERIFIED / CLOSURE READY`

## Canonical repository
`marekmossakowski-droid/PawelHumieckiHMI`

## Governance state
- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-001`: `FULFILLED FOR AUTHORIZED BENCH SCOPE`.
- `HC-S1-001` through `HC-S7-001`: `MERGED / VERIFIED`.
- `HC-BENCH-MVP-CLOSURE-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `HC-P1-001` through `HC-P7-001`: `MERGED / VERIFIED`.
- `IA-HC-002`: nadal `APPROVED / ACTIVE` do czasu zatwierdzenia osobnego closure record; zakres pozostaje wyłącznie izolowany, off-machine, non-actuating, synthetic/test-only.
- `HC-PHYSICAL-PROTOTYPE-CLOSURE-001`: `PROPOSED — PROJECT OWNER APPROVAL REQUIRED`.

## Kanoniczny checkpoint P7
PR #54 approved head `c6083495296a59835a427f035a11ecd859f5be6f` → merge `7e3f4e573bead9664e39422a97ab6cc3ddbb2c41`.

## P7 TDD lineage
- RED `db7b91525cc59a38207db8b8eb40320355ab8c12`.
- implementation attempt `28a97276bf3eb43c977711b7670e6600db87f4fb` — zakres poprawny, lecz test używał niedeklarowanego `pytest`.
- corrected GREEN `17bb4d430fdc96fea7a108b1e5b3152cc5be117a` — projektowy `unittest`, runtime-ci i docs-ci zielone.
- final `c6083495296a59835a427f035a11ecd859f5be6f` — reconciliation + acceptance/closure-readiness.

## Zweryfikowany physical-prototype scope
- 10.1-inch / 1024×600 HMI layout i touch targets;
- dashboard oraz workflow operatora;
- fail-closed navigation/state binding;
- lokalna persistence i restart recovery;
- lokalny canonical PDF wraz z provenance;
- synthetic/test-only acceptance harness;
- brak machine-control surface.

## Active authority boundaries
Authorized w ramach nadal aktywnego `IA-HC-002`: izolowany physical HMI prototype, low-voltage bench, synthetic/test data, simulated RFID/KVK sources, local persistence/reporting/navigation oraz serial/RS-485/Modbus wyłącznie do dedykowanych simulatorów/test equipment.

Not authorized: jakiekolwiek elektryczne lub logiczne połączenie z realnym KVK 801-1; live RFID z real-farm data; live KVK I/O; CAN/RS-485/Modbus/serial do maszyny; KVK commands/writes/configuration/actuation; hydraulika; PLC/safety mutation; autonomous veterinary diagnosis; real-farm data; network/cloud exposure; external report delivery; deployment/signing/release/public distribution.

## Closure state
Po osobnej zgodzie Project Ownera na `HC-PHYSICAL-PROTOTYPE-CLOSURE-001` i kontrolowanym merge:
- `PHYSICAL PROTOTYPE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`;
- `IA-HC-002 = FULFILLED FOR AUTHORIZED PHYSICAL-PROTOTYPE SCOPE`.

## Next phase
Następny etap wymaga dostępu do realnego KVK 801-1 generacji około 2013: zdjęcia, identyfikacja szafy/sterowania/zasilania/sensorów/interfejsów i przygotowanie izolowanego observation-only boundary. Żadna live integracja nie jest obecnie autoryzowana.

## Explicit blockers
- `field_kvk_verified = false`.
- `real_farm_data_used = false`.
- `deployment_ready = false`.
- Dostęp do fizycznego KVK 801-1 i osobne live-observation authority są wymagane przed kolejną fazą integracji.
- Commercial/product naming pozostaje nierozstrzygnięte.
