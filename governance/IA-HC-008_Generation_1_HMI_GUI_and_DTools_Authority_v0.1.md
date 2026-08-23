# IA-HC-008 — Generation 1 HMI GUI and DTools Authority v0.1

## Status

`PROPOSED / NOT ACTIVE`

## Prospektywny zakres

Po osobnym zatwierdzeniu treści, kontrolowanym merge, Repository Verification i
kanonicznej aktywacji authority MAY zezwolić wyłącznie na lokalną,
synthetic/test-only implementację `REQ-HC-003-G1 v0.1`:

- semantyczny graf ekranów i route guards Generacji 1;
- pełny lokalny workflow Pawła jako zootechnika;
- powierzchnie zleceń, dozwolonych cen, materiałów, liczników, statystyk,
  settlementu, historii i raportów wykorzystujące istniejące use case'y;
- syntetyczną lokalną bramkę PIN strefy właściciela i presentation-only admin;
- adaptacyjne komponenty oraz profil GL100E `1024×600`;
- manifest ekranów i bindingów DTools;
- natywny projekt Kinco DTools oraz offline build/compile, jeśli toolchain jest
  dostępny i wersja/hash/log zostaną utrwalone;
- syntetyczne adaptery, testy, dokumentację i traceability.

## Obowiązkowe ograniczenia

- Każdy pion G1-1..G1-6 wymaga clean assertion RED, zdalnego test-only
  checkpointu, minimalnego GREEN, pełnej regresji i osobnego Draft PR.
- Każdy finalny head wymaga osobnej zgody Project Ownera przed merge.
- GUI korzysta wyłącznie z kanonicznych usług; nie duplikuje obliczeń ani
  persistence.
- Brak kanonicznego use case oznacza brak aktywnej akcji GUI.
- Pierwsza sesja `COMPLETED` zachowuje nieodwracalne zamrożenie cen.
- Rutynowy ekran zabiegu nie pokazuje cen ani kwot.
- Wszystkie dane, credentials i bindingi pozostają syntetyczne/testowe.
- DTools offline compile nie jest uploadem, deploymentem ani HW-A3 PASS.
- `EDGE_HOST_REQUIRED / NOT YET SELECTED` pozostaje blokadą operacyjnego
  połączenia HMI z aplikacją.

## Jawne wyłączenia

Authority nie obejmuje Generation 2; real data; korekt zamkniętego rozliczenia;
network/cloud lub synchronizacji; live RFID, kamery, device access, KVK I/O lub
machine bus; commands do maszyny, sterowania lub hydrauliki; PLC/safety mutation;
invoicing, VAT, księgowości lub płatności; produkcyjnego
authentication/credentials; uploadu na fizyczny HMI, HW-A1/HW-A2/HW-A3 PASS;
deploymentu, signing, release ani public distribution. Nie obejmuje merge lub
mutacji `main` bez osobnej zgody exact-head. PR #77 i R2 pozostają bez zmian.

## Bramka aktywacji

Runtime pozostaje zabroniony, dopóki łącznie nie wystąpią:

1. zatwierdzenie treści `REQ-HC-003-G1`, `UX-HC-002`, planu i tego authority;
2. zgoda Project Ownera na exact final head pakietu;
3. kontrolowany merge z ochroną expected-head;
4. pozytywna Repository Verification exact merge tree;
5. osobny rekord aktywacji `IA-HC-008 = APPROVED / ACTIVE`;
6. clean assertion RED pierwszego pionu runtime.

## Bieżący skutek

This proposal grants no implementation authority. Samo opublikowanie pakietu
nie zezwala na implementację GUI ani projektu Kinco DTools.
