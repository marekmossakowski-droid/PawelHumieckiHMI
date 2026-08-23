# UX-HC-001 — Menu ról, zlecenia, rozliczenia i statystyki v0.1

## Status

`APPROVED DESIGN CONTENT / IA-HC-007 ACTIVE FOR REQ-HC-002 V0.1 SLICE`

Project Owner zatwierdził kierunek funkcjonalny obejmujący:

- osobne menu operatora i właściciela;
- licznik wykonanych krów i zużytych materiałów;
- zlecenie przypisane do gospodarstwa/klienta;
- stawkę netto za krowę obejmującą standardowy zakres i standardowe materiały;
- dodatkowe materiały rozliczane osobno;
- możliwość dodania materiału obowiązującego wyłącznie w bieżącym zleceniu;
- ukrycie cen w trakcie właściwej pracy;
- końcowe zestawienie z kwotą `RAZEM NETTO` w PLN.

PR #80 został scalony jako `3a32e3b5b7d1f5b2693836c044ef73caa63276d3` po zatwierdzeniu exact headu `8901922380a3ec342747088e5acccdcd4ca5b44d` i Repository Verification. `IA-HC-007` aktywuje wyłącznie ograniczony zakres `REQ-HC-002` v0.1; szersze funkcje opisane jako przyszłe nadal wymagają osobnych wymagań i authority. `IA-HC-006` pozostaje oddzielnie ograniczone do `AUD-HC-018`–`AUD-HC-025`.

## 1. Cel

Zapewnić operatorowi szybki, rękawiczkowy workflow zabiegowy oraz kompletne rozliczenie pojedynczego gospodarstwa bez prezentowania cen podczas obsługi kolejnych zwierząt. Zapewnić właścicielowi szerszy wgląd w działalność, katalog materiałów, historię zleceń, statystyki i audyt.

System wspiera przygotowanie rozliczenia usługi. Wersja v0.1 nie wystawia faktury, nie oblicza VAT i nie stanowi systemu księgowego.

## 2. Role i dostęp

### 2.1. Operator — Paweł

Operator może:

- otworzyć zlecenie dla wybranego gospodarstwa;
- wpisać stawkę netto za krowę;
- ustalić ceny dodatkowych materiałów dla zlecenia;
- rozpocząć, wznowić i zakończyć obsługę zwierzęcia;
- rejestrować wykorzystane dodatkowe materiały;
- obserwować liczbę wykonanych krów i ilości materiałów;
- zamknąć zlecenie i zobaczyć końcowe rozliczenie netto;
- wygenerować lokalne podsumowanie PDF.

Operator nie może:

- zmieniać historycznych cen zamkniętego zlecenia bez audytowanej korekty;
- automatycznie dodawać materiału lokalnego do katalogu głównego;
- zarządzać innymi użytkownikami;
- usuwać śladu audytowego;
- korzystać z jakiejkolwiek funkcji sterowania KVK.

### 2.2. Właściciel — Marek

Właściciel ma dostęp do widoku operatora oraz może:

- przeglądać wszystkie zlecenia i statystyki;
- zarządzać klientami/gospodarstwami;
- zarządzać katalogiem dodatkowych materiałów i domyślnymi cenami;
- przenieść materiał lokalny z zamkniętego zlecenia do katalogu głównego jawnie i osobną operacją;
- zarządzać operatorami i uprawnieniami;
- wykonywać audytowane korekty rozliczeń;
- przeglądać diagnostykę własnej aplikacji.

Strefa właściciela jest oddzielona od trybu operatora i chroniona sześciocyfrowym PIN-em z automatyczną blokadą po okresie bezczynności. Ten mechanizm jest wymaganiem projektowym; jego implementacja wymaga osobnej analizy bezpieczeństwa i authority.

## 3. Struktura menu

### 3.1. Menu operatora

Stały dolny pasek zawiera cztery duże pozycje:

| Pozycja | Zawartość |
|---|---|
| `START` | aktywne zlecenie, nowy zabieg, wznowienie, licznik krów i materiałów |
| `KONTROLE` | kontrole na dziś, opóźnione i zakończone |
| `HISTORIA` | wyszukiwanie zwierzęcia, poprzednie zabiegi, zdjęcia i PDF |
| `WIĘCEJ` | podsumowanie zlecenia, proste statystyki, pomoc, zmiana operatora |

### 3.2. Menu właściciela

| Pozycja | Zawartość |
|---|---|
| `PULPIT` | KPI działalności, aktywne zlecenia, kontrole, niekompletne wpisy |
| `DANE` | gospodarstwa, zwierzęta, historia zabiegów i wyszukiwanie |
| `RAPORTY` | zlecenia, okresy, gospodarstwa, materiały i lokalne PDF |
| `ZARZĄDZANIE` | operatorzy, katalog materiałów, szablony, audyt i diagnostyka |

### 3.3. Kreator zabiegu

Kanoniczny przebieg operatora:

`identyfikacja → kończyna i racica → strefa i zmiana → zdjęcia → zabieg → materiały → termin kontroli → podsumowanie → trwały zapis`

Na ekranach kreatora mogą występować najwyżej cztery podstawowe akcje w dolnym pasku: `WSTECZ`, `ZAPISZ SZKIC`, `DALEJ`, `ZAKOŃCZ`.

## 4. Otwarcie zlecenia

Przed rozpoczęciem pracy operator podaje lub wybiera:

- klienta i gospodarstwo;
- datę zlecenia;
- planowaną liczbę krów, jeżeli jest znana;
- stawkę netto za jedną krowę w PLN;
- dodatkowe materiały dostępne w tym zleceniu;
- cenę netto i jednostkę każdego dodatkowego materiału.

Stawka za krowę obejmuje standardowy zakres korekcji i standardowe materiały. Tylko materiały jawnie sklasyfikowane jako dodatkowe są doliczane osobno.

Otwarcie zlecenia tworzy niezmienny snapshot stawek. Późniejsza zmiana katalogu lub cen domyślnych nie zmienia otwartego ani zamkniętego zlecenia.

## 5. Materiały dodatkowe

### 5.1. Katalog główny

Pozycja katalogowa zawiera co najmniej:

- stabilny identyfikator;
- nazwę wyświetlaną;
- jednostkę, np. `szt.`, `ml`, `g`, `m`;
- domyślną cenę netto w PLN;
- stan aktywności;
- wersję lub timestamp obowiązywania.

### 5.2. Materiał lokalny zlecenia

Operator może dodać brakujący materiał przez akcję `+ INNY MATERIAŁ`, podając:

- nazwę;
- jednostkę;
- cenę netto;
- ilość.

Materiał lokalny obowiązuje wyłącznie w bieżącym zleceniu. Nie trafia automatycznie do katalogu głównego. Właściciel może później jawnie utworzyć na jego podstawie nową pozycję katalogową; operacja nie zmienia historycznego zlecenia.

Materiał lokalny można zdefiniować przy otwarciu zlecenia albo dodać później. Dodanie go podczas aktywnej pracy otwiera osobny ekran wyceny, na którym cena jest widoczna wyłącznie podczas zapisu tej pozycji. Po powrocie do kreatora ceny ponownie są ukryte.

### 5.3. Rejestracja podczas pracy

Ekran materiałów prezentuje duże kafle oraz akcje `−` i `+`. Podczas właściwej pracy widoczne są nazwy, jednostki i ilości, ale nie ceny ani bieżąca kwota pieniężna.

Materiał klinicznie związany z konkretnym zwierzęciem jest przypisany do jego ukończonej sesji. Korekta materiału po trwałym zapisie jest audytowaną poprawką, a nie cichym nadpisaniem.

## 6. Liczniki i statystyki operatora

### 6.1. Aktywne zlecenie

Dashboard operatora pokazuje stale:

- gospodarstwo i identyfikator zlecenia;
- `WYKONANE KROWY: n`;
- `PLAN: n / plan`, jeśli plan podano;
- liczbę sesji niedokończonych;
- zagregowane ilości dodatkowych materiałów;
- czas rozpoczęcia i czas trwania zlecenia.

### 6.2. Reguła liczenia krów

Licznik zwiększa się wyłącznie po trwałym zapisaniu kompletnej sesji zwierzęcia. Otwarcie ekranu, rozpoczęcie szkicu, anulowanie lub błąd zapisu nie zwiększają licznika.

Jedno zwierzę jest liczone jeden raz w obrębie zlecenia. Ponowne otwarcie lub audytowana korekta tej samej sesji nie zwiększa licznika. Powtórna, odrębna płatna usługa wymaga jawnie nowej pozycji albo nowego zlecenia.

### 6.3. Statystyki dostępne Pawłowi

Operator może przeglądać:

- liczbę krów w bieżącym zleceniu;
- liczbę krów w bieżącym dniu, łącznie i według gospodarstwa;
- zużycie dodatkowych materiałów w zleceniu i dniu;
- liczbę zabiegów według rodzaju;
- liczbę kontroli, poprawek i sesji niedokończonych;
- listę zamkniętych zleceń z końcową kwotą netto.

## 7. Statystyki właściciela

Właściciel może agregować dane według:

- operatora;
- gospodarstwa;
- dnia, tygodnia, miesiąca i własnego zakresu dat;
- liczby krów;
- rodzaju zabiegu;
- dodatkowego materiału;
- statusu zlecenia i kontroli;
- końcowej wartości netto.

Statystyki finansowe są wyliczane z niezmiennych snapshotów zamkniętych zleceń, nie z aktualnego katalogu cen.

## 8. Widoczność cen

| Etap | Widoczność cen |
|---|---|
| otwieranie zlecenia | pełna: stawka za krowę i dodatkowe materiały |
| właściwa praca przy zwierzęciu | ukryta |
| podgląd liczników zlecenia | ilości bez cen |
| ekran przed zamknięciem | pełne zestawienie do kontroli |
| zamknięte zlecenie | pełne, historyczne zestawienie netto |

Ukrycie ceny dotyczy prezentacji. Snapshot cen pozostaje częścią trwałego rekordu zlecenia przez cały jego cykl życia.

## 9. Kalkulacja

Wszystkie wartości pieniężne są przechowywane jako całkowita liczba groszy. Obliczenia nie wykorzystują binarnych liczb zmiennoprzecinkowych.

Definicje:

- `C` — liczba trwale ukończonych i rozliczanych krów;
- `P` — stawka netto za jedną krowę w groszach;
- `Qᵢ` — rozliczana ilość dodatkowego materiału `i`;
- `Mᵢ` — cena netto jednostki materiału `i` w groszach.

Formuła:

`RAZEM_NETTO = C × P + Σ(Qᵢ × Mᵢ)`

Ilości niecałkowite są dozwolone wyłącznie dla jednostek, które je dopuszczają. Katalog określa precyzję ilości od zera do trzech miejsc dziesiętnych. Wartość każdej pozycji jest liczona arytmetyką dziesiętną i zaokrąglana do pełnego grosza metodą `ROUND_HALF_UP`; suma końcowa jest sumą już zaokrąglonych pozycji. Kwota końcowa jest prezentowana w formacie `1 556,00 zł`.

## 10. Zamknięcie zlecenia

Przed zamknięciem system pokazuje:

| Pozycja | Ilość | Cena netto | Wartość netto |
|---|---:|---:|---:|
| Korekcja krów | `C` | `P` | `C × P` |
| Materiał dodatkowy | `Qᵢ` | `Mᵢ` | `Qᵢ × Mᵢ` |

Na dole widoczna jest dominująca pozycja `RAZEM NETTO: X XXX,XX zł`.

Zamknięcie jest blokowane, jeżeli:

- istnieje aktywna lub niezidentyfikowana sesja;
- trwały zapis którejkolwiek rozliczanej sesji nie został potwierdzony;
- cena lub jednostka dodatkowego materiału jest brakująca albo nieprawidłowa;
- wynik kalkulacji nie może zostać wyliczony deterministycznie;
- występuje konflikt tożsamości zwierzęcia lub zlecenia.

Po potwierdzeniu zlecenie otrzymuje niezmienny identyfikator rozliczenia, timestamp zamknięcia, identyfikator operatora oraz lokalny PDF. Zamknięte zlecenie nie jest fakturą VAT.

## 11. Korekty i audyt

Korekta zamkniętego zlecenia wymaga:

- roli właściciela;
- podania przyczyny;
- zapisu wartości poprzedniej i nowej;
- identyfikatora wykonującego zmianę;
- timestampu;
- nowej wersji podsumowania/PDF bez usuwania poprzedniej wersji.

Historia nie może być cicho przeliczona po zmianie katalogu, stawki lub materiału.

## 12. Błędy i zachowanie fail-closed

- Nieudany zapis sesji nie zwiększa licznika krów ani rozliczenia.
- Nieudany zapis materiału nie zwiększa ilości ani kwoty.
- Ponowienie tego samego zdarzenia nie może podwójnie naliczyć krowy ani materiału.
- Brak ceny blokuje zamknięcie, ale nie powoduje automatycznego podstawienia wartości.
- Awaria HMI nie może zmienić już trwale zatwierdzonych liczników i snapshotu cen.
- Odtworzenie po restarcie musi rozróżniać zlecenie otwarte, zamknięte i wymagające uzgodnienia.

## 13. Granica danych i bezpieczeństwa

Projekt pozostaje lokalny i offline-first. Do czasu osobnej decyzji o danych wszystkie testy i demonstracje używają wyłącznie syntetycznych gospodarstw, zwierząt, cen i materiałów.

Moduł nie zapewnia i nie może pośrednio tworzyć:

- sterowania KVK, hydrauliką, bramami, wciągarkami lub PLC;
- modyfikacji układów bezpieczeństwa;
- realnego KVK I/O lub live RFID;
- komunikacji sieciowej/chmurowej;
- zewnętrznej wysyłki raportów;
- fakturowania, księgowania, płatności ani funkcji fiskalnych;
- wdrożenia, podpisywania, release ani publicznej dystrybucji.

## 14. Kryteria akceptacyjne przyszłej implementacji

Przyszła implementacja wymaga testów TDD obejmujących co najmniej:

1. licznik rośnie dopiero po trwałym ukończeniu sesji;
2. ponowienie nie powoduje podwójnego naliczenia;
3. stawka i ceny są snapshotem zlecenia;
4. ceny są ukryte w ekranach pracy;
5. cena jest widoczna przy otwarciu i zamknięciu;
6. standardowe materiały nie są doliczane drugi raz;
7. materiał dodatkowy jest naliczany według ilości i ceny snapshotu;
8. materiał lokalny nie trafia automatycznie do katalogu głównego;
9. zmiana katalogu nie przelicza historii;
10. końcowa suma netto jest liczona w groszach i zgodna z pozycjami;
11. brak ceny lub niekompletna sesja blokuje zamknięcie;
12. korekta zamkniętego zlecenia tworzy audytowaną nową wersję;
13. operator i właściciel widzą wyłącznie właściwe dla roli powierzchnie;
14. żaden ekran nie udostępnia sterowania maszyną;
15. pełny przebieg działa na syntetycznych danych bez sieci i urządzeń fizycznych.

## 15. Zależności przed implementacją

Wymagane są:

- osobne Implementation Authority dla `UX-HC-001`;
- implementowalne wymagania dla zlecenia, cennika, materiałów, ról, statystyk i rozliczeń;
- decyzja architektoniczna dla trwałego modelu zlecenia i snapshotu cen;
- decyzja bezpieczeństwa dla uwierzytelniania właściciela;
- plan implementacji z obowiązkowym TDD;
- utrzymanie lokalnego synthetic/test-only zakresu aż do osobnej zgody na dane rzeczywiste.
