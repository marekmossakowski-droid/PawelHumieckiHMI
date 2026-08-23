# HC-IA-HC-007-ACTIVATION-001 — Role-Based Jobs Authority Activation

## Status

`MERGED / REPOSITORY VERIFIED — IA-HC-007 PROSPECTIVELY ACTIVE`

## Project Owner decision

23 sierpnia 2026 Project Owner udzielił zgody exact-head na merge PR #80 i prospektywną aktywację `IA-HC-007` po Repository Verification.

Decyzja dotyczyła dokładnie:

- PR #80 head `8901922380a3ec342747088e5acccdcd4ca5b44d`;
- tree `fa8d5e3bdf1d71087b12472d8a649f6685ac6632`;
- `UX-HC-001`, `ADR-HC-008`, `REQ-HC-002`, `IMP-UX-HC-001` i `IA-HC-007` w wersjach zawartych w tym drzewie.

## Controlled merge evidence

- base `main`: `046d033cde8108090ebfd94886958837ae5bc58d`;
- approved head: `8901922380a3ec342747088e5acccdcd4ca5b44d`;
- merge commit: `3a32e3b5b7d1f5b2693836c044ef73caa63276d3`;
- merge parents: base i approved head powyżej;
- merge tree: `fa8d5e3bdf1d71087b12472d8a649f6685ac6632`.

Merge wykonano z ochroną `expected_head_sha` po ponownym potwierdzeniu zielonych `runtime-ci` i `docs-ci`, braku review oraz braku review threads.

## Repository Verification

Na kanonicznym `main` potwierdzono:

- equality `main == 3a32e3b5b7d1f5b2693836c044ef73caa63276d3` — PASS;
- exact merge parents — PASS;
- equality remote merge tree i niezależnie testowanego local tree — PASS;
- 104/104 pełnej regresji — PASS;
- `compileall` — PASS;
- coverage runner — PASS;
- foundation governance — PASS;
- semantic governance — PASS;
- `git diff --check` — PASS.

## Prospective effect

Od pozytywnego Repository Verification:

- `UX-HC-001 / ADR-HC-008 / REQ-HC-002 = APPROVED / BASELINED` dla ograniczonego v0.1 slice;
- `IMP-UX-HC-001 = APPROVED / ACTIVE`;
- `IA-HC-007 = APPROVED / ACTIVE` prospektywnie;
- każdy runtime increment nadal wymaga zdalnego clean assertion RED, minimalnego GREEN, pełnej regresji, Draft PR i osobnego exact-head approval przed merge;
- aktywacja nie oznacza, że runtime został już zaimplementowany lub zweryfikowany.

## Boundary

Authority pozostaje wyłącznie lokalne i synthetic/test-only. Nie zezwala na realne gospodarstwa, klientów, zwierzęta, operatorów lub ceny; live RFID; kamerę lub device access; realny KVK I/O; machine CAN/RS485/Modbus/serial; commands/writes/configuration/actuation; hydraulikę; PLC/safety mutation; network/cloud; wysyłkę raportów; fakturowanie, VAT, księgowanie lub płatności; produkcyjne credentials; korekty rozliczeń; deployment, provisioning, signing, release ani public distribution.

PR #77, R2 closure, HW-A1/HW-A2/HW-A3 oraz fizyczna integracja pozostają odrębne i nie są objęte tą decyzją.
