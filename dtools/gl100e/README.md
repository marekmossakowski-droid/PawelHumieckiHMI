# HoofCare G1 — pakiet przekazania Kinco DTools / GL100E

## Stan

`NATIVE_DTOOLS_ARTIFACT_REQUIRED / OFFLINE COMPILE NOT YET EVIDENCED`

Ten katalog zawiera zweryfikowany manifest realizacyjny dla Kinco GL100E
`1024×600`. Nie zawiera jeszcze natywnego projektu utworzonego przez Kinco
DTools i nie wolno przedstawiać go jako projektu skompilowanego.

## Granice

- wyłącznie dane syntetyczne/testowe;
- brak konfiguracji KVK, PLC, hydrauliki, live RFID i kamery;
- brak uploadu na panel, deploymentu i fizycznej akceptacji;
- brak produkcyjnego transportu — `EDGE_HOST_REQUIRED / NOT YET SELECTED`;
- akcje `COMMAND_REQUEST` oznaczają tylko zatwierdzone lokalne przypadki użycia
  aplikacji, nigdy komendy maszyny.

## Pliki wejściowe

- `manifest.json` — kanoniczna lista 21 ekranów, widgetów, bindingów i geometrii;
- `../../docs/design/UX-HC-002-A1_iOS_Industrial_Visual_System_v0.1.md` —
  baselined system wizualny `G1-LIGHT-A`, exact source blob
  `8bf33ec97cd98d015545cd2720d39765510a6b9d`;
- `../../docs/design/UX-HC-002_Generation_1_Complete_HMI_GUI_and_DTools_v0.1.md`
  — zatwierdzony projekt semantyczny;
- `../../docs/prototype/GL100E-DTOOLS-SPEC-001_v0.1.md` — wcześniejsza
  specyfikacja realizacyjna; manifest G1 jest nadrzędny dla pełnej mapy ekranów.

## Procedura na Windows 11

1. Uruchomić zainstalowany Kinco DTools i zapisać dokładny numer wersji.
2. Utworzyć nowy projekt dla dokładnego modelu `Kinco GL100E`, płótno
   `1024×600`.
3. Utworzyć 21 ekranów zgodnie z `screens[].screen_id` i `route_id`.
4. Dla każdego ekranu odwzorować `widgets[]`, polskie etykiety i geometrię
   `x/y/width/height` bez modyfikowania bindingów.
5. Zastosować font, minimalny rozmiar tekstu i pełną paletę z sekcji
   `visual_system`; nie zastępować stanów samym kolorem.
6. Bindingi `READ` odwzorować jako prezentacyjne zmienne testowe. Bindingi
   `COMMAND_REQUEST` połączyć wyłącznie z lokalną nawigacją ekranów.
7. Nie dodawać urządzeń, adresów PLC/Modbus, KVK, sieci, live RFID ani kamery.
8. Uruchomić `Tools -> Compile All` i wymagać `Error 0` oraz dokładnie jednego
   natywnego artefaktu `.pkg` albo `.pkgx`.
9. Zapisać natywny projekt z rozszerzeniem nadanym przez DTools — nie zmieniać
   rozszerzenia i nie tworzyć tekstowego zamiennika.

## Pakiet wyniku do zwrotu

Należy przekazać jeden katalog lub ZIP zawierający:

- natywny plik projektu DTools;
- eksportowany pełny log build/compile z wynikiem `0 errors`;
- plik tekstowy z dokładnym numerem wersji DTools;
- zrzut ekranu ustawień modelu `GL100E / 1024×600`;
- zrzut ekranu wyniku kompilacji;
- zrzuty wszystkich 21 ekranów.

Po otrzymaniu pakietu repozytorium zapisze jego rzeczywiste ścieżki, SHA-256 i
timestamp UTC w `native_artifact` manifestu. Dopiero wtedy status może przejść
na `OFFLINE_COMPILE_VERIFIED` po ponownej walidacji. Nadal nie będzie to upload,
deployment ani `HW-A1/HW-A2/HW-A3 = PASS`.

## Lokalna kontrola manifestu

Z katalogu głównego repozytorium:

```powershell
$env:PYTHONPATH = "src"
python scripts/check_gen1_dtools_manifest.py
python -m unittest tests.test_gen1_gl100e_layout tests.test_gen1_dtools_manifest -v
```
