# HC-REQ-HC-003-G1-BASELINE-DECISION-001

## Status

`BASELINE READY — PROJECT OWNER EXACT-HEAD MERGE REQUIRED`

## Decyzja

Po kontrolowanym merge i pozytywnej Repository Verification tego rekordu:

- `REQ-HC-003-G1 v0.1` staje się `APPROVED / BASELINED`;
- `UX-HC-002 v0.1` staje się zatwierdzonym written design;
- plan TDD G1-1..G1-6 staje się zatwierdzonym planem realizacji;
- `IA-HC-008` staje się prospektywnie `APPROVED / ACTIVE` wyłącznie w
  granicach zapisanych w authority.

## Podstawa

- source package: PR #101;
- Project Owner-approved exact head: `f18df0d37df6ff241696822758e14f795107eddd`;
- source tree: `b25b5ff8a12f2aca37d109a72beaded3130e20ba`;
- controlled merge: `eb41f067d2c0c2c4eeba98c9d8ab4cdae598c361`;
- merge parents: `d2af53d739403ff6f4199fabe43159cb3de10317` and
  `f18df0d37df6ff241696822758e14f795107eddd`;
- verified merge tree: `b25b5ff8a12f2aca37d109a72beaded3130e20ba`;
- Repository Verification: 156/156 tests, coverage, compileall, foundation
  governance, semantic governance and diff check — PASS.

## Granice

Decyzja nie uruchamia implementacji przed merge i Repository Verification
rekordu aktywacji. Nie rozszerza zakresu na Generation 2, real data,
network/cloud, synchronizację, live RFID, kamerę, device access, KVK I/O,
machine bus, sterowanie, hydraulikę, PLC/safety mutation, fakturowanie, VAT,
księgowość, płatności, produkcyjne authentication, upload na panel,
deployment, signing, release ani public distribution. `EDGE_HOST_REQUIRED`,
HW-A1, HW-A2 i HW-A3 pozostają otwarte. PR #77 i R2 pozostają bez zmian.
