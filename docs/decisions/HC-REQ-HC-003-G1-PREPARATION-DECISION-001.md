# HC-REQ-HC-003-G1-PREPARATION-DECISION-001

## Status

`PACKAGE PREPARATION AUTHORIZED / CONTENT APPROVAL PENDING / RUNTIME NOT AUTHORIZED`

## Instrukcja Project Ownera

24 sierpnia 2026 Project Owner zezwolił na autonomiczne przygotowanie
ograniczonego pakietu projektowego dla kompletnego GUI HMI Generacji 1 i
realizacji Kinco DTools. Podstawą jest kanoniczny `main` po kontrolowanym merge
PR #100 `d2af53d739403ff6f4199fabe43159cb3de10317` i Repository Verification
exact tree `d28f73b0731917bd3777d198c5210071c9a613d8`.

## Dozwolona zawartość pakietu

- wymagania dla pełnej lokalnej nawigacji i workflow zootechnika;
- written design semantycznej warstwy prezentacji i profilu GL100E;
- szczegółowy plan implementacji TDD;
- requirement-level traceability;
- proponowane, nieaktywne `IA-HC-008`;
- fail-closed kontrole spójności governance.

Pakiet może opisywać przygotowanie zlecenia, ceny, cały zabieg, materiały,
liczniki, statystyki, zamknięcie i `RAZEM NETTO`, raporty oraz lokalną strefę
właściciela. Kinco GL100E `1024×600` jest pierwszym profilem realizacyjnym, a
nie właściwością domeny.

## Wybrany kierunek

Warstwa domenowa i aplikacyjna pozostają kanonicznym źródłem reguł. GUI
konsumuje semantyczne view modele. Profil GL100E mapuje je na geometrię
`1024×600`, a projekt DTools realizuje wyłącznie zatwierdzony manifest ekranów
i bindingów. DTools nie oblicza cen, liczników ani rozliczenia.

## Brak skutku wykonawczego

Ta decyzja nie zatwierdza treści pakietu, nie baselinuje `REQ-HC-003-G1`, nie
aktywuje `IA-HC-008` i nie zezwala na implementację GUI, utworzenie projektu
DTools, upload do panelu ani zmianę runtime. Nie obejmuje Generacji 2,
rzeczywistych danych, urządzeń, synchronizacji, network/cloud, sterowania,
fakturowania, VAT, księgowości, płatności, deploymentu ani public distribution.
PR #77 i R2 pozostają bez zmian.
