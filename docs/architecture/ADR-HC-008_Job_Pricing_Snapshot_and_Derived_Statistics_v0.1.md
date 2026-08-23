# ADR-HC-008 — Snapshot cen zlecenia i statystyki pochodne v0.1

## Status

`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## Kontekst

Operator musi znać liczbę wykonanych krów i zużyte materiały dla konkretnego gospodarstwa, a po zamknięciu zlecenia otrzymać deterministyczną kwotę netto w PLN. Ceny mają być ustawiane przy otwarciu zlecenia, ukryte podczas rutynowej pracy i ponownie widoczne w podsumowaniu. Zmiana katalogu nie może przeliczać historii.

## Decyzja

1. Zlecenie jest odrębnym agregatem domenowym powiązanym z gospodarstwem, operatorem i sesjami zwierząt.
2. Otwarcie zlecenia zapisuje snapshot stawki netto za krowę oraz stawek dodatkowych materiałów.
3. Standardowy zakres i standardowe materiały są zawarte w stawce za krowę; tylko jawne materiały dodatkowe tworzą osobne pozycje rozliczenia.
4. Materiał lokalny może rozszerzyć snapshot wyłącznie otwartego zlecenia. Nie modyfikuje katalogu głównego.
5. Kwoty są przechowywane jako całkowita liczba groszy w walucie PLN.
6. Ilości materiałów są dziesiętne z precyzją zero–trzy miejsca, zgodnie z definicją pozycji.
7. Wartość pozycji materiałowej jest zaokrąglana do grosza metodą `ROUND_HALF_UP`; suma netto jest sumą zaokrąglonych pozycji.
8. Liczniki i statystyki są pochodne z trwałych rekordów zleceń i sesji. Nie istnieje niezależny, ręcznie inkrementowany licznik będący źródłem prawdy.
9. Zamknięcie zlecenia tworzy niezmienny snapshot rozliczenia. Mechanizm korekt pozostaje poza zakresem v0.1 i będzie wymagał osobnej decyzji projektowej.
10. Podsumowanie jest rozliczeniem usługi, nie fakturą, dokumentem fiskalnym ani księgowym.

## Konsekwencje

- aktualny `LocalSessionStore` nie staje się magazynem zleceń; powstaje osobny `LocalJobStore`;
- warstwa aplikacyjna koordynuje sesje i zlecenie przez jawne identyfikatory;
- HMI nie oblicza ani nie przechowuje kanonicznej kwoty; prezentuje wynik serwisu aplikacyjnego;
- raport zlecenia jest generowany wyłącznie z zamkniętego, trwałego rekordu;
- ponowienie zdarzenia z tym samym identyfikatorem jest idempotentne;
- błąd trwałego zapisu nie zmienia licznika ani kwoty.

## Odrzucone warianty

### Bieżący katalog jako źródło cen historycznych

Odrzucono, ponieważ zmiana ceny przeliczałaby stare zlecenia i niszczyła audytowalność.

### Jeden ręcznie edytowany licznik krów

Odrzucono, ponieważ może rozjechać się z trwałymi sesjami po restarcie, ponowieniu lub korekcie.

### `float` dla pieniędzy

Odrzucono z powodu niedeterministycznych błędów reprezentacji binarnej.

## Granice

Decyzja dotyczy wyłącznie lokalnego modelu synthetic/test-only. Nie zezwala na realne dane gospodarstw, fakturowanie, płatności, chmurę, live RFID, KVK I/O, sterowanie maszyną, wdrożenie ani dystrybucję.
