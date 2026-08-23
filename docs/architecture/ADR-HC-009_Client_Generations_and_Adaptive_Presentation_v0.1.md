# ADR-HC-009 — Generacje klientów i adaptacyjna warstwa prezentacji v0.1

## Status

`APPROVED DESIGN CONTENT / NO IMPLEMENTATION AUTHORITY`

Project Owner zatwierdził 23.08.2026 rozdzielenie systemu na autonomiczną
Generację 1 opartą na HMI oraz przyszłą Generację 2 obejmującą komputer,
telefon i tablet. Niniejsza decyzja koryguje interpretację, według której całe
GUI miałoby być projektowane wyłącznie dla stałego płótna `1024×600`.

Dokument nie aktywuje implementacji klientów Generacji 2, komunikacji zdalnej,
sieci, chmury, aktualizacji zdalnych ani administracyjnego write-path.

## 1. Kontekst

Pierwszy fizyczny profil projektu wykorzystuje przemysłowy panel Kinco GL100E
10,1 cala o rozdzielczości `1024×600`. Jest to profil realizacyjny HMI, a nie
ograniczenie wspólnej domeny, usług aplikacyjnych ani przyszłego systemu
prezentacji.

Paweł działa w systemie jako zootechnik i wykonuje na HMI cały proces zabiegu.
Jego rola obejmuje również dostęp do cen netto, ustalanie cen przy otwieraniu
zlecenia i ich kontrolowane korygowanie. Ukrywanie cen podczas właściwej pracy
przy zwierzęciu jest regułą prezentacji, a nie odebraniem uprawnienia.

W przyszłości komputer ma służyć do przygotowywania zleceń, pobierania
raportów i statystyk oraz administracji oprogramowaniem HMI. Telefon i tablet
mają w kolejnej generacji umożliwiać Pawłowi pełną obsługę zabiegu, lecz ich
implementacja nie należy do Generacji 1.

## 2. Decyzja

### 2.1. Generacja 1 — autonomiczne HMI

Generacja 1 implementuje samodzielny interfejs HMI. Brak komputera, telefonu,
tabletu, sieci lub chmury nie może blokować:

- przygotowania i otwarcia zlecenia;
- wyboru gospodarstwa i operatora;
- ustalenia stawki netto za krowę i cen dodatkowych materiałów;
- kontrolowanej korekty cen w dozwolonym stanie zlecenia;
- identyfikacji zwierzęcia i pełnego przebiegu zabiegu;
- rejestracji dodatkowych materiałów;
- trwałego liczenia ukończonych krów;
- prezentacji statystyk bieżącego dnia i zlecenia;
- zamknięcia zlecenia i prezentacji `RAZEM NETTO`;
- utworzenia lokalnego raportu oraz dostępu do historii;
- lokalnej diagnostyki i administracji przewidzianej osobnym authority.

GL100E `1024×600` pozostaje pierwszym zweryfikowanym profilem fizycznym.
Konkretne współrzędne i testy geometrii tego profilu pozostają ważne, ale nie
mogą przenikać do modelu domenowego ani usług aplikacyjnych.

### 2.2. Generacja 2 — przyszli klienci

Generacja 2 może objąć następujące niezależne profile prezentacji:

| Klient | Docelowa odpowiedzialność |
|---|---|
| komputer/laptop | przygotowanie zleceń, gospodarstwa, cenniki, raporty, statystyki, backup, użytkownicy, diagnostyka i kontrolowane zarządzanie wersją HMI |
| tablet | pełny workflow zootechnika dostosowany do orientacji pionowej i poziomej |
| telefon | pełny workflow zootechnika, w tym ceny, korekty, zabieg, materiały, zamknięcie i statystyki |

Powyższa tabela definiuje kierunek produktowy, nie gotowe interfejsy ani
authority. Każdy klient Generacji 2 wymaga osobnych wymagań, threat modelu,
decyzji o synchronizacji, authentication, ochronie danych i Implementation
Authority.

## 3. Podział odpowiedzialności

System zachowuje zależności skierowane od prezentacji do stabilnych usług:

`profil urządzenia → komponenty prezentacji → usługi aplikacyjne → domena`

- domena zawiera reguły zleceń, cen, materiałów, liczników, korekt i statystyk;
- usługi aplikacyjne udostępniają jawne przypadki użycia bez zależności od
  rozdzielczości ekranu;
- warstwa prezentacji mapuje przypadki użycia na konkretne urządzenie;
- profil urządzenia definiuje układ, gęstość, nawigację, orientację i minimalne
  cele dotykowe;
- żadna warstwa kliencka nie implementuje własnego alternatywnego sposobu
  wyliczania kwoty netto lub liczby krów.

## 4. Adaptacyjna prezentacja

Projekt wspólnych komponentów nie może opierać się na globalnych sztywnych
współrzędnych. Powinien wykorzystywać semantyczne regiony, tokeny odstępów,
typografii i celów dotykowych oraz reguły przepływu treści.

Profile mogą różnić się:

- liczbą kolumn i zagęszczeniem informacji;
- nawigacją dolną, boczną lub panelową;
- orientacją oraz sposobem prezentacji tabel;
- liczbą jednocześnie widocznych danych i akcji;
- rozmiarem kontrolek oraz wymaganiami obsługi w rękawicach.

Profile nie mogą różnić się semantyką operacji, regułami finansowymi,
uprawnieniami roli ani audytem. Krytycznych elementów nie wolno jedynie
pomniejszać do dostępnego obszaru; układ musi je przeorganizować.

## 5. Rola zootechnika

Paweł ma na HMI pełne uprawnienia operacyjne zootechnika w zatwierdzonym
zakresie produktu:

- wykonuje cały zabieg;
- przygotowuje i zamyka zlecenie;
- widzi i ustala ceny przy otwieraniu zlecenia;
- może wykonać kontrolowaną korektę ceny;
- widzi pełne rozliczenie netto przed i po zamknięciu;
- korzysta ze statystyk potrzebnych do rozliczenia gospodarstwa.

Korekta ceny nie może cicho zastąpić istniejącej wartości. Wymaga co najmniej
zapisu wartości poprzedniej i nowej, operatora, czasu oraz przyczyny. Korekta
zamkniętego rozliczenia pozostaje odrębną, wersjonowaną operacją wymagającą
osobnego zatwierdzonego zakresu implementacji.

## 6. Przyszła administracja komputerowa

Administracja z komputera oznacza przyszłą, kontrolowaną powierzchnię do:

- odczytu wersji, stanu i diagnostyki aplikacji HMI;
- pobierania raportów, statystyk i kopii danych;
- przygotowania danych zleceń i cenników;
- tworzenia i weryfikacji kopii bezpieczeństwa;
- przygotowania kontrolowanej aktualizacji oprogramowania.

Nie oznacza ona sterowania KVK, hydrauliką, PLC, safety ani automatycznego
wykonywania aktualizacji. Kanał komunikacji, podpisy pakietów, rollback,
authentication, authorization i procedura potwierdzenia wymagają przyszłych
ADR oraz authority.

## 7. Dane i synchronizacja

Generacja 1 pozostaje lokalna i offline-first. Kontrakty danych powinny być
wersjonowane tak, aby w przyszłości umożliwić eksport raportów i synchronizację
bez migracji reguł biznesowych do klienta komputerowego.

Preferowany przyszły kierunek to lokalna komunikacja w zaufanym, jawnie
skonfigurowanym środowisku oraz podpisany eksport/import jako tryb awaryjny.
Chmura nie jest elementem tej decyzji.

## 8. Zachowane granice

Ta decyzja:

- nie dodaje klienta komputerowego, telefonicznego ani tabletowego;
- nie aktywuje sieci, cloud, remote access ani synchronizacji;
- nie dodaje production authentication lub credentials;
- nie autoryzuje aktualizacji, deploymentu, signing ani release;
- nie rozszerza dostępu do rzeczywistych danych gospodarstw, klientów,
  operatorów, zwierząt lub cen;
- nie dodaje live RFID, kamery, device access, machine bus ani KVK I/O;
- nie tworzy sterowania, hydrauliki ani mutation PLC/safety;
- nie modyfikuje zakresu PR #77 ani nie zamyka R2.

## 9. Konsekwencje

1. Dalszy projekt GUI nie może opisywać `1024×600` jako jedynego docelowego
   urządzenia całego systemu.
2. Testy geometrii GL100E pozostają obowiązkowe dla profilu Generacji 1.
3. Nowa logika zleceń i rozliczeń musi być testowana bez zależności od GUI.
4. Elementy wspólne powinny mieć semantyczne kontrakty umożliwiające późniejsze
   profile, bez implementowania ich przed czasem.
5. Generacja 2 pozostaje `PLANNED / NOT IMPLEMENTED / AUTHORITY REQUIRED`.

## 10. Kryteria zgodności przyszłej implementacji

Implementacja Generacji 1 jest zgodna z decyzją, jeżeli:

- HMI realizuje pełny workflow Pawła bez udziału zewnętrznego urządzenia;
- logika zleceń, cen i statystyk nie importuje modułów prezentacji;
- `1024×600` jest profilem layoutu, a nie właściwością przypadków użycia;
- ceny są dostępne Pawłowi w dozwolonych etapach i ukryte jedynie podczas
  właściwej pracy przy zwierzęciu;
- korekty pozostawiają wymagany ślad audytowy;
- brak klientów Generacji 2 nie tworzy atrap sieciowych ani nieaktywnych
  powierzchni zdalnego sterowania.
