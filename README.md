# Med-Assist
IO school project
Projekt: Med-Assist
Dokumentacja

Wprowadzenie
Aplikacja webowa, która analizuje podane informacje, na podstawie których proponuje Użytkownikowi wykonanie szczepień, badań profilaktycznych oraz badań okresowych.

Propozycje badań, przypomnienia badań dalej w instrukcji są nazwane “wynikami” ze względu na to, że zależą od wyników analizy danych w bazie.

 1. Szczegóły techniczne
Technologia: język python3 z frameworkiem Flask z dodatkowymi paczkami
Dodatkowe narzędzia: docker i docker compose (opcjonalnie), html i css (budowa stony)
Baza danych: MySQL
Hosting: local hosting, darmowy hosting online

 2. Konta
Założenie konta zapewnia dostęp do aplikacji, dane osobowe poza adresem mailowym nie muszą być autentyczne, służą jedynie identyfikacji Użytkownika celem powiązania go z informacjami w formularzach, ich anallizy oraz wyświetlenia wyniku analizy (propozycji szczepień lub badań). Prawdziwe pozostają dane podane w formularzarz oraz adres e-mail.

 a) Rejestracja
Zawiera pola do wypełnienia: Nazwa, E-mail, Nazwa Użytkownika, Hasło. Jeśli Nazwa Użytkownika lub E-mail istnieją już w bazie, pojawi się komunikat błędu. “Nazwa” i “Hasło” mogą się powtarzać wśród pozostałych Użytkowników.
- Wszystkie dane znajdują się w bazie ‘projekt’ tabela ‘accounts’.
- W bazie niepowtarzające się pola UNIQUE + sprawdzanie if’em w programie

 b) Logowanie
Pierwsza strona uruchomienia aplikacji. Wymaga wpisania pól: Nazwa Użytkownika, Hasło. Poprawne logowanie przenosi do Profilu Użytkownika, daje dostęp do danych podanych w formularzach I do wyników analizy.

 c) Błędy logowania I rejestracji
Nie ma możliwości podania powtarzającej się nazwy użytkownika lub adresu e-mail.

 3. Profil Użytkownika
Pola widoczne na Profilu Użytkownika:

 a) Nazwa Użytkownika
W widocznym miejscu np na górze strony, avatar (opcjonalnie)

 b) Ustawienia
Zmiana pól: Nazwa użytkownika, Hasło, Adres e-mail, Nazwa.
(opcjonalne) Ustawienie avatara/obrazka

 c) Formularz początkowy - obowiązkowy (Informacje podstawowe)
Moze mieć inny kolor (np. czerwony, gdy nie jest uzupełniony, również pole z wynikami może ieć komunikat, że należy go wypełnić aby cokolwiek się pojawiło na ekranie z wyników).

Dane z tego formularza zapisane zostaną w tabeli ‘basics’ baza ‘projekt’. Mają wpływ na wygląd pozostałych formularzy.
Pola do wypełnienia: wiek, waga, wzrost, aktywność fizyczna (wysoka, średnia, niska), papierosy (tak, nie), alkohol (w ramach czasowych jak często lub nie), płeć, pole BMI jest obliczane automatycznie.

Odpowiedzi do każdego z formularzy są zapisane w bazie, mogą być wyświetlone z Profilu Użytkownika oraz mogą być zmienione, co wpływa na wyniki wyświetlane na Profilu.

Wyróżniamy 3 rodzaje formularzy opcojnalnych, które pozwalają na precyzyjniejszą analizę:

- Szczepienia ochronne
Obowiązkowe, rekomendowane, nieobowiązkowe.
Pytania zawierają jedynie informacje o wykonanych szczepieniach, można odpowiedzieć “Tak”, “Nie”, “Nie wiem”.
Pytania zależą np od wieku, płci.

- Badania okresowe
Kontrolne badania okresowe, wykonywane regularnie. Checkboxy: można zaznaczyć zainteresowanie danymi badaniami, żeby wyświetlały się one w wynikach.
Pytania zależą np od wieku, płci, aktywności fizycznej, używek (papierosy, alkohol), BMI.

- Badania profilaktyczne
Oferowane programy profilaktyczne przez Ministerstwo Zdrowia.
Użytkownik zaznacza tylko czy chce mieć wyświetlane informacje o dostępnych badaniach profilaktycznych (“Tak”, “Nie”), do wyników z tej kategorii można dodać odnośniki do stron gov.pl  z ofertą MZ.
Pytania zależą np od wieku, płci, aktywności fizycznej, używek (papierosy, alkohol), BMI.

 4. Wyniki (kryteria wyświetlania wyników)
Muszą być określone indywidualnie dla każdego wyniku.
Planowo dodajemy po 5: 
- szczepień, 
- badań okresowych,
- badań profilaktycznych.
