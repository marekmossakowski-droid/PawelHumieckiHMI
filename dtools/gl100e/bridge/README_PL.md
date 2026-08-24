# Kinco DTools Bridge v0.1.10 — uruchomienie na Windows 11

Zakres tego prototypu to wyłącznie lokalny, syntetyczny projekt
`HoofCare_GL100E_G1`. Bridge nie udostępnia narzędzi PLC, KVK, urządzeń,
transferu, uploadu ani downloadu projektu.

Zainstalowany launcher uruchamia Bridge wyłącznie z `--read-only` i udostępnia
trzy narzędzia: `dtools_status`, `dtools_inspect` oraz `dtools_capture`.

## 1. Zbuduj pakiet

Wymagane są Windows 11 oraz Python 3.13 dostępny przez launcher `py`.
Uruchom zwykły PowerShell w katalogu rozpakowanego repozytorium:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\windows\dtools_bridge\Build-DToolsBridge.ps1
```

Skrypt tworzy odizolowane środowisko, uruchamia testy Windows przeciwko
emulatorowi i buduje katalog `dist\HoofCare.DToolsBridge`.

## 2. Zainstaluj per-user

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\windows\dtools_bridge\Install-DToolsBridge.ps1
```

Instalator pokaże dwa okna wyboru:

1. wskaż rzeczywisty plik wykonywalny Kinco DTools;
2. wskaż wyłącznie folder kopii testowej `HoofCare_GL100E_G1`.

Program trafi do `%LOCALAPPDATA%\HoofCare\DToolsBridge`. Konfiguracja zapisze
kanoniczne ścieżki i SHA-256 wybranego programu. Instalator nie tworzy usługi,
autostartu ani reguł sieciowych.

## 3. Podłącz lokalnego klienta MCP

Oficjalna dokumentacja OpenAI potwierdza obsługę lokalnych serwerów STDIO przez
ChatGPT desktop, Codex CLI i rozszerzenie IDE. W ChatGPT desktop wybierz
`Settings → MCP servers → Add server`, tryb `STDIO`, a jako polecenie wskaż:

```text
%LOCALAPPDATA%\HoofCare\DToolsBridge\Run-DToolsBridge.cmd
```

Alternatywnie w Codex CLI:

```powershell
codex mcp add hoofcare-dtools -- "$env:LOCALAPPDATA\HoofCare\DToolsBridge\Run-DToolsBridge.cmd"
codex mcp list
```

Po dodaniu uruchom ponownie klienta i sprawdź `/mcp`. ChatGPT w przeglądarce
nie odczytuje lokalnej konfiguracji MCP; bezpośrednie sterowanie w v0.1 wymaga
klienta działającego na tym samym Windows.

Dokumentacja: <https://developers.openai.com/codex/mcp/>

## 4. Pierwsza próba — tylko odczyt

Otwórz w DTools kopię testową `HoofCare_GL100E_G1`, pozostaw ekran `HMI0.whe`
i wykonaj wyłącznie:

1. `dtools_status`;
2. `dtools_inspect`;
3. `dtools_capture`.

Narzędzie `dtools_request_save` nie jest dostępne w katalogu read-only. Globalny
skrót awaryjny nie jest rejestrowany w tym trybie, ponieważ launcher nie
udostępnia żadnej operacji zmieniającej stan.
Po próbie prześlij `audit.jsonl` oraz zrzuty z katalogu
`%LOCALAPPDATA%\HoofCare\DToolsBridge\logs` do analizy profilu UI.

Krok `load_g1_00_bitmap` pozostaje celowo zablokowany jako
`PROFILE_STEP_UNVERIFIED` poza emulatorem, dopóki odczyt realnego DTools nie
potwierdzi semantycznej ścieżki kontrolki.
