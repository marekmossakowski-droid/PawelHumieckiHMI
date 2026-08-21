# PawelHumieckiHMI / HoofCare

> **Naming status:** `PawelHumieckiHMI` and `HoofCare` are internal project codenames used for engineering continuity. They are not an approved commercial/product brand. The final product name remains `TBD` and requires a separate Project Owner decision.

Under the current codename, the project develops an industrial HMI and hoof-treatment record system, initially as a retrofit for a KVK 801-1 chute from approximately the 2013 generation.

## Cel

System ma wspierać operatora podczas pełnego procesu obsługi jednej krowy:

`identyfikacja → wybór kończyny → wybór palca → lokalizacja zmiany → klasyfikacja schorzenia → zabieg → materiały → zdjęcia PRZED/PO → follow-up → raport`

Docelowo system ma dostarczać użyteczne dane dla rolnika, zootechnika, lekarza weterynarii i żywieniowca oraz statystyki stada.

## Granica bezpieczeństwa

System nie zastępuje i nie omija fabrycznych funkcji bezpieczeństwa KVK. Pierwsza generacja integracji z poskromem ma charakter `READ_ONLY`: odczyt i rejestracja stanów bez sterowania hydrauliką, bramami, wciągarkami, E-STOP ani innymi funkcjami wykonawczymi.

## Metodyka

Projekt używa tej samej dyscypliny rozwoju co VoltOps:

`Foundation → ARS → ARB → ADR → System Architecture → LEL → Requirements → Implementation → Testing → Integration → Release`

Każdy przyrost przechodzi przez osobną gałąź i Draft PR. Merge do `main` wymaga jawnej zgody Project Ownera na końcowy diff i dokładny head SHA.

## Aktualny etap

`FOUNDATION / GOVERNANCE INITIALIZATION`

Stan kanoniczny projektu: [`project_context/CURRENT_STATE.md`](project_context/CURRENT_STATE.md).
