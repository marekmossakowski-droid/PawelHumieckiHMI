# REQ-HC-002 — Role, zlecenia, rozliczenia i statystyki v0.1

## Status

`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

Ten pakiet materializuje pierwszą część wizji `UX-HC-001`: role, zlecenia, ceny, materiały dodatkowe, liczniki, rozliczenie i ich statystyki. Szczegółowe funkcje kontroli, analityki klinicznej i korekt rozliczeń pozostają przyszłymi przyrostami z osobnymi wymaganiami i authority.

## 1. Role

### REQ-HC-JOB-ROLE-001 — Menu operatora

System SHALL udostępnić operatorowi powierzchnie `START`, `KONTROLE`, `HISTORIA` i `WIĘCEJ` oraz nie eksponować funkcji właścicielskich bez odblokowania roli właściciela.

### REQ-HC-JOB-ROLE-002 — Menu właściciela

System SHALL udostępnić właścicielowi powierzchnie `PULPIT`, `DANE`, `RAPORTY` i `ZARZĄDZANIE` oraz możliwość wejścia w widok operatora.

### REQ-HC-JOB-ROLE-003 — Ochrona właściciela

Strefa właściciela SHALL wymagać sześciocyfrowego PIN-u i SHALL blokować się automatycznie po okresie bezczynności określonym w przyszłej konfiguracji bezpieczeństwa.

## 2. Otwarcie zlecenia

### REQ-HC-JOB-OPEN-001 — Kontekst

Otwarcie SHALL wymagać identyfikatora syntetycznego gospodarstwa, operatora, daty i stawki netto za krowę w PLN. Planowana liczba krów MAY być pusta.

### REQ-HC-JOB-OPEN-002 — Snapshot cen

System SHALL zapisać snapshot stawki za krowę i stawek materiałów dodatkowych. Zmiana katalogu SHALL NOT zmienić istniejącego snapshotu.

### REQ-HC-JOB-OPEN-003 — Standardowy zakres

Stawka za krowę SHALL obejmować standardowy zakres i standardowe materiały. System SHALL NOT doliczać ich drugi raz.

## 3. Materiały dodatkowe

### REQ-HC-JOB-MAT-001 — Katalog

Materiał dodatkowy SHALL mieć stabilny kod, nazwę, jednostkę, cenę netto w groszach, precyzję ilości zero–trzy oraz stan aktywności.

### REQ-HC-JOB-MAT-002 — Materiał lokalny

Operator SHALL móc dodać materiał lokalny do otwartego zlecenia. Pozycja SHALL obowiązywać wyłącznie w tym zleceniu i SHALL NOT automatycznie modyfikować katalogu głównego.

### REQ-HC-JOB-MAT-003 — Trwałe zużycie

Zużycie materiału SHALL wpływać na licznik i rozliczenie dopiero po trwałym zapisie zdarzenia. Ponowienie tego samego zdarzenia SHALL być idempotentne.

## 4. Liczenie krów

### REQ-HC-JOB-COUNT-001 — Źródło prawdy

Liczba wykonanych krów SHALL być pochodna z unikalnych, trwale zapisanych sesji `COMPLETED` przypisanych do zlecenia.

### REQ-HC-JOB-COUNT-002 — Brak fałszywego naliczenia

Szkic, anulowanie, nierozwiązana tożsamość, błąd zapisu, ponowienie i korekta tej samej sesji SHALL NOT zwiększyć licznika.

### REQ-HC-JOB-COUNT-003 — Widoczność

Operator SHALL widzieć licznik bieżącego zlecenia oraz dzienny licznik łączny i według gospodarstwa.

## 5. Ceny i kalkulacja

### REQ-HC-JOB-PRICE-001 — Widoczność

Ceny SHALL być widoczne przy otwieraniu, na osobnym ekranie dodania materiału lokalnego oraz przed i po zamknięciu. SHALL być ukryte w rutynowym kreatorze zabiegu i ekranie liczników.

### REQ-HC-JOB-PRICE-002 — Reprezentacja

Kwoty SHALL być przechowywane jako całkowita liczba groszy. Ilości SHALL używać arytmetyki dziesiętnej, nigdy binarnego `float` do kalkulacji pieniężnej.

### REQ-HC-JOB-PRICE-003 — Formuła

System SHALL obliczać `RAZEM_NETTO = C × P + Σ(Qᵢ × Mᵢ)`, zaokrąglając każdą pozycję materiałową do grosza metodą `ROUND_HALF_UP` i sumując zaokrąglone pozycje.

## 6. Zamknięcie

### REQ-HC-JOB-CLOSE-001 — Blokady

Zamknięcie SHALL być zablokowane przy aktywnej/nierozwiązanej sesji, niepotwierdzonym zapisie, brakującej cenie/jednostce albo niedeterministycznej kalkulacji.

### REQ-HC-JOB-CLOSE-002 — Podsumowanie

Ekran zamknięcia SHALL pokazać pozycje, ilości, ceny netto, wartości netto i dominujące `RAZEM NETTO: X XXX,XX zł`.

### REQ-HC-JOB-CLOSE-003 — Trwały wynik

Zamknięcie SHALL zapisać identyfikator rozliczenia, timestamp, operatora, snapshot pozycji i sumę oraz SHALL umożliwić lokalny PDF.

## 7. Statystyki

### REQ-HC-JOB-STAT-001 — Operator

Operator SHALL móc przeglądać liczbę krów, ilości materiałów, liczbę i statusy swoich zleceń oraz zamknięte sumy netto, w tym widok dzienny łączny i według gospodarstwa.

### REQ-HC-JOB-STAT-002 — Właściciel

Właściciel SHALL móc agregować liczbę zleceń, krów, ilości materiałów i wartości netto według operatora, gospodarstwa, zakresu dat i statusu zlecenia.

### REQ-HC-JOB-STAT-003 — Pochodzenie

Statystyki SHALL być obliczane z trwałych rekordów i historycznych snapshotów, a nie z mutowalnego katalogu lub przejściowego stanu ekranu.

## 8. Granice

### REQ-HC-JOB-SAF-001 — Brak sterowania

Żaden ekran SHALL NOT udostępniać KVK I/O, machine bus, hydrauliki, PLC, konfiguracji ani aktuacji.

### REQ-HC-JOB-DATA-001 — Synthetic-only

Do czasu osobnej decyzji wszystkie dane gospodarstw, operatorów, zwierząt, cen i materiałów SHALL być synthetic/test-only i lokalne.

### REQ-HC-JOB-FIN-001 — Brak funkcji księgowych

Podsumowanie SHALL NOT być przedstawiane jako faktura, dokument fiskalny, płatność ani księgowanie.
