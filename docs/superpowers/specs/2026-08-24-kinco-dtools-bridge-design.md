# Kinco DTools Bridge — projekt prototypu lokalnego v0.1

## Status i decyzja

`DESIGN APPROVED IN CHAT / WRITTEN SPECIFICATION PENDING PROJECT OWNER REVIEW`

Dokument utrwala zatwierdzony projekt lokalnego mostu MCP dla Kinco DTools na
Windows 11. Prototyp służy wyłącznie do realizacji ekranów
`synthetic/test-only` dla profilu GL100E i nie rozszerza `IA-HC-008`.

## Cel

Zapewnić agentowi kontrolowany, audytowalny dostęp do interfejsu Kinco DTools,
aby mógł odczytywać stan aplikacji i autonomicznie wykonywać dozwolone działania
projektowe bez prowadzenia operatora przez ręczne kliknięcia.

Pierwszy pion ma wykazać, że most potrafi:

1. wykryć właściwy proces DTools i projekt `HoofCare_GL100E_G1`;
2. odczytać strukturę UI oraz obraz okna;
3. wejść w poprawny kontekst edytora grafiki bitmapowej `.bg`;
4. wybrać lub utworzyć grafikę `.bg` i załadować wskazany BMP;
5. zweryfikować wynik po operacji;
6. zatrzymać się przed zapisem projektu i poprosić o zgodę.

## Granice authority i bezpieczeństwa

Dozwolony zakres obejmuje wyłącznie:

- proces Kinco DTools;
- projekt testowy `HoofCare_GL100E_G1`;
- lokalne artefakty ekranów GL100E;
- katalog konfiguracji i dzienników Bridge;
- lokalne działania UI wymagane do tworzenia ekranów synthetic/test-only.

Bezwzględnie zabronione są:

- dostęp do PLC, KVK, HMI lub innych urządzeń;
- użycie portów COM, Ethernet, USB lub magistral urządzeń;
- konfiguracja komunikacji lub urządzeń;
- pobieranie, upload, download, transfer albo deployment projektu;
- funkcje sterowania maszyną;
- rozszerzenie `IA-HC-008`;
- nasłuch sieciowy poza interfejsem loopback;
- ogólny shell lub dowolne wykonywanie poleceń przekazanych przez MCP.

Policy Engine odrzuca akcję przed wykonaniem, jeżeli nazwa procesu, tytuł
projektu, kontekst okna, rodzaj kontrolki albo oczekiwany rezultat są
niejednoznaczne. Blokady działań związanych z `Download`, `PLC`, `COM`,
`Ethernet`, `Device` i `Transfer` nie mogą zostać uchylone potwierdzeniem
operatora.

## Wybrana architektura

Pierwszy prototyp będzie napisany w Pythonie i spakowany do lokalnego programu
Windows. Wykorzysta kolejno:

1. Windows UI Automation do semantycznego odczytu i aktywacji kontrolek;
2. Win32 do obsługi elementów starszego interfejsu MFC niewidocznych w UIA;
3. analizę zrzutu okna jako źródło obserwacji i weryfikacji;
4. klik współrzędnościowy wyłącznie jako jawnie oznaczony ostatni fallback,
   ograniczony do prostokąta wcześniej zidentyfikowanego okna DTools.

Komponenty prototypu:

- `DToolsLocator` — identyfikuje proces, okno główne i dokładny projekt;
- `UiInspector` — zwraca drzewo UIA/Win32 i zrzut wyłącznie okna DTools;
- `ActionPolicy` — sprawdza allowlistę i denylistę przed każdą akcją;
- `DToolsController` — wykonuje dozwolone akcje i weryfikuje stan po operacji;
- `SessionGuard` — zarządza tokenem sesji, awaryjnym STOP i stanem fail-closed;
- `AuditLog` — zapisuje rekordy JSONL oraz referencje do zrzutów przed i po;
- `McpServer` — udostępnia mały, typowany zestaw narzędzi bez generic execute.

## Interfejs MCP v0.1

Prototyp udostępni wyłącznie następujące operacje:

- `dtools_status()` — proces, tytuł projektu, aktywne okno i stan blokady;
- `dtools_inspect()` — ograniczone drzewo UI i metadane kontrolek;
- `dtools_capture()` — zrzut klienta DTools z identyfikatorem audytowym;
- `dtools_activate(control_id)` — aktywacja kontrolki z allowlisty;
- `dtools_open_menu(menu_path)` — otwarcie dozwolonej ścieżki menu;
- `dtools_set_text(control_id, value)` — tekst tylko w dozwolonym polu;
- `dtools_send_shortcut(shortcut_id)` — wyłącznie nazwany skrót z allowlisty;
- `dtools_run_step(step)` — pojedynczy krok wysokiego poziomu z pre/postcondition;
- `dtools_request_save()` — tworzy żądanie potwierdzenia, ale nie zapisuje;
- `dtools_emergency_stop()` — natychmiast blokuje dalsze działania.

`control_id`, `menu_path`, `shortcut_id` i `step` są wartościami typowanymi z
lokalnej konfiguracji. Interfejs nie przyjmuje współrzędnych, nazw procesów,
ścieżek wykonywalnych ani dowolnych sekwencji klawiszy od klienta MCP.

## Przepływ działania

Każda akcja przechodzi tę samą sekwencję:

1. Bridge sprawdza aktywną sesję i token.
2. `DToolsLocator` potwierdza właściwy proces oraz projekt.
3. `UiInspector` zapisuje stan i zrzut przed operacją.
4. `ActionPolicy` ocenia akcję, kontekst i allowlistę.
5. `DToolsController` wykonuje pojedynczą dozwoloną operację.
6. `UiInspector` odczytuje stan po operacji.
7. Kontroler porównuje wynik z deklarowaną postcondition.
8. `AuditLog` zapisuje decyzję, metodę, rezultat i referencje do dowodów.

Brak oczekiwanego stanu, pojawienie się nieznanego okna dialogowego, zmiana
projektu albo utrata DTools powodują `STOPPED_FAIL_CLOSED`. Wznowienie wymaga
lokalnej decyzji operatora i nowej inspekcji stanu.

## Tryb autonomiczny i potwierdzenia

Wybrano tryb `AUTONOMOUS_BOUNDED`:

- agent samodzielnie wykonuje dozwolone operacje projektowe;
- zapis projektu wymaga pojedynczego potwierdzenia operatora;
- zamknięcie projektu lub DTools wymaga potwierdzenia operatora;
- nieoczekiwane okno wymaga zatrzymania i decyzji operatora;
- globalny skrót `Ctrl+Alt+F12` wymusza awaryjny STOP;
- zabronione działania pozostają niemożliwe niezależnie od potwierdzenia.

## Instalacja i transport

Pierwszy etap używa lokalnego MCP na tym samym Windows 11:

- instalacja per-user, bez uprawnień administratora;
- brak usługi systemowej i brak autostartu;
- ręczne uruchomienie Bridge tylko na czas pracy z DTools;
- nasłuch wyłącznie na `127.0.0.1` albo transport `stdio`;
- losowy token generowany przy każdym uruchomieniu;
- klient Codex działający lokalnie na Windows łączy się z MCP;
- konfiguracja zapisuje wyłącznie dozwolony katalog projektu i logów;
- odinstalowanie nie usuwa automatycznie logów ani kopii projektu.

Drugi etap może dodać dostęp z czatu WWW przez szyfrowane połączenie wychodzące.
Jest to osobny pion, domyślnie wyłączony i nieobjęty implementacją prototypu v0.1.

## Dane audytowe

Każdy rekord JSONL zawiera co najmniej:

- identyfikator sesji i monotoniczny numer operacji;
- UTC timestamp;
- nazwę narzędzia i typowaną akcję;
- hash konfiguracji allowlisty;
- PID, klasę okna oraz rozpoznany tytuł projektu;
- decyzję policy (`ALLOW` albo kod odmowy);
- użyty mechanizm (`UIA`, `WIN32`, `VISION_FALLBACK`);
- wynik postcondition;
- identyfikatory zrzutów przed i po;
- informację, czy wymagano potwierdzenia operatora.

Log nie zapisuje danych uwierzytelniających ani pełnej zawartości dowolnych pól
tekstowych. Ścieżki są ograniczone do katalogu projektu i katalogu Bridge.

## Obsługa błędów

- Nie znaleziono DTools: brak akcji, `DTOOLS_NOT_FOUND`.
- Niewłaściwy projekt: brak akcji, `PROJECT_MISMATCH`.
- Więcej niż jedno pasujące okno: brak akcji, `AMBIGUOUS_WINDOW`.
- Nieznana kontrolka lub dialog: `STOPPED_FAIL_CLOSED`.
- Niezgodna postcondition: `STOPPED_FAIL_CLOSED` i dowody przed/po.
- Próba działania zabronionego: `DENIED_PERMANENT_BOUNDARY`.
- Awaryjny STOP: przerwanie kolejki i odrzucenie kolejnych działań.
- Utrata klienta MCP: brak nowych działań; DTools pozostaje otwarty.

Bridge nie próbuje automatycznie zamykać dialogu, cofać nieznanej operacji ani
zapisywać projektu po błędzie.

## Strategia testów

Implementacja przebiega test-first. Warstwy weryfikacji:

1. testy jednostkowe `ActionPolicy`, tokenu sesji i redakcji logów;
2. testowy emulator okien Windows odtwarzający wymagane kontrolki i dialogi;
3. testy integracyjne UIA/Win32 przeciwko emulatorowi;
4. testy fail-closed dla zmiany procesu, projektu, dialogu i postcondition;
5. test awaryjnego STOP i odrzucenia kolejki;
6. test pakietu instalacyjnego w czystym profilu użytkownika;
7. kontrolowana próba z prawdziwym DTools i kopią projektu testowego;
8. ręczne potwierdzenie, że żadne źródło PLC, COM, Ethernet ani urządzenie nie
   zostało skonfigurowane lub użyte.

Test na prawdziwym DTools nie obejmuje zapisu bez osobnego potwierdzenia,
kompilacji, downloadu ani połączenia z HMI.

## Kryteria akceptacji prototypu

Prototyp v0.1 jest gotowy do review, gdy:

- działa na Windows 11 bez praw administratora;
- udostępnia wyłącznie zdefiniowane narzędzia MCP;
- rozpoznaje DTools i dokładny projekt lub zatrzymuje się fail-closed;
- potrafi wejść do edytora bitmapy i załadować wskazany BMP do `.bg`;
- każdą operację potwierdza odczytem stanu po akcji;
- blokuje wszystkie zabronione powierzchnie w testach negatywnych;
- awaryjny STOP działa niezależnie od połączenia MCP;
- tworzy kompletny log JSONL i zrzuty przed/po;
- zatrzymuje się przed zapisem;
- nie uzyskuje dostępu do PLC, KVK, urządzeń ani funkcji pobierania.

## Poza zakresem v0.1

- sterowanie dowolną aplikacją inną niż DTools;
- zdalny pulpit;
- agent działający jako administrator;
- dostęp przez czat WWW lub publiczny Internet;
- automatyczny zapis albo zamknięcie projektu;
- kompilacja, upload, download lub deployment;
- odczyt albo modyfikacja plików projektu poza dozwolonym katalogiem;
- operacyjne połączenie z HMI, PLC, KVK lub innym urządzeniem.
