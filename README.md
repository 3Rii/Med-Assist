# Med-Assist
IO school project
Projekt: Med-Assist
Dokumentacja

Wprowadzenie
Aplikacja webowa, która analizuje podane informacje, na podstawie których proponuje Użytkownikowi wykonanie szczepień, badań profilaktycznych oraz badań okresowych.

Propozycje badań, przypomnienia badań dalej w instrukcji są nazwane “wynikami” ze względu na to, że zależą od wyników analizy danych w bazie.

 1. Szczegóły techniczne
Narzędzia: język python3 z frameworkiem Flask
Baza danych: MySQL
Hosting: local hosting, darmowy hosting online

 2. Konta
Założenie konta zapewnia dostęp do aplikacji, dane osobowe poza adresem mailowym nie muszą być autentyczne, służą jedynie identyfikacji Użytkownika celem powiązania go z informacjami w formularzu, ich analizy oraz wyświetlenia wyniku analizy (propozycji szczepień lub badań). Prawdziwe pozostają dane podane w formularzarzu oraz adres e-mail. (Nie ma weryfikacji adresu mailowego ani wysyłania maili zwrotnych)

 a) Rejestracja
Zawiera pola do wypełnienia: Nazwa, E-mail, Nazwa Użytkownika, Hasło. Jeśli Nazwa Użytkownika lub E-mail istnieją już w bazie, pojawi się komunikat błędu. “Nazwa” i “Hasło” mogą się powtarzać wśród pozostałych Użytkowników.

 b) Logowanie
Pierwsza strona uruchomienia aplikacji. Wymaga wpisania pól: Nazwa Użytkownika, Hasło. Poprawne logowanie przenosi do Profilu Użytkownika, daje dostęp do danych podanych w formularzu i do wyników analizy.

 3. Profil Użytkownika
Pola widoczne na Profilu Użytkownika:

 a) Nazwa Użytkownika
W widocznym miejscu np na górze strony

b) Tablica
Z proponowanymi wynikami analizy

c) Zakładki:
- Formularz początkowy - obowiązkowy (Informacje podstawowe) do wypełnienia przez Użytkownika, bez danych w tej tabeli analiza nie jest możliwa. Formularz musi zostać wypełniony w całości. Wiek, waga oraz wzrost muszą być liczbowe. Formularz pamięta wybór i umożliwia edycję oraz usunięcie danych. Nowe wprowadzone dane są widoczne po odświeżeniu strony np. przyskiem "Odśwież". Przycisk "Analiza" wprowdza dane do tabel: Szczepienia, Badania kontrolne, Profilaktyka
- Szczepienia, Proilaktyka, Badania kontrolne: zawierają tabele, gdzie można odhaczyć wynik jak zadanie lub zdjąć je ze strony głównej.
