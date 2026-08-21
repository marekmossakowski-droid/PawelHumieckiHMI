# FND-HC-001 — Project Foundation v0.1

## Status

`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## 1. Tożsamość projektu

- Nazwa robocza: `HoofCare`.
- Repozytorium SSOT: `marekmossakowski-droid/PawelHumieckiHMI`.
- Pierwsza platforma docelowa: poskrom `KVK 801-1`, generacja około 2013 r., starsza zielona konstrukcja.
- Project Owner: właściciel repozytorium.

## 2. Problem

Proces korekcji i diagnostyki racic jest wykonywany fizycznie przy poskromie, natomiast identyfikacja zwierzęcia, lokalizacja zmiany, klasyfikacja schorzenia, materiały, dokumentacja zdjęciowa i follow-up są zwykle rejestrowane w rozproszony sposób albo nie są rejestrowane w sposób pozwalający na analizę stada.

## 3. Cel produktu

HoofCare ma zapewnić operatorowi jednoznaczny, szybki i audytowalny workflow HMI dla pojedynczego zabiegu oraz tworzyć struktury danych i raporty użyteczne dla:

- rolnika;
- zootechnika;
- lekarza weterynarii;
- żywieniowca;
- służb technicznych utrzymujących stanowisko.

## 4. Zakres produktu v1

1. Identyfikacja krowy.
2. Wybór kończyny i palca.
3. Graficzna mapa stref racicy.
4. Rejestracja zmiany i jej ciężkości.
5. Rejestracja wykonanego zabiegu.
6. Rejestracja zużytych materiałów.
7. Dokumentacja zdjęciowa PRZED/PO.
8. Historia zwierzęcia.
9. Follow-up i przypomnienie kontroli.
10. Raport indywidualny i statystyki stada.
11. Odczyt wybranych stanów KVK w trybie `READ_ONLY`, jeśli audyt konkretnego egzemplarza potwierdzi bezpieczny interfejs.

## 5. Poza zakresem bazowym

Bez osobnej decyzji i Implementation Authority poza zakresem pozostają:

- sterowanie hydrauliką KVK;
- sterowanie bramami, pasami, wciągarkami lub podnoszeniem;
- obejście lub zastąpienie PLC KVK;
- modyfikacja E-STOP, safety PLC, interlocków lub innych funkcji bezpieczeństwa;
- automatyczne wykonywanie zabiegów;
- autonomiczna diagnoza weterynaryjna;
- automatyczne dawkowanie leków;
- systemy wymagające certyfikacji medycznej/weterynaryjnej bez osobnego workstreamu zgodności.

## 6. Invariants

### FND-HC-I01 — Safety independence

HoofCare SHALL NOT być wymagany do działania podstawowych funkcji bezpieczeństwa poskromu.

### FND-HC-I02 — Read-only first

Pierwsza integracja z KVK SHALL być ograniczona do bezpiecznego odczytu i rejestracji stanów.

### FND-HC-I03 — Human clinical authority

Klasyfikacja kliniczna wymagająca wiedzy weterynaryjnej SHALL pozostawać decyzją człowieka; system może wspierać wybór, dokumentację i spójność nomenklatury.

### FND-HC-I04 — Provenance

Każdy rekord zabiegu i zdjęcie SHALL mieć możliwe do audytu pochodzenie, identyfikację zwierzęcia, operatora i timestamp.

### FND-HC-I05 — Fail closed

Brak wiarygodnej identyfikacji zwierzęcia, konflikt danych lub utrata integralności sesji SHALL blokować automatyczne przypisanie danych do historii zwierzęcia.

## 7. Pierwszy sprzęt prototypowy

Aktualny kandydat HMI MVP: `Kinco GL100E 10.1"`.

Decyzja nie jest jeszcze architektonicznym baseline'em. Ostateczny dobór zależy od audytu KVK 801-1 i wyników prototypu stołowego.

## 8. Metodyka rozwoju

Projekt stosuje sekwencję:

`Foundation → ARS → ARB → ADR → System Architecture → LEL → Requirements → Implementation → Testing → Integration → Release`

Każda implementacja wymaga wcześniejszego, jawnego authority odpowiadającego jej zakresowi.

## 9. Kryterium zamknięcia Foundation

Foundation może zostać oznaczony `BASELINED`, gdy Project Owner zatwierdzi końcowy diff dokumentu oraz zostaną ustanowione co najmniej:

- kanoniczny current state;
- roadmapa;
- traceability;
- pierwsza granica Implementation Authority.
