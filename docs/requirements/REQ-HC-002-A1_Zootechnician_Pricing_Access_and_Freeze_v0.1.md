# REQ-HC-002-A1 — Dostęp zootechnika do cen i punkt zamrożenia v0.1

## Status

`PROPOSED — PROJECT OWNER BASELINE APPROVAL REQUIRED`

Niniejszy dodatek precyzuje `REQ-HC-002 v0.1` zgodnie z kanonicznym
`ADR-HC-009`. Nie zmienia historycznych wymagań ani nie aktywuje implementacji.

## 1. Rola Pawła

### REQ-HC-JOB-ROLE-A1-001 — Pełny workflow zootechnika

System SHALL umożliwić Pawłowi, działającemu jako zootechnik, przygotowanie,
otwarcie, wykonanie i zamknięcie syntetycznego zlecenia na autonomicznym HMI
Generacji 1 bez udziału komputera, telefonu, tabletu, sieci lub chmury.

### REQ-HC-JOB-ROLE-A1-002 — Ceny nie są funkcją wyłącznie właścicielską

Paweł SHALL móc ustalić stawkę netto za krowę oraz ceny dodatkowych materiałów
przy otwieraniu zlecenia. Strefa właściciela MAY pozostawać odrębna dla
administracji, audytu i zarządzania systemem, lecz SHALL NOT być wymagana do
wykonania powyższych operacji cenowych przez Pawła.

### REQ-HC-JOB-ROLE-A1-003 — Ukrycie prezentacyjne

Ceny SHALL być ukryte w rutynowych ekranach pracy przy zwierzęciu. Ukrycie
SHALL NOT usuwać uprawnienia Pawła do cen na ekranie otwarcia, dozwolonej
korekty oraz podsumowania przed i po zamknięciu.

## 2. Korekta otwartego zlecenia

### REQ-HC-JOB-PRICE-A1-001 — Dozwolone okno korekty

Paweł SHALL móc skorygować stawkę za krowę lub cenę dodatkowego materiału
wyłącznie, gdy zlecenie pozostaje otwarte i liczba trwale przypisanych sesji
`COMPLETED` wynosi zero.

### REQ-HC-JOB-PRICE-A1-002 — Punkt zamrożenia

Trwałe przypisanie pierwszej unikalnej sesji `COMPLETED` do zlecenia SHALL
nieodwracalnie zamrozić snapshot cen tego zlecenia. Po tym zdarzeniu próba
zmiany stawki, ceny, jednostki lub precyzji materiału SHALL zakończyć się
fail-closed bez zmiany snapshotu.

### REQ-HC-JOB-PRICE-A1-003 — Audyt korekty

Każda dozwolona korekta SHALL zapisać nieusuwalny rekord zawierający:

- identyfikator zdarzenia korekty;
- identyfikator zlecenia;
- identyfikator operatora;
- timestamp ze strefą czasową;
- niepustą przyczynę;
- pole podlegające korekcie;
- wartość poprzednią i nową jako całkowitą liczbę groszy.

Ponowienie tego samego identyfikatora zdarzenia z identyczną treścią SHALL być
idempotentne. Ponowienie z inną treścią SHALL zostać odrzucone fail-closed.

### REQ-HC-JOB-PRICE-A1-004 — Brak przeliczenia historii

Korekta przed punktem zamrożenia SHALL utworzyć nową wersję snapshotu wraz z
rekordem audytu. Nie może usuwać poprzedniej wersji ani zmieniać katalogu
głównego. Ponieważ przed korektą nie istnieje rozliczana sesja `COMPLETED`,
operacja SHALL NOT przeliczać wykonanych krów ani historycznego rozliczenia.

## 3. Granice

Dodatek nie obejmuje:

- korekty po pierwszej ukończonej krowie;
- korekty zamkniętego rozliczenia;
- fakturowania, VAT, księgowości lub płatności;
- rzeczywistych danych gospodarstw, klientów, operatorów, zwierząt lub cen;
- klientów Generacji 2, synchronizacji, sieci, chmury lub remote access;
- live RFID, kamery, device access, KVK I/O, machine bus, sterowania,
  hydrauliki lub PLC/safety mutation;
- production authentication, deploymentu, signing, release lub publicznej
  dystrybucji.

## 4. Minimalne dowody TDD

Implementacja wymaga co najmniej testów dowodzących, że:

1. Paweł może ustawić ceny przy otwarciu bez odblokowania strefy właściciela;
2. korekta przed pierwszą sesją `COMPLETED` tworzy nową wersję i audyt;
3. identyczne ponowienie korekty nie tworzy duplikatu;
4. konflikt identyfikatora zdarzenia jest odrzucany;
5. pierwsza trwała sesja `COMPLETED` zamraża ceny;
6. po zamrożeniu każda korekta ceny jest odrzucana bez mutacji;
7. ceny pozostają ukryte w roboczym ekranie zabiegu;
8. zamknięte rozliczenie pozostaje niezmienne;
9. żaden interfejs nie tworzy dostępu do KVK ani klienta Generacji 2.
