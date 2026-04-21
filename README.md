Changelog - DEX Tracker

Wszystkie istotne zmiany w projekcie DEX Tracker są dokumentowane w tym pliku.

[1.1.0] - 2026-04-21
Added
Weryfikacja backlogu: Wprowadzono możliwość wygenerowania raportu Backlog, który zawiera przesyłki niedostarczone oraz niezwrócone zgodnie ze standardami danego przewoźnika.
Eksport „Ostatni status / Cała historia”: Dodano możliwość wyboru trybu raportu generowanego przez użytkownika. Aplikacja umożliwia wygenerowanie raportu z pełną historią paczki lub wyłącznie z jej ostatnim statusem.
Fixed
Stabilność UI: Naprawiono błąd powodujący migotanie głównego okna aplikacji podczas przełączania zakładek przewoźników.
Obsługa błędów: Poprawiono logikę obsługi błędów w module Poczty Polskiej w przypadku braku odpowiedzi serwera.
Optymalizacja „STOP”: Całkowicie przebudowano mechanizm przerywania weryfikacji. Przycisk „STOP” poprawnie reaguje, bezpiecznie kończąc aktywne sesje przeglądarki. Aplikacja umożliwia wygenerowanie raportu na podstawie paczek sprawdzonych przed zatrzymaniem procesu.
[1.0.0] - 2026-03-01
Added
Pierwsza stabilna wersja .exe (standalone).
Obsługa przewoźników: InPost, DPD, Poczta Polska, Orlen Paczka.
System poziomów dostępu: BASIC oraz PRO (multi-threading).
Automatyczne zarządzanie sterownikami przeglądarki Chrome.
Eksport danych do formatu .xlsx.
