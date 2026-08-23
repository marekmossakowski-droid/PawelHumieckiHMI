# REQ-HC-003-G1 — Complete Generation 1 HMI GUI and DTools v0.1

## Status

`APPROVED / BASELINED — EFFECTIVE AFTER MERGE AND REPOSITORY VERIFICATION OF HC-IA-HC-008-ACTIVATION-001`

## Cel i zakres

Wymagania definiują kompletną lokalną powierzchnię GUI Generacji 1 dla Pawła
działającego jako zootechnik oraz oddzielną strefę właściciela. Zachowują
`ADR-HC-009`, zamknięte ograniczone workstreamy `REQ-HC-002-A1` i
`REQ-HC-002-S1` oraz istniejące reguły kliniczne. Wszystkie dane, demonstracje
i bindingi pozostają synthetic/test-only.

„Kompletny GUI” oznacza kompletność semantycznych ekranów i przejść w
zatwierdzonym lokalnym zakresie. Nie oznacza fizycznej akceptacji GL100E,
działającego połączenia z edge hostem, realnych urządzeń ani gotowości produktu
do wdrożenia.

## Wymagania nawigacji i powłoki

### REQ-HC-G1-NAV-001 — Kanoniczny graf ekranów

GUI SHALL posiadać wersjonowany graf obejmujący: start i recovery, pulpit,
otwieranie zlecenia, ceny, aktywne zlecenie, pełny kreator zabiegu, materiały,
podsumowanie sesji, statystyki, historię, zamknięcie zlecenia, raporty, strefę
właściciela, diagnostykę oraz kontrolowane ekrany błędów.

### REQ-HC-G1-NAV-002 — Deterministyczne przejścia

Każda akcja SHALL mieć jawny ekran źródłowy, docelowy, warunek dostępności i
zachowanie odmowy. `WSTECZ` nie może usuwać trwałego rekordu ani omijać bramki
zapisu. Restart SHALL odtworzyć ekran z bezpiecznego stanu domenowego, a nie z
niezweryfikowanej historii widoku.

### REQ-HC-G1-NAV-003 — Obsługa w rękawicach

Na GL100E każdy podstawowy cel dotykowy SHALL mieć co najmniej `64×64 px`, nie
nakładać się i mieścić w `1024×600`. Ekran SHALL prezentować najwyżej cztery
podstawowe akcje w stałym obszarze nawigacyjnym.

## Zlecenie i ceny

### REQ-HC-G1-JOB-001 — Otwarcie zlecenia

Paweł SHALL móc lokalnie wybrać syntetyczne gospodarstwo i operatora, podać
planowaną liczbę krów, ustalić stawkę netto za krowę oraz ceny dodatkowych
materiałów i zatwierdzić snapshot przed rozpoczęciem pracy.

### REQ-HC-G1-JOB-002 — Widoczność i korekta cen

Ceny SHALL być widoczne przy otwieraniu, dozwolonej korekcie i podsumowaniu,
lecz ukryte podczas rutynowej pracy przy zwierzęciu. Paweł nie potrzebuje PIN-u
właściciela do operacji cenowych dozwolonych przez `REQ-HC-002-A1`.

### REQ-HC-G1-JOB-003 — Stan aktywnego zlecenia

Pulpit SHALL pokazywać gospodarstwo, identyfikator zlecenia, liczbę wykonanych
krów, plan, niedokończone sesje i ilości dodatkowych materiałów bez cen.

## Pełny zabieg zootechnika

### REQ-HC-G1-TREAT-001 — Kreator zabiegu

Paweł SHALL wykonać na HMI przepływ: identyfikacja zwierzęcia → kończyna i
racica → strefa i zmiana → zabieg → dodatkowe materiały → termin kontroli →
podsumowanie → trwały zapis. Niedostępna kamera nie może blokować zabiegu ani
tworzyć fałszywego dowodu zdjęcia.

### REQ-HC-G1-TREAT-002 — Zapis i licznik

Akcja ukończenia SHALL korzystać z kanonicznej operacji aplikacyjnej. Licznik
zwiększa się dopiero po trwałym przypisaniu unikalnej sesji `COMPLETED`; błąd,
anulowanie, szkic i identyczne ponowienie nie zwiększają go.

### REQ-HC-G1-TREAT-003 — Materiały

GUI SHALL umożliwić wybór i zmianę ilości dodatkowych materiałów przypisanych
do sesji. Rutynowy ekran pokazuje kod/nazwę, jednostkę i ilość bez ceny.

### REQ-HC-G1-TREAT-004 — Recovery fail-closed

Brak identyfikacji, konflikt sesji, niepotwierdzony zapis lub niespójny snapshot
SHALL blokować ukończenie i kierować do jawnego widoku uzgodnienia. GUI nie
może samodzielnie naprawiać ani cicho pomijać konfliktu.

## Statystyki, rozliczenie i raporty

### REQ-HC-G1-STAT-001 — Widok pracy

Paweł SHALL widzieć dzienną i zleceniową liczbę ukończonych krów, dodatkowe
materiały oraz otwarte i zamknięte zlecenia. Widok pracy nie pokazuje kwot.

### REQ-HC-G1-STAT-002 — Zamknięcie i RAZEM NETTO

Ekran zamknięcia SHALL prezentować kanoniczne linie settlementu i dominujące
`RAZEM NETTO: X XXX,XX zł`. GUI nie wykonuje własnych obliczeń finansowych.

### REQ-HC-G1-STAT-003 — Historia i raporty

GUI SHALL umożliwić lokalne filtrowanie syntetycznych zleceń według operatora,
gospodarstwa, daty i statusu oraz wygenerowanie istniejącego deterministycznego
PDF oznaczonego `DOKUMENT ROZLICZENIOWY — NIE JEST FAKTURĄ`.

## Strefa właściciela

### REQ-HC-G1-ADMIN-001 — Oddzielona strefa

Strefa właściciela SHALL być oddzielona sześciocyfrowym lokalnym PIN-em,
automatycznie blokowana po bezczynności i odrzucać niepełne, błędne lub
nadmiarowe wejście. Pięć kolejnych błędnych prób SHALL blokować nowe próby na
pięć minut, a poprawnie otwarta sesja SHALL wygasać po dziesięciu minutach
bezczynności. Czas jest wstrzykiwany i testowany deterministycznie. Zakres
obejmuje wyłącznie syntetyczną bramkę, bez produkcyjnego authentication i
credentials.

### REQ-HC-G1-ADMIN-002 — Powierzchnie administracyjne

Po odblokowaniu właściciel SHALL mieć semantyczne powierzchnie gospodarstw,
katalogu materiałów, operatorów, historii, raportów, audytu i diagnostyki.
Każda mutacja musi wywoływać osobny kanoniczny przypadek użycia; brak takiego
przypadku użycia oznacza akcję niewidoczną lub zablokowaną.

### REQ-HC-G1-ADMIN-003 — Brak blokady Pawła

PIN właściciela SHALL NOT blokować Pawłowi pełnego zabiegu, otwierania i
zamykania zlecenia, dozwolonego ustalania/korekty cen ani jego statystyk.

## Adaptacyjna prezentacja i DTools

### REQ-HC-G1-ADAPT-001 — Semantyka niezależna od profilu

Modele ekranów, akcji, widoczności i błędów SHALL być niezależne od pikseli,
orientacji i DTools. Profil urządzenia mapuje semantykę na geometrię.

### REQ-HC-G1-ADAPT-002 — Profil GL100E

Pierwszy profil SHALL realizować Kinco GL100E `1024×600`, stały nagłówek,
obszar treści, dolny pasek akcji, czytelność z odległości roboczej oraz cele
dotykowe co najmniej `64×64 px`. Rozdzielczość nie może przenikać do domeny.

### REQ-HC-G1-ADAPT-003 — Brak przedwczesnej Generacji 2

Kontrakty MAY pozostać wieloprofilowe, lecz pakiet SHALL NOT implementować
komputera, telefonu, tabletu, sieci, synchronizacji ani zdalnej administracji.

### REQ-HC-G1-DTOOLS-001 — Natywny artefakt

Po aktywacji właściwego authority realizacja SHALL utworzyć natywny projekt
Kinco DTools dla dokładnego modelu GL100E, zapisując wersję DTools, hash źródła,
manifest ekranów i timestamp. Specyfikacja tekstowa nie może być przedstawiana
jako natywny artefakt.

### REQ-HC-G1-DTOOLS-002 — Binding manifest

Każdy widget SHALL wskazywać semantyczny binding, typ, kierunek, dozwolony stan
i zachowanie przy braku danych. DTools SHALL NOT obliczać cen, liczników,
diagnoz ani settlementu.

### REQ-HC-G1-DTOOLS-003 — Kompilacja offline

Projekt SHALL przejść build/compile w jawnie zapisanej wersji DTools bez
błędów. Dowód obejmuje log, hash projektu i zgodność liczby ekranów/bindingów z
manifestem repozytorium.

### REQ-HC-G1-DTOOLS-004 — Granica fizyczna

Offline build i symulator nie ustanawiają `HW-A1`, `HW-A2` ani `HW-A3 = PASS`.
Upload, test dotyku na panelu i fizyczne bindingi wymagają dostarczonego sprzętu,
wybranego edge hosta, osobnego authority i Repository Verification.

## Globalne wymagania bezpieczeństwa

- GUI SHALL NOT udostępniać sterowania KVK, hydrauliką, PLC ani safety.
- Brak kanonicznego use case SHALL skutkować brakiem aktywnej akcji.
- Wszystkie dane i fixture'y pozostają lokalne i syntetyczne.
- Kamera, live RFID i device access pozostają niedostępne i uczciwie oznaczone.
- Raport jest dokumentem rozliczeniowym, nie fakturą ani dokumentem fiskalnym.

## Weryfikacja

Każdy inkrement runtime wymaga clean assertion RED, zdalnego test-only
checkpointu, minimalnego GREEN, testów celowanych, pełnej regresji, osobnego
Draft PR i zgody Project Ownera na exact final head. Implementacja pozostaje
zabroniona do kontrolowanego merge i Repository Verification rekordu
`HC-IA-HC-008-ACTIVATION-001`.

## Wyłączenia

Brak Generacji 2, rzeczywistych danych, network/cloud, synchronizacji, live
RFID, kamery, device access, KVK I/O, machine bus, sterowania, hydrauliki,
PLC/safety mutation, korekt zamkniętego rozliczenia, invoicing, VAT,
księgowości, płatności, produkcyjnego authentication, deploymentu, signing,
release i public distribution. PR #77 i R2 pozostają bez zmian.
