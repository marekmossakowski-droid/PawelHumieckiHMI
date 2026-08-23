# HC-IA-HC-008-ACTIVATION-001 — Generation 1 HMI GUI Authority Activation

## Status

`ACTIVATION READY — PROJECT OWNER EXACT-HEAD MERGE REQUIRED`

## Zatwierdzona treść i dowody merge

- source package: PR #101;
- Project Owner-approved exact head: `f18df0d37df6ff241696822758e14f795107eddd`;
- source tree: `b25b5ff8a12f2aca37d109a72beaded3130e20ba`;
- controlled merge: `eb41f067d2c0c2c4eeba98c9d8ab4cdae598c361`;
- merge parents: `d2af53d739403ff6f4199fabe43159cb3de10317` and
  `f18df0d37df6ff241696822758e14f795107eddd`;
- verified merge tree: `b25b5ff8a12f2aca37d109a72beaded3130e20ba`.

Repository Verification exact merge commitu zakończyła się PASS: 156/156
testów, coverage, compileall, foundation governance, semantic governance i
diff check.

## Skutek prospektywny po merge i weryfikacji tego rekordu

- `REQ-HC-003-G1 = APPROVED / BASELINED`;
- `UX-HC-002 = APPROVED / BASELINED`;
- plan TDD G1-1..G1-6 = `APPROVED / ACTIVE`;
- `IA-HC-008 = APPROVED / ACTIVE` prospektywnie;
- implementacja może rozpocząć się wyłącznie od osobnego clean assertion RED
  dla G1-1 i dalej podlegać pełnemu rygorowi planu.

`RUNTIME NOT STARTED` w chwili utworzenia tego rekordu.

## Brak retroaktywności

Rekord nie ustanawia authority przed własnym kontrolowanym merge i pozytywną
Repository Verification. Nie zatwierdza wcześniejszego kodu ani danych.

## Granice

Authority nie obejmuje Generation 2, real data, network/cloud, synchronizacji,
live RFID, kamery, device access, KVK I/O, machine bus, sterowania, hydrauliki,
PLC/safety mutation, fakturowania, VAT, księgowości, płatności, produkcyjnego
authentication, uploadu na fizyczny panel, deploymentu, signing, release ani
public distribution. `EDGE_HOST_REQUIRED`, HW-A1, HW-A2 i HW-A3 pozostają
otwarte. PR #77 i R2 pozostają bez zmian.
