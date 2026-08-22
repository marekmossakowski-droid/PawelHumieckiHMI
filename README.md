# PawelHumieckiHMI / HoofCare

> **Status nazewnictwa:** `PawelHumieckiHMI` i `HoofCare` są wewnętrznymi nazwami kodowymi używanymi dla ciągłości prac inżynierskich. Nie stanowią zatwierdzonej nazwy handlowej ani marki produktu. Docelowa nazwa produktu pozostaje `TBD` i wymaga osobnej decyzji Project Ownera.

Pod aktualną nazwą kodową rozwijany jest przemysłowy system HMI i rejestracji zabiegów korekcji racic, początkowo jako retrofit dla poskromu KVK 801-1 generacji około 2013 r.

## Cel
System ma wspierać operatora podczas pełnego procesu obsługi jednej krowy:

`identyfikacja → wybór kończyny → wybór palca → lokalizacja zmiany → klasyfikacja schorzenia → zabieg → materiały → zdjęcia PRZED/PO → follow-up → raport`

## Granica bezpieczeństwa
System nie zastępuje i nie omija fabrycznych funkcji bezpieczeństwa KVK. Pierwsza generacja integracji z poskromem ma charakter `READ_ONLY`; żadna live KVK integration authority nie jest obecnie aktywna.

## Metodyka
`Foundation → ARS → ARB → ADR → System Architecture → LEL → Requirements → Implementation → Testing → Integration → Release`

Każdy przyrost przechodzi przez osobną gałąź i Draft PR. Merge do `main` wymaga jawnej zgody Project Ownera na końcowy diff i dokładny head SHA.

## Aktualny etap
`WAVE R0 REMEDIATION + ISOLATED BENCH HARDWARE PREPARATION`

Zamknięte techniczne korekty R0:
- exact bench hardware profile: `Kinco GL100E + KS123-14DR`;
- structurally valid local PDF;
- durable completion + evidence-derived acceptance.

Aktualnie przygotowana jest deterministyczna specyfikacja realizacji GL100E w DTools oraz requirement-level traceability. Native DTools artifact nie jest jeszcze udawany ani deklarowany jako istniejący.

Fizyczny etap pozostaje `HW-A1 — WAITING FOR PHYSICAL HARDWARE`.

Stan kanoniczny projektu: [`project_context/CURRENT_STATE.md`](project_context/CURRENT_STATE.md).
