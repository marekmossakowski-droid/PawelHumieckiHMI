# UX-HC-002 — Generation 1 Complete HMI GUI and DTools Design v0.1

## Status

`DRAFT / CONTENT APPROVAL REQUIRED / IMPLEMENTATION NOT AUTHORIZED`

## 1. Decyzja projektowa

Wybrano architekturę semantycznego GUI z osobnym profilem urządzenia i
natywną realizacją DTools:

`domena → usługi aplikacyjne → semantyczne view modele → profil GL100E → DTools`

Domena pozostaje jedynym miejscem reguł cen, zamrożenia, liczników, settlementu
i klinicznego zapisu. GUI organizuje pracę i prezentuje stan. Profil GL100E
definiuje geometrię. DTools odwzorowuje manifest, ale nie tworzy alternatywnej
logiki biznesowej.

Rozważono i odrzucono:

1. monolityczny projekt DTools ze sztywną logiką w rejestrach — szybki, lecz
   duplikuje reguły i wiąże produkt z `1024×600`;
2. klient webowy jako pierwszy interfejs — ułatwia responsywność, lecz narusza
   decyzję o autonomicznej Generacji 1 i przedwcześnie otwiera sieć;
3. wybrany wariant semantyczny — większa dyscyplina bindingów, ale zachowuje
   offline-first HMI i przygotowuje przyszłe profile bez ich implementowania.

## 2. Granica architektury

Kanoniczne persistence i raportowanie pozostają poza HMI. Fizyczny host
aplikacyjny nadal ma status `EDGE_HOST_REQUIRED / NOT YET SELECTED`. Dlatego
pakiet może doprowadzić do kompletnego semantycznego GUI, profilu GL100E,
symulowanych bindingów i natywnego projektu DTools z offline compile, ale nie
może deklarować operacyjnego połączenia GUI z produkcyjnym runtime.

GL100E↔KS123-14DR pozostaje osobnym, lokalnym zakresem bench I/O. Nie wolno
wykorzystać tej magistrali jako ukrytego kanału do domeny, realnego KVK lub
sterowania maszyną.

## 3. Komponenty

| Komponent | Odpowiedzialność | Nie wykonuje |
|---|---|---|
| `Gen1RouteGraph` | ekrany, przejścia, guards, recovery | persistence i obliczenia |
| `Gen1AppShellView` | nagłówek, status, rola, cztery akcje | logika domenowa |
| `JobOpeningView` | gospodarstwo, plan, snapshot cen | własne ceny domyślne |
| `TreatmentWizardView` | pełny zabieg i walidacja kroków | diagnoza automatyczna |
| `WorkStatisticsView` | liczniki i materiały bez cen | drugi magazyn liczników |
| `SettlementView` | zapisane linie i `RAZEM NETTO` | przeliczanie settlementu |
| `OwnerZoneView` | lokalna bramka i admin surfaces | blokowanie operacji Pawła |
| `DeviceProfile` | regiony, typografia, dotyk | semantyka operacji |
| `DToolsManifest` | ekran/widget/binding/stan | reguły finansowe i kliniczne |

## 4. Mapa ekranów Generacji 1

| ID | Ekran | Główne wyjścia |
|---|---|---|
| G1-00 | Start / recovery | pulpit, uzgodnienie, diagnostyka |
| G1-10 | Pulpit Pawła | nowe zlecenie, aktywne zlecenie, statystyki, więcej |
| G1-20 | Wybór gospodarstwa i operatora | ceny, anuluj |
| G1-21 | Otwarcie i ceny | zatwierdź snapshot, wróć |
| G1-22 | Dozwolona korekta ceny | zapisz korektę, anuluj |
| G1-30 | Identyfikacja zwierzęcia | dalej, ręczne dane syntetyczne, anuluj |
| G1-31 | Kończyna / racica | wybór, wstecz, dalej |
| G1-32 | Strefa / zmiana | wybór kliniczny, wstecz, dalej |
| G1-33 | Zabieg | wybór zabiegu, wstecz, dalej |
| G1-34 | Materiały | ilości, inny materiał, wstecz, dalej |
| G1-35 | Kontrola | termin lub brak kontroli, wstecz, dalej |
| G1-36 | Podsumowanie krowy | zapisz szkic, ukończ, wstecz |
| G1-40 | Statystyki pracy | filtry, historia, pulpit |
| G1-41 | Historia zleceń | szczegóły, PDF, pulpit |
| G1-42 | Zamknięcie zlecenia | potwierdź, korekta ceny jeśli dozwolona, wróć |
| G1-43 | Zamknięte rozliczenie | PDF, historia, pulpit |
| G1-50 | PIN właściciela | odblokuj, anuluj |
| G1-51 | Pulpit właściciela | dane, raporty, zarządzanie, audyt |
| G1-52 | Administracja lokalna | gospodarstwa, materiały, operatorzy |
| G1-53 | Diagnostyka | statusy, wersje, eksport dowodów lokalnych |
| G1-60 | Uzgodnienie / błąd | ponów bez duplikacji, wróć bez zapisu, diagnostyka |

Kamera i live RFID nie otrzymują aktywnych akcji. Jeżeli przyszły ekran ich
wymaga, pokazuje jawny stan `NIEDOSTĘPNE W GENERACJI 1 / AUTHORITY REQUIRED`.

## 5. Nawigacja i stan

- Widok jest projekcją kanonicznego stanu, nie magazynem procesu.
- Każdy route guard zwraca `ALLOW`, `DENY_WITH_REASON` albo
  `RECOVERY_REQUIRED`.
- `WSTECZ` cofa wyłącznie dane nietrwałego formularza danego kroku.
- Opuszczenie brudnego formularza wymaga `ZAPISZ SZKIC` albo `ODRZUĆ ZMIANY`.
- Po restarcie system ładuje zlecenie i sesję, a następnie wyznacza bezpieczny
  ekran; nie odtwarza ślepo ostatniego numeru ekranu.
- Brak danych obowiązkowych usuwa akcję kończącą albo pokazuje przyczynę
  blokady bez automatycznego uzupełnienia.

## 6. Widoczność i role

Paweł wykonuje cały operacyjny workflow. Widzi ceny na G1-21, G1-22, G1-42 i
G1-43, ale nie na G1-30..G1-36 ani G1-40. Pierwsza trwała sesja `COMPLETED`
usuwa akcję korekty cen zgodnie z `REQ-HC-002-A1`.

Strefa właściciela daje dostęp do administracji i audytu, nie do funkcji
sterowania. Syntetyczny PIN ma dokładnie sześć cyfr, limit prób, jawny stan
blokady po pięciu błędnych próbach przez pięć minut i automatyczne wygaśnięcie
sesji po dziesięciu minutach bezczynności. Czas jest zależnością wstrzykiwaną;
nie wolno przedstawiać tego mechanizmu jako produkcyjnego authentication.

## 7. Profil GL100E

Profil `gl100e-landscape-v1` ma płótno `1024×600`:

- nagłówek: `x=0, y=0, w=1024, h=64`;
- treść: `x=0, y=64, w=1024, h=472`;
- pasek akcji: `x=0, y=536, w=1024, h=64`;
- maksymalnie cztery akcje podstawowe;
- minimalny cel dotykowy `64×64 px`;
- brak nakładania, wyjścia poza płótno i tekstu krytycznego poza regionem;
- stany błędu nie mogą polegać wyłącznie na kolorze.

Wartość `1024×600` nie występuje w domenie ani usługach aplikacyjnych. Inne
profile będą osobnymi mapowaniami tych samych kontraktów, ale nie należą do
tego workstreamu.

## 8. DTools

Repozytorium przechowuje czytelny manifest ekranów i bindingów oraz, po
aktywacji authority i dostępie do toolchainu, natywny projekt DTools. Dla
każdego widgetu manifest zapisuje:

- `screen_id`, `widget_id`, typ i region;
- semantyczny `binding_id` oraz kierunek `READ` lub `COMMAND_REQUEST`;
- warunki widoczności i dostępności;
- fail-closed wartość braku danych;
- test geometrii i oczekiwany tekst polski.

`COMMAND_REQUEST` oznacza wyłącznie wywołanie zatwierdzonego lokalnego use case,
np. zapis sesji lub zamknięcie zlecenia. Nie oznacza komendy do KVK. Dopóki
edge host i transport aplikacyjny nie zostaną wybrane, bindingi używają
syntetycznego adaptera testowego i nie deklarują fizycznego protokołu.

## 9. Obsługa błędów

| Sytuacja | Zachowanie GUI |
|---|---|
| brak/konflikt zwierzęcia | blokada ukończenia, ekran uzgodnienia |
| nieudany zapis | brak sukcesu i brak zmiany licznika, bezpieczne ponowienie |
| duplikat identycznego zdarzenia | ten sam wynik, bez podwójnego naliczenia |
| konflikt payloadu | odmowa fail-closed z identyfikatorem zdarzenia |
| niespójny snapshot | tylko diagnostyka i uzgodnienie, brak mutacji |
| niedostępna funkcja urządzenia | jawne `NIEDOSTĘPNE`, bez atrap danych |
| brak edge hosta | symulator/binding test-only, brak deklaracji połączenia |

## 10. Weryfikacja i kryteria ukończenia

Każdy pion przechodzi RED→GREEN i pełną regresję. Semantyczne testy pokrywają
route guards, role, widoczność cen, brak obliczeń w GUI, restart i błędy.
Geometria pokrywa wszystkie ekrany GL100E. DTools wymaga natywnego projektu,
offline compile, hashów i zgodności manifestu.

Workstream może być uznany za wykonany synthetic/offline dopiero po merge i
Repository Verification wszystkich pionów G1-1..G1-6. Nawet wtedy fizyczna
akceptacja pozostaje `BLOCKED` do HW-A1/HW-A3, wyboru edge hosta, uploadu i
testu dotyku na realnym panelu.

## 11. Zachowane granice

Brak klientów Generation 2, real data, network/cloud, synchronizacji, live
RFID, kamery, device access, KVK I/O, sterowania, hydrauliki, PLC/safety
mutation, invoicing, VAT, księgowości, płatności, produkcyjnego authentication,
deploymentu, signing, release i public distribution. PR #77 i R2 pozostają bez
zmian.
