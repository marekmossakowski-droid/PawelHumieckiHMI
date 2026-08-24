# UX-HC-002-A1 — Jasny iOS-industrial Visual System v0.1

## Status

`PROPOSED FOR OWNER APPROVAL / BASELINE EFFECTIVE ONLY AFTER EXACT-HEAD
APPROVAL, CONTROLLED MERGE AND REPOSITORY VERIFICATION / NO NEW IMPLEMENTATION
AUTHORITY`

## 1. Cel i źródło decyzji

Dokument rozwija zatwierdzony przez Project Ownera kierunek
`HC-UX-HC-002-VISUAL-DIRECTION-DECISION-001`: grafika inspirowana iOS z lekką,
funkcjonalną nutą AI. Ustanawia deterministyczny język wizualny dla profilu
Kinco GL100E `1024×600`, który może następnie zostać odwzorowany w DTools w
ramach istniejącego `IA-HC-008`.

Inspiracja iOS oznacza spokojną hierarchię, czytelne karty, rytm, oszczędne
separatory i jednoznaczne stany. Nie oznacza kopiowania fontów, ikon, znaków
towarowych, zasobów ani układu konkretnej aplikacji Apple.

## 2. Niezmienne priorytety

1. Czytelność i obsługa w rękawicach są ważniejsze niż dekoracja.
2. Każda podstawowa akcja ma cel co najmniej `64×64 px`; ekran ma najwyżej
   cztery akcje podstawowe w stałym dolnym pasku.
3. Stan krytyczny jest opisany tekstem i symbolem; kolor nigdy nie jest jedynym
   nośnikiem informacji.
4. Rutynowe ekrany zabiegu nie pokazują cen ani kwot.
5. Asysta AI nie diagnozuje, nie zatwierdza zabiegu i nie wykonuje akcji.
6. Brak danych lub nieobsługiwana funkcja daje jawny stan fail-closed.

## 3. Paleta `G1-LIGHT-A`

| Token | Wartość | Zastosowanie |
|---|---|---|
| `surface.canvas` | `#F2F4F7` | główne jasnoszare tło |
| `surface.card` | `#FFFFFF` | karty i panele treści |
| `surface.selected` | `#E8F1FF` | wybrana pozycja bez utraty kontrastu |
| `text.primary` | `#17212B` | nagłówki, wartości i tekst główny |
| `text.secondary` | `#5F6B7A` | opisy i metadane |
| `action.primary` | `#1477FF` | zatwierdzone akcje główne |
| `action.disabled` | `#C7CDD5` | akcja niedostępna wraz z opisem przyczyny |
| `status.success` | `#168A5B` | sukces potwierdzony tekstem i symbolem |
| `status.warning` | `#A85F00` | ostrzeżenie wymagające uwagi |
| `status.blocked` | `#C9363E` | blokada lub odmowa fail-closed |
| `assist.teal` | `#168F84` | podpisana informacja asysty |
| `assist.violet` | `#665CF6` | mały symbol asysty, nie akcja autonomiczna |
| `border.subtle` | `#D8DEE6` | obrys kart i separatory |

Gradient, przezroczystość i cień nie mogą przenosić znaczenia. Jeżeli DTools
nie odwzoruje efektu dekoracyjnego deterministycznie, stosuje się kolor pełny
i obrys `border.subtle` bez zmiany semantyki.

## 4. Typografia

Podstawowym fontem realizacyjnym jest `Arial`, ponieważ nie kopiuje fontów
Apple, obsługuje polskie znaki i jest typowo dostępny w środowisku Windows.
Przed offline compile należy potwierdzić jego dostępność w użytej wersji
DTools. Brak pełnego zestawu polskich znaków blokuje build evidence.

| Styl | Rozmiar minimalny | Waga | Zastosowanie |
|---|---:|---|---|
| `display` | 32 px | Bold | dominująca wartość lub `RAZEM NETTO` |
| `heading` | 26 px | Bold | tytuł ekranu |
| `section` | 22 px | Bold | nazwa karty lub etapu |
| `body` | 20 px | Regular | dane i komunikaty robocze |
| `label` | 18 px | Bold | etykiety i przyciski |
| `meta` | 18 px | Regular | czas, identyfikator i opis pomocniczy |

Nie stosuje się tekstu poniżej 18 px ani kapitalików w długich komunikatach.
Wartość ważniejsza wizualnie zawsze poprzedza opis techniczny.

## 5. Siatka i kształt

- płótno: `1024×600`;
- nagłówek: `x=0, y=0, w=1024, h=64`;
- treść: `x=0, y=64, w=1024, h=472`;
- pasek akcji: `x=0, y=536, w=1024, h=64`;
- podstawowy margines treści: `24 px`;
- odstęp między kartami: `16 px`;
- promień kart: `16 px`, jeżeli DTools obsługuje go bez rasteryzacji tekstu;
- fallback kart: prostokąt z obrysem `1 px border.subtle`, bez fałszywego cienia;
- maksymalnie dwa poziomy kart zagnieżdżonych.

## 6. Komponenty

### `G1TopBar`

Pokazuje tytuł, rolę `Paweł` lub `Właściciel`, stan syntetyczny/offline i
opcjonalny licznik etapu. Nie zawiera ukrytych gestów ani nawigacji wymagającej
precyzyjnego trafienia.

### `G1Card`

Biała karta na tle `surface.canvas`, z marginesem 24 px, obrysem
`border.subtle` i opcjonalnym zaokrągleniem 16 px. Jedna karta odpowiada jednej
grupie znaczeniowej.

### `G1PrimaryButton`

Wypełnienie `action.primary`, biały tekst, minimum `64 px` wysokości. Akcja
jest widoczna tylko wtedy, gdy istnieje kanoniczny przypadek użycia i spełniono
jego guard.

### `G1SecondaryButton`

Białe wypełnienie, obrys `action.primary`, tekst `text.primary`. Służy do
`WSTECZ`, anulowania lub przejścia pomocniczego; nie konkuruje z akcją główną.

### `G1BlockedButton`

Wypełnienie `action.disabled`, tekst i symbol blokady oraz widoczna przyczyna.
Nie wysyła requestu i nie udaje działania.

### `G1StatusCard`

Łączy symbol, nagłówek i krótki opis. Obsługiwane statusy to `Informacja`,
`Sukces`, `Ostrzeżenie` i `Blokada`. Każdy status ma tekst niezależny od koloru.

### `G1AssistCard`

Opcjonalna karta z lewym paskiem `assist.teal`, niewielkim własnym symbolem
asysty w `assist.violet` i obowiązkową etykietą `Sugestia`. Karta zawiera
wyłącznie krótką, wyjaśnialną informację. Nie może zawierać przycisku
`Zastosuj automatycznie`, diagnozy ani wyniku sugerującego authority AI.

## 7. Mikrointerakcje

Jeżeli DTools obsługuje je bez obciążenia czytelności:

- potwierdzenie dotknięcia: zmiana wypełnienia przez `120 ms`;
- pojawienie się komunikatu: przejście bez przesunięcia do `180 ms`;
- zapis zakończony: pojedyncze, spokojne potwierdzenie do `180 ms`.

Animacja nie może być jedynym dowodem zapisu, błędu lub blokady. Brak wsparcia
animacji nie obniża zgodności, jeśli tekst i stan pozostają jednoznaczne.

## 8. Ekrany referencyjne

### G1-10 — Pulpit Pawła

- nagłówek: `Pulpit Pawła`, stan `Lokalnie • dane testowe`;
- górna karta: gospodarstwo, aktywne zlecenie i postęp krów;
- dwie karty licznikowe: wykonane krowy i zużyte materiały, bez cen;
- spokojny banner `Paweł Humięcki the best zootechnik` jako treść drugorzędna;
- dolne akcje: `Nowe zlecenie`, `Wznów pracę`, `Statystyki`, `Właściciel`.

### G1-33 — Zabieg

- nagłówek z identyfikatorem syntetycznego zwierzęcia i etapem;
- lewa karta: wybrana kończyna, racica, strefa i zmiana;
- prawa karta: dozwolone zabiegi z jednoznacznym stanem wyboru;
- brak cen, kwot, live RFID i kamery;
- dolne akcje: `Dalej`, `Wstecz` oraz wyłącznie akcje wynikające z view modelu.

### G1-43 — Zamknięte rozliczenie

- karta linii settlementu odczytanych z kanonicznego dokumentu;
- `RAZEM NETTO` jako dominujący styl `display`;
- stała etykieta `DOKUMENT ROZLICZENIOWY — NIE JEST FAKTURĄ`;
- brak ponownego obliczania kwot w DTools;
- akcje: istniejący PDF, historia i pulpit, jeśli udostępnia je view model.

### G1-60 — Uzgodnienie i błąd

- `G1StatusCard` typu `Blokada` z kodem i prostym opisem;
- następny bezpieczny krok jest wypisany jawnie;
- opcjonalna `G1AssistCard` może wyjaśnić przyczynę, ale nie rozwiązuje
  konfliktu automatycznie;
- akcje: bezpieczne ponowienie, diagnostyka i powrót bez zapisu.

### G1-51 — Pulpit właściciela

- odmienna etykieta roli, ale ten sam język wizualny;
- karty gospodarstw, materiałów, operatorów, historii, raportów, audytu i
  diagnostyki pojawiają się wyłącznie dla jawnych capability;
- brak kart KVK, PLC, hydrauliki lub sterowania urządzeniem;
- wygaśnięta sesja usuwa powierzchnie i kieruje do jawnej bramki PIN.

## 9. Kryteria zgodności DTools

1. Wszystkie polskie etykiety są kompletne i czytelne w docelowym foncie.
2. Każdy ekran zachowuje regiony `64/472/64` i maksymalnie cztery akcje.
3. Każdy cel podstawowy ma co najmniej `64×64 px` i nie nakłada się.
4. Wszystkie stany są rozpoznawalne bez polegania wyłącznie na kolorze.
5. Zabieg nie pokazuje cen, a settlement nie oblicza kwot.
6. Element asysty zawsze ma etykietę `Sugestia` i nie wysyła komendy.
7. Dowód offline zapisuje wersję DTools, natywny artefakt, SHA-256, timestamp
   UTC, log `0 errors` i zrzuty ekranów.
8. Brak obsługi zaokrągleń lub animacji jest zapisany jako jawny downgrade
   dekoracyjny; nie wolno zastępować nim wymagań dotyku, tekstu lub stanów.

## 10. Granice i skutek zatwierdzenia

Zatwierdzenie i późniejszy baseline tego dokumentu ustanawiają wyłącznie język
wizualny w istniejącym zakresie `IA-HC-008`. Nie implementują modelu AI,
diagnozy, autonomicznej rekomendacji, nowych use case'ów ani bindingów. Nie
zezwalają na real data, urządzenia, KVK I/O, machine bus, live RFID, kamerę,
hydraulikę, PLC/safety mutation, sieć/chmurę, upload na panel, deployment,
signing, release ani `HW-A1/HW-A2/HW-A3 = PASS`. `EDGE_HOST_REQUIRED` oraz
PR #77 / R2 pozostają bez zmian.
