# IA-HC-007-A1 — Zootechnician Pricing Access Amendment v0.1

## Status

`APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-007-A1-ACTIVATION-001`

Ten addytywny dodatek nie zmienia historycznego tekstu ani dowodów aktywacji
`IA-HC-007`. Obowiązuje prospektywnie po zgodzie Project Ownera na exact head
PR #86, kontrolowanym merge i pozytywnej Repository Verification zapisanych w
`HC-IA-HC-007-A1-ACTIVATION-001`.

## Podstawa

- `ADR-HC-009` jest kanoniczne po merge PR #83
  `0e13e1d762a332b126358cd2f490d68793249755`;
- Project Owner zatwierdził regułę zamrożenia ceny po pierwszej trwale
  ukończonej krowie;
- `REQ-HC-002-A1` jest `APPROVED / BASELINED` decyzją Project Ownera.

## Prospektywnie autoryzowany zakres

Po aktywacji dodatek MAY autoryzować wyłącznie lokalną, synthetic/test-only
implementację:

- operacyjnej roli Pawła jako zootechnika z dostępem do ustalania cen;
- dozwolonej korekty cen otwartego zlecenia przed pierwszą trwałą sesją
  `COMPLETED`;
- wersjonowanego snapshotu ceny i nieusuwalnego rekordu audytu korekty;
- idempotentnego zdarzenia korekty i fail-closed konfliktu payloadu;
- nieodwracalnego zamrożenia cen po pierwszej przypisanej sesji `COMPLETED`;
- semantycznych view models HMI Generacji 1, niezależnych od rozdzielczości;
- osobnego profilu geometrii GL100E `1024×600` i testów obsługi w rękawicach;
- prezentacyjnego ukrycia cen podczas właściwej pracy przy zwierzęciu;
- testów, dokumentacji i traceability wymaganych dla tego przyrostu.

## Obowiązkowe ograniczenia

- Każdy runtime increment wymaga clean assertion RED, minimalnego GREEN i
  pełnej regresji.
- Wartości pieniężne pozostają całkowitą liczbą groszy; binary `float` jest
  zabroniony.
- Pierwsza trwała sesja `COMPLETED` jest jedynym punktem zamrożenia ceny.
- Strefa właściciela pozostaje oddzielona dla administracji, lecz nie może
  blokować Pawłowi zatwierdzonych operacji cenowych.
- Korekta nie może usuwać poprzedniego snapshotu lub rekordu audytu.
- Brak, uszkodzenie lub konflikt audytu powoduje fail-closed odrzucenie.
- Wszystkie fixture'y i demonstracje pozostają synthetic/test-only.

## Wyłączenia

Dodatek nie autoryzuje:

- korekt po pierwszej sesji `COMPLETED` ani korekt zamkniętego rozliczenia;
- usuwania lub przepisywania historii cen;
- rzeczywistych danych i production credentials/authentication;
- klientów komputerowych, telefonicznych lub tabletowych Generacji 2;
- network/cloud, synchronizacji, remote administration lub aktualizacji;
- live RFID, kamery, device access, realnego KVK I/O lub machine bus;
- commands, writes, configuration, actuation, hydrauliki lub PLC/safety
  mutation;
- fakturowania, VAT, księgowości, płatności lub systemów fiskalnych;
- deploymentu, provisioning, signing, release lub public distribution;
- merge/default-branch mutation bez osobnej zgody exact-head.

## Warunek aktywacji

Aktywacja wymaga łącznie:

1. zatwierdzenia `REQ-HC-002-A1` jako baselined;
2. zgody Project Ownera na exact final head pakietu;
3. kontrolowanego merge z ochroną expected-head;
4. pozytywnej Repository Verification;
5. kanonicznego rekordu aktywacji odróżniającego authority od rozpoczęcia
   implementacji runtime.

## Warunek spełnienia

Dodatek może zostać oznaczony jako fulfilled dopiero po scaleniu i
Repository Verification wszystkich zatwierdzonych inkrementów TDD oraz
udowodnieniu pełnego pokrycia `REQ-HC-002-A1`, z zachowaniem wszystkich
wyłączeń.
