# Zootechnician Pricing Access and Freeze Design

## Status

`APPROVED DESIGN DIRECTION / WRITTEN SPEC REVIEW REQUIRED`

## Cel

Pogodzić kanoniczny `ADR-HC-009` z aktywnym `IA-HC-007` tak, aby Paweł mógł
samodzielnie przygotować całe zlecenie na HMI, ustalić ceny oraz naprawić błąd
wyceny przed rozpoczęciem rozliczanej pracy, bez otwierania korekt historycznych
lub klientów Generacji 2.

## Decyzja

System zachowuje dwa pojęcia dostępu:

1. **zootechnik operacyjny** — Paweł wykonuje cały zabieg, otwiera i zamyka
   zlecenie, ustala ceny oraz korzysta ze statystyk potrzebnych do rozliczenia;
2. **właściciel administracyjny** — odrębna strefa do funkcji administracji,
   audytu i przyszłego zarządzania systemem.

Cena nie jest funkcją wyłącznie właścicielską. PIN właściciela nie jest
wymagany do operacji cenowych Pawła określonych w `REQ-HC-002-A1`.

## Model korekty

Otwarte zlecenie rozpoczyna się od wersji snapshotu ceny `1`. Dozwolona
korekta tworzy kolejną wersję snapshotu i osobny rekord audytu. Poprzednia
wersja pozostaje dostępna do weryfikacji.

Korekta jest dozwolona tylko wtedy, gdy:

- zlecenie ma stan `OPEN`;
- nie ma żadnej trwale przypisanej sesji `COMPLETED`;
- operator, timestamp, przyczyna, stare i nowe wartości są kompletne;
- identyfikator zdarzenia nie koliduje z inną treścią.

Pierwsze trwałe przypisanie sesji `COMPLETED` zamraża snapshot. Od tego momentu
nie istnieje ścieżka zmiany stawki, ceny, jednostki ani precyzji materiału w
tym zleceniu. Korekta zamkniętego rozliczenia pozostaje poza zakresem.

## Granice modułów

### Domena

Model domenowy odpowiada za wersję snapshotu, audyt korekty, idempotencję,
punkt zamrożenia i fail-closed odrzucenie. Nie importuje modułów HMI ani
geometrii urządzenia.

### Warstwa aplikacyjna

Przypadek użycia korekty ładuje trwałe zlecenie, stosuje domenową operację i
atomowo zapisuje nową wersję przed potwierdzeniem sukcesu. Nie dodaje sieci,
chmury ani zdalnego klienta.

### Prezentacja HMI Generacji 1

Semantyczny model ekranu udostępnia Pawłowi ceny podczas otwarcia, dozwolonej
korekty i podsumowania. Rutynowy ekran zabiegu pokazuje ilości bez cen.
GL100E `1024×600` jest osobnym profilem layoutu, a nie parametrem domeny lub
przypadku użycia.

### Strefa właściciela

Strefa właściciela pozostaje oddzielona. Ten przyrost może zawierać jedynie
etykiety lub kontrakty administracyjne wymagane do nawigacji; nie implementuje
production authentication, zarządzania użytkownikami ani korekt zamkniętych
rozliczeń.

## Przepływ danych

1. Paweł otwiera syntetyczne zlecenie i zapisuje snapshot cen v1.
2. Przed pierwszą ukończoną krową może podać przyczynę i nową wartość.
3. Domena waliduje zdarzenie, zachowuje v1 i tworzy v2 wraz z audytem.
4. Warstwa trwałości zapisuje kompletne zlecenie atomowo.
5. Pierwsza sesja `COMPLETED` zostaje zapisana przed aktualizacją zlecenia.
6. Przypisanie tej sesji zamraża aktywną wersję ceny.
7. Każda późniejsza próba korekty kończy się bez zmiany stanu.

## Błędy i zachowanie fail-closed

- Niepusta historia ukończonych sesji blokuje korektę.
- Brak przyczyny, operatora, timestampu lub wartości blokuje korektę.
- Identyczny retry zwraca ten sam stan bez duplikatu audytu.
- Ten sam identyfikator z innym payloadem jest konfliktem.
- Błąd trwałego zapisu nie może pozostawić częściowo zmienionego snapshotu.
- Uszkodzony audit lub niezgodna wersja snapshotu blokuje odczyt zlecenia.
- Prezentacja nie wykonuje własnych obliczeń finansowych.

## Strategia TDD

Implementacja zostanie podzielona na osobne inkrementy:

1. wersjonowany snapshot i domenowy rekord audytu;
2. atomowy zapis/odczyt historii ceny;
3. aplikacyjna operacja korekty i punkt zamrożenia;
4. semantyczny model HMI oraz profil GL100E;
5. pełny syntetyczny przebieg otwarcie → korekta → pierwsza krowa → blokada →
   zamknięcie.

Każdy inkrement wymaga zdalnego clean assertion RED przed kodem produkcyjnym,
minimalnego GREEN, pełnej regresji i osobnej zgody exact-head przed merge.

## Kryteria akceptacyjne

Projekt jest gotowy do planowania implementacji, gdy:

- `REQ-HC-002-A1` jednoznacznie definiuje prawa Pawła i punkt zamrożenia;
- `IA-HC-007-A1` pozostaje nieaktywne do jawnej decyzji właściciela;
- nie istnieje ścieżka korekty po pierwszej ukończonej krowie;
- strefa właściciela nie blokuje zatwierdzonych operacji Pawła;
- HMI pozostaje autonomiczne, a domena niezależna od `1024×600`;
- Generacja 2 i wszystkie granice rzeczywiste/sprzętowe pozostają wyłączone.
