# HC-IA-HC-006-RECOVERY-ACTIVATION-001 — R2 Governance Recovery and Prospective Activation

## Status
`APPROVED — PROJECT OWNER DECISION 2026-08-23 / REPOSITORY MATERIALIZATION PENDING CONTROLLED MERGE`

## Wykryta luka
PR #73 opublikował `IMP-HC-005` i `IA-HC-006` wyłącznie jako `PROPOSED / NOT ACTIVE`. Kanoniczny dokument authority nie został następnie aktywowany przed merge PR #74, #75 i #76, mimo że opisy tych PR-ów używały określenia `under active IA-HC-006`.

Ta luka jest błędem governance. Zielone CI i obecność zmian na `main` nie stanowią dowodu wcześniejszego authority.

## Decyzja Project Ownera
23 sierpnia 2026 Project Owner zaakceptował rekomendację przeprowadzenia autonomicznego `R2 GOVERNANCE RECOVERY`.

Decyzja:
- zatwierdza `IMP-HC-005` jako aktywny plan ograniczonego recovery Wave R2;
- aktywuje `IA-HC-006` prospektywnie od kontrolowanego merge niniejszego rekordu i Repository Verification;
- nakazuje świeżą weryfikację treści obecnych na `main` po PR #74–#76;
- pozwala następnie zaktualizować, ponownie zweryfikować i przedłożyć do decyzji PR #77;
- nie nadaje authority retroaktywnie i nie usuwa historycznej informacji o luce.

## Stan zastany podlegający ponownej weryfikacji
- PR #74 merge `9330a129ec37ac3f9d09b03e424981b9f2089075` — HMI navigation i geometria 1024×600;
- PR #75 merge `0a7795c41ac2b2416906869180289cdab2f53464` — provenance obserwacji i allowlisted capabilities;
- PR #76 merge `61de55a84319a2ba29a21dda5387a603381873f8` — runtime/docs CI i semantic governance checker.

Zmiany te są istniejącym stanem repozytorium. Recovery nie twierdzi, że posiadały wcześniejsze authority.

## Świeża weryfikacja recovery
Na bazie `main` `61de55a84319a2ba29a21dda5387a603381873f8` wykonano:
- przegląd połączonego diffu PR #74–#76;
- 15/15 celowanych testów R2-A/R2-B/R2-C — PASS;
- 103/103 pełnej regresji — PASS;
- `compileall`, coverage runner, foundation governance i semantic governance — PASS.

Treść PR #74–#76 zostaje przyjęta jako ponownie zweryfikowany stan techniczny, z zachowaniem jawnego historycznego braku activation record. R2-C semantic governance wymaga korekty zawartej w tym recovery PR; closure pozostaje otwarte.

## Prospektywny zakres IA-HC-006
Po kontrolowanym merge i Repository Verification dozwolone są wyłącznie lokalne, synthetic/test-only działania określone w `IMP-HC-005` dla `AUD-HC-018`–`AUD-HC-025`, w tym korekta PR #77, testy, dokumentacja i reconciliation.

## Wyłączenia
Brak authority dla HW-A1/HW-A2/HW-A3 PASS, natywnego artefaktu Kinco DTools, wyboru lub wdrożenia fizycznego edge hosta, real-farm data, live RFID, realnego KVK I/O, machine CAN/RS485/Modbus/serial, commands/writes/configuration/actuation, hydrauliki, PLC/safety mutation, network/cloud, external report delivery, deployment/provisioning, signing, release ani public distribution.

## Warunek aktywacji
`IA-HC-006 = APPROVED / ACTIVE` dopiero po:
1. finalnym zatwierdzeniu dokładnego head SHA recovery PR przez Project Ownera;
2. kontrolowanym merge bez zmiany zatwierdzonego diffu;
3. Repository Verification na kanonicznym `main`.

Do tego momentu PR #77 pozostaje `OPEN / MERGE BLOCKED BY GOVERNANCE RECOVERY`.
