# DTools Startup and Offline Build Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Uruchamiać most MCP niezależnie od bieżącej dostępności okna DTools, a następnie wystawić wyłącznie nazwane operacje utworzenia świeżego projektu GL100E i kompilacji offline.

**Architecture:** Proces MCP rejestruje katalog narzędzi przed próbą połączenia z DTools. Warstwa odroczonego połączenia ustanawia i buforuje dokładnie jedno zweryfikowane połączenie z zatwierdzonym plikiem wykonywalnym oraz projektem; niedostępność okna jest stanem obserwowalnym, nie błędem startu serwera. Operacje zapisu i kompilacji pozostają osobnym, allowlistowanym profilem bez ogólnego wykonania poleceń, uploadu lub dostępu do urządzeń.

**Tech Stack:** Python 3.13, MCP 2.x, pywinauto 0.6.8, Windows 11, Kinco DTools, unittest.

**Spec:** `docs/requirements/REQ-HC-003_Generation_1_Complete_HMI_GUI_and_DTools_v0.1.md`

## Global Constraints

- Wyłącznie projekt `HoofCare_GL100E_G1`, model Kinco GL100E i rozdzielczość `1024x600`.
- Brak uploadu/downloadu/transferu na panel, device I/O, KVK I/O, PLC i funkcji bezpieczeństwa.
- Dokładny hash programu DTools i katalog projektu pozostają obowiązkowe.
- Każda mutacja jest nazwaną operacją z precondition, postcondition, audit logiem i fail-closed.
- Kompilacja offline zapisuje wersję DTools, pełny log oraz SHA-256 źródła i artefaktu.

---

### Task 1: Startup-resilient MCP registration

**Files:**
- Create: `src/hoofcare/dtools_bridge/deferred_backend.py`
- Modify: `src/hoofcare/dtools_bridge/__main__.py`
- Modify: `src/hoofcare/dtools_bridge/server.py`
- Test: `tests/test_dtools_bridge_deferred_backend.py`
- Test: `tests/test_dtools_bridge_server.py`

**Interfaces:**
- Consumes: `DToolsBackend`, `WindowsDToolsBackend.connect_exact`.
- Produces: `DeferredDToolsBackend.connection_status() -> dict[str, object]` oraz pełny kontrakt `DToolsBackend` delegowany po udanym połączeniu.

- [ ] Napisz test, w którym katalog MCP powstaje mimo `DTOOLS_NOT_FOUND`, a `dtools_status` zwraca `available=false` bez zatrzymania sesji.
- [ ] Uruchom test i potwierdź RED wynikający z braku `DeferredDToolsBackend`.
- [ ] Dodaj minimalny odroczony backend i użyj go w `__main__.py` bez wywołania `connect_exact` podczas startu.
- [ ] Uruchom test celowany i potwierdź GREEN.
- [ ] Uruchom cały zestaw `test_dtools_bridge*.py`.

### Task 2: Fresh-project workspace admission

**Files:**
- Modify: `src/hoofcare/dtools_bridge/diagnostics.py`
- Modify: `src/hoofcare/dtools_bridge/__main__.py`
- Test: `tests/test_dtools_bridge_diagnostics.py`

**Interfaces:**
- Consumes: jawny `--project-directory` oraz dozwolony suffix projektu.
- Produces: deterministyczny status `NATIVE_PROJECT_COUNT_INVALID` dla pustego katalogu bez awarii procesu MCP.

- [ ] Napisz test pustego, istniejącego katalogu projektu i oczekuj blokady `native_project`.
- [ ] Uruchom test i potwierdź właściwy RED.
- [ ] Usuń wymóg obecności natywnego `.dpj` przy starcie, zachowując wymóg istniejącego, jawnie wybranego katalogu.
- [ ] Uruchom test celowany i pełne testy diagnostyczne.

### Task 3: Named fresh-project and offline-compile contract

**Files:**
- Modify: `src/hoofcare/dtools_bridge/model.py`
- Modify: `src/hoofcare/dtools_bridge/backend.py`
- Modify: `src/hoofcare/dtools_bridge/controller.py`
- Modify: `src/hoofcare/dtools_bridge/policy.py`
- Modify: `src/hoofcare/dtools_bridge/server.py`
- Modify: `dtools/gl100e/bridge/allowlist.json`
- Test: `tests/test_dtools_bridge_controller.py`
- Test: `tests/test_dtools_bridge_policy.py`
- Test: `tests/test_dtools_bridge_server.py`

**Interfaces:**
- Consumes: zatwierdzony `dtools/gl100e/manifest.json` i dokładny kontekst UI.
- Produces: `dtools_create_fresh_gl100e_project` oraz `dtools_compile_offline`; bez parametrów ścieżki, współrzędnych i surowych klawiszy.

- [ ] Napisz testy katalogu narzędzi, allowlisty, odmowy złego kontekstu i braku upload/download.
- [ ] Uruchom je i potwierdź RED dla brakujących nazwanych operacji.
- [ ] Dodaj minimalny kontrakt kontrolera i backendu bez ogólnego executora.
- [ ] Uruchom testy i potwierdź GREEN.

### Task 4: Verified Windows UI profile and evidence package

**Files:**
- Modify: `src/hoofcare/dtools_bridge/windows_backend.py`
- Modify: `scripts/windows/dtools_bridge/DToolsBridgeEmulator.py`
- Create: `scripts/windows/dtools_bridge/Run-DToolsBridge-Automation.cmd`
- Modify: `scripts/windows/dtools_bridge/Build-DToolsBridge.ps1`
- Modify: `scripts/windows/dtools_bridge/Install-DToolsBridge.ps1`
- Test: `tests/test_dtools_bridge_windows.py`
- Test: `tests/test_dtools_bridge_package.py`

**Interfaces:**
- Consumes: rzeczywisty profil menu/kontrolek DTools odczytany przez Task 1.
- Produces: natywny `.dpj/.whe`, wynik kompilacji offline, pełny log i SHA-256.

- [ ] Napisz Windows RED przeciwko emulatorowi dla utworzenia projektu, zapisu i kompilacji.
- [ ] Potwierdź RED na Windows CI.
- [ ] Zaimplementuj wyłącznie zweryfikowane semantyczne ścieżki menu/kontrolek.
- [ ] Potwierdź GREEN na emulatorze i realnym DTools.
- [ ] Zapisz wersję DTools, hash programu, hash projektu, hash artefaktu, log i zrzuty przed/po.

