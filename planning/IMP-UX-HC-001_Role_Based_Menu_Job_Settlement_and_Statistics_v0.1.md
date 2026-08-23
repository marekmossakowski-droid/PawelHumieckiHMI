# IMP-UX-HC-001 — Menu ról, zlecenia, rozliczenia i statystyki v0.1

## Status

`APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-007-ACTIVATION-001`

## Cel

Zrealizować zatwierdzony projekt `UX-HC-001` jako lokalny, synthetic/test-only moduł zleceń, rozliczeń i statystyk, z obowiązkowym TDD i bez rozszerzenia granicy KVK.

## Źródła

- `docs/design/UX-HC-001_Role_Based_Menu_Job_Settlement_and_Statistics_v0.1.md`;
- `docs/architecture/ADR-HC-008_Job_Pricing_Snapshot_and_Derived_Statistics_v0.1.md`;
- `docs/requirements/REQ-HC-002_Role_Based_Jobs_Settlement_and_Statistics_v0.1.md`;
- `docs/superpowers/plans/2026-08-23-ux-hc-001-job-settlement.md`.

## Inkrementy

### UX-HC-001-A — Ceny i kalkulacja

- pieniądze w groszach;
- dziesiętne ilości materiałów;
- snapshot stawek;
- deterministyczne `ROUND_HALF_UP`;
- materiał lokalny bez mutacji katalogu.

### UX-HC-001-B — Cykl zlecenia i liczniki

- otwarcie, aktywna praca i niezmienne zamknięcie;
- powiązanie z trwałymi sesjami;
- unikalne liczenie ukończonych krów;
- idempotentne zużycie materiałów;
- fail-closed blokady zamknięcia.

### UX-HC-001-C — Trwałość i audyt

- osobny `LocalJobStore`;
- atomowy zapis i integralność;
- niezmienny snapshot zamknięcia; korekty poza zakresem v0.1;
- odtworzenie po restarcie;
- brak cichego przeliczenia historii.

### UX-HC-001-D — Menu ról i widoczność cen

- cztery główne powierzchnie operatora;
- cztery główne powierzchnie właściciela;
- role-aware view model;
- ceny widoczne tylko na zatwierdzonych ekranach;
- geometria 1024×600 i minimum 48 px;
- brak affordance sterowania maszyną.

### UX-HC-001-E — Statystyki i podsumowanie PDF

- statystyki operatora i właściciela z trwałych rekordów;
- końcowe pozycje i `RAZEM NETTO`;
- lokalny PDF oznaczony jako podsumowanie, nie faktura;
- pełny syntetyczny przebieg integracyjny.

## TDD i bramki

Każdy inkrement wykonuje kolejno:

1. zdalny commit RED zawierający wyłącznie test zachowania;
2. potwierdzenie oczekiwanej porażki asercji, bez setup/import/file errors;
3. minimalny commit GREEN;
4. testy celowane;
5. pełną regresję;
6. coverage, foundation governance i semantic governance;
7. dokumentację i traceability;
8. Draft PR albo jawny, reviewowalny checkpoint w zatwierdzonym PR;
9. exact-head approval przed merge.

## Granice

- tylko lokalne dane syntetyczne;
- bez realnych gospodarstw, zwierząt i cen;
- bez live RFID i realnego KVK I/O;
- bez machine bus, command/write/configuration/actuation;
- bez hydrauliki i PLC/safety mutation;
- bez network/cloud i zewnętrznej wysyłki;
- bez fakturowania, płatności i księgowania;
- bez deployment, signing, release i public distribution.

## Warunek rozpoczęcia

Warunek rozpoczęcia został spełniony przez zatwierdzenie exact headu PR #80, kontrolowany merge `3a32e3b5b7d1f5b2693836c044ef73caa63276d3`, Repository Verification oraz kanoniczny rekord `HC-IA-HC-007-ACTIVATION-001`. Runtime może być realizowany wyłącznie w ograniczonym zakresie `IA-HC-007`, inkrementami TDD i z osobnym exact-head approval każdego merge.

## Warunek zakończenia

Zakres może zostać uznany za wdrożony wyłącznie po merge wszystkich zatwierdzonych inkrementów, pełnej weryfikacji na `main`, rekonsyliacji wymagań i oddzielnej decyzji closure. Nie ustanawia to gotowości produkcyjnej ani zgody na realne dane.
