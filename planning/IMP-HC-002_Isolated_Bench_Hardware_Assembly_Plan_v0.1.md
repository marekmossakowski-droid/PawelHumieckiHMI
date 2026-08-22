# IMP-HC-002 — Isolated Bench Hardware Assembly Plan v0.1

## Status
`APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA PR #57`

## Cel
Zmontować i zweryfikować rzeczywisty, izolowany bench prototype HMI bez jakiegokolwiek elektrycznego, logicznego lub mechanicznego połączenia z realnym KVK 801-1.

## Selected procurement target
- HMI: `Kinco GL100E` — 10.1-inch TFT, 1024×600, DC 10–28 V, Ethernet, COM0 RS232/RS485/RS422, COM2 RS232.
- I/O: `Kinco KS123-14DR` — 24 VDC, 8 cyfrowych wejść DC24V, 6 wyjść przekaźnikowych, Modbus slave capability.
- Zasilanie 24 VDC: istniejące po stronie Project Ownera.
- RFID: `DEFERRED` — nie jest wymagany do tego planu.

## Architektura bench
`24 VDC → GL100E ↔ RS485 / Modbus RTU ↔ KS123-14DR → wyłącznie przyciski i lampki testowe`

Nie wolno łączyć bench prototype z KVK 801-1, jego PLC, szafą, przewodami sygnałowymi, magistralami ani hydrauliką.

## Kroki realizacyjne
1. `HW-A1 — Goods-in verification`
   - potwierdzić exact modele i tabliczki znamionowe GL100E i KS123-14DR;
   - sprawdzić brak uszkodzeń, kompletność zacisków i dokumentacji;
   - zapisać zdjęcia sprzętu jako evidence bez danych gospodarstwa.

2. `HW-A2 — Isolated 24 VDC bench wiring`
   - wykonać osobne zabezpieczone zasilanie 24 VDC HMI i I/O;
   - potwierdzić polaryzację i napięcie przed podaniem zasilania;
   - brak przewodów do KVK.

3. `HW-A3 — HMI commissioning`
   - uruchomić GL100E;
   - załadować testowy projekt DTools zgodny z P2–P7;
   - zweryfikować 1024×600, dotyk i podstawową nawigację.

4. `HW-A4 — RS485 / Modbus RTU bench link`
   - połączyć GL100E wyłącznie z KS123-14DR;
   - ustalić parametry komunikacji i adres slave;
   - zweryfikować odczyt DI i testowe sterowanie wyjściami przekaźnikowymi wyłącznie do lampek/test load.

5. `HW-A5 — Operator workflow bench test`
   - dashboard → sesja zwierzęcia → racica → strefa/schorzenie → zabieg → raport;
   - wyłącznie synthetic/test data;
   - potwierdzić liczniki krów i opatrunków oraz banner `Paweł Humięcki the best zootechnik`.

6. `HW-A6 — Restart / persistence / reporting test`
   - restart HMI/edge path;
   - potwierdzić recovery sesji testowej;
   - wygenerować lokalny raport PDF z synthetic provenance.

7. `HW-A7 — Bench acceptance`
   - pełny test operatora w rękawicach;
   - negative tests komunikacji;
   - potwierdzić brak machine-control surface i brak jakiegokolwiek połączenia do KVK.

## Acceptance criteria
- GL100E uruchamia właściwy projekt HMI;
- KS123-14DR komunikuje się stabilnie po izolowanym RS485/Modbus RTU;
- 8 DI i 6 relay DO są możliwe do zweryfikowania na test load;
- cały workflow P2–P7 działa na rzeczywistym bench hardware;
- restart i raportowanie są zweryfikowane;
- `synthetic/test-only = true`;
- `real_farm_data_used = false`;
- `kvk_connected = false`;
- żadne wyjście nie steruje elementem KVK ani innym rzeczywistym aktuátorem maszyny.

## Explicit exclusions
Plan nie obejmuje:
- realnego KVK I/O;
- podłączenia CAN/RS485/Modbus/serial do KVK;
- hydrauliki, elektrozaworów, bram, silników, wciągarek i innych aktuatorów;
- PLC/safety mutation;
- live RFID i real-farm data;
- network/cloud service exposure;
- external report delivery;
- deployment, signing, release ani public distribution.

## Verification model
Każdy etap ma powstać jako najmniejszy niezależny inkrement z verification evidence przed przejściem do kolejnego. Runtime/software changes, jeśli będą konieczne do fizycznego sprzętu, wymagają zachowania obecnych fail-closed invariants i osobnego RED → GREEN lineage.

## Exit
`ISOLATED BENCH HARDWARE = ASSEMBLED / VERIFIED / RECONCILED`

Po exit F80 nadal pozostaje `BLOCKED_BY_SITE_ACCESS` do czasu zdjęć i audytu rzeczywistego KVK 801-1.
