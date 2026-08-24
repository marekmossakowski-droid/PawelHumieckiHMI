# HC-UX-HC-002-VISUAL-DIRECTION-DECISION-001 — iOS-inspired HMI with subtle AI cues

## Status

`PROJECT OWNER DIRECTIVE — APPROVED CONTENT ONLY / NOT BASELINED / NO NEW IMPLEMENTATION AUTHORITY`

## Decyzja Project Ownera

Project Owner zatwierdził dla projektowania kolejnych ekranów HoofCare HMI
kierunek:

> wzorować się na grafice iOS z lekką nutą AI.

Decyzja stanowi wejście projektowe do dalszego rozwinięcia
`UX-HC-002 — Generation 1 Complete HMI GUI and DTools Design v0.1`.
Nie zmienia samodzielnie jego baseline'u i nie autoryzuje implementacji poza
istniejącym `IA-HC-008`.

## Interpretacja projektowa

### 1. Inspiracja iOS

Ekrany SHALL wykorzystywać:

- spokojną i jednoznaczną hierarchię informacji;
- czytelną typografię oraz wyraźne rozróżnienie nagłówków, wartości i opisów;
- miękkie karty, kontrolowane zaokrąglenia i oszczędne separatory;
- spójne marginesy, rytm i grupowanie funkcji;
- prosty język wizualny bez technicznego przeładowania;
- subtelne, krótkie mikrointerakcje wyłącznie tam, gdzie wspierają potwierdzenie
  stanu lub działania.

Inspiracja nie oznacza kopiowania znaków towarowych, ikon, fontów, zasobów ani
układu konkretnej aplikacji Apple. HoofCare zachowuje własną tożsamość i
przemysłowy charakter.

### 2. Lekka nuta AI

Motyw AI SHALL pozostać subtelny i funkcjonalny. Może być widoczny poprzez:

- delikatny akcent kolorystyczny przy podpowiedzi lub stanie wymagającym uwagi;
- krótkie, wyjaśnialne komunikaty pomocnicze;
- rozróżnienie statusów: informacja, sugestia, ostrzeżenie i blokada;
- niewielki symbol asysty przy funkcji, która korzysta z przyszłej,
  jawnie autoryzowanej logiki wspomagającej;
- spokojne animowane potwierdzenie analizy lub walidacji, jeżeli profil
  urządzenia i narzędzie DTools pozwalają to zrealizować bez pogorszenia
  czytelności.

Interfejs SHALL NOT sugerować, że AI samodzielnie diagnozuje, zatwierdza zabieg,
podejmuje decyzję kliniczną, omija operatora albo posiada authority.

### 3. Priorytet pracy Pawła

Kierunek wizualny nie może osłabić ergonomii przemysłowego HMI. Dla profilu
Kinco GL100E `1024×600` nadal obowiązują:

- obsługa w rękawicach;
- podstawowe cele dotykowe co najmniej `64×64 px`;
- najwyżej cztery podstawowe akcje w stałym obszarze nawigacyjnym;
- wysoki kontrast i czytelność z odległości roboczej;
- język polski;
- ceny niewidoczne podczas rutynowej pracy przy zwierzęciu;
- wyraźne, fail-closed komunikaty błędów i recovery;
- brak dekoracji konkurującej z identyfikacją zwierzęcia, etapem zabiegu,
  licznikami lub ostrzeżeniami.

## Zastosowanie

Kierunek SHALL zostać rozwinięty w osobnym, kontrolowanym przyroście projektowym
przed implementacją wizualnych ekranów i profilu GL100E. Przyrost powinien
zdefiniować co najmniej paletę, typografię, komponenty kart, przyciski, stany
systemowe, komunikaty asysty, zasady animacji oraz przykładowe ekrany referencyjne.

Nie należy mieszać tego dokumentu z bounded runtime incrementem G1-2.

## Granice

Decyzja nie:

- implementuje GUI, modeli AI ani autonomicznych rekomendacji;
- nie rozszerza `REQ-HC-003-G1`, `UX-HC-002` ani `IA-HC-008`;
- nie aktywuje Generation 2, sieci, chmury, synchronizacji ani zdalnej administracji;
- nie nadaje dostępu do kamery, live RFID, urządzeń, KVK I/O ani machine bus;
- nie zezwala na sterowanie, hydraulikę ani PLC/safety mutation;
- nie ustanawia production authentication, uploadu na fizyczny panel,
  deploymentu, signing, release ani public distribution;
- nie zmienia `EDGE_HOST_REQUIRED`, HW-A1/HW-A2/HW-A3, PR #77 ani R2.
