# Instrukcja Użytkowania

1. Pracę rozpoczynamy od sekcji "Reading maps files" po lewej stronie. Dodajemy kolejno mapy przyciskiem "Add".
2. Wciskamy **Read whole maps**, by wczytać mapy. Będzie trwać, a program nie będzie reagować, jak OMSI podczas ładowania.
3. Gdy program powróci do żywych, dowiemy się, w jakim stopniu udało się załadować mapy. Jeśli w tabelce wszystkie mają w kolumnie **Ready** wartość **True**, to możemy przejść do następnego punktu. W przeciwnym razie, możemy rozwinąć trójkątem po lewej stronie drzewo ze strukturą wczytywanej mapy i zobaczyć, w czym leży problem.
   - Każdy element w drzewie reprezentuje obiekt jednego z następujących typów:
     - **unit** - jeden plik z mapy OMSI
     - **list** - grupa **list** lub/i **unitów**
   - Po wybraniu elementu, pod drzewem wyświetlą się szczegółowe informacje o błędzie (jeśli był).
   - Dla każdego elementu można użyć opcji **Load selected**, by ponowić wczytywanie (np. po poprawieniu pliku).
   - Dla elementów typu **unit** można użyć opcji **Open file in editor**, która otworzy ten plik w naszym domyślnym edytorze.
   - Dla elementów typu **OmsiMap**, jeśli global.cfg jest wczytany, można użyć opcji **Scan for chronos**, która wyszuka katalogi chrono.
   - Dla elementów typu **Timetable** można użyć opcji **Scan for lines**, **Scan for tracks**, **Scan for trips**, które wyszukają pliki odpowiednio ttl, ttr, ttp w danym rozkładzie.
4. Po zaznaczeniu mapy (nie jej podrzędnych elementów) w tabelce mamy możliwość przesuwania jej na diagramie. Ustawiamy mapy tak, jak chcemy.
5. Po zaznaczeniu mapy w tabelce jak w punkcie powyżej, uaktywnia się przycisk **(toggle) Keep original main ground texture on tiles of selected map**. Możemy nim włączyć pokrycie całego obszaru danej mapy dodatkową teksturą groundtex taką, jak ma ta mapa przed łączeniem, by wizualnie zachowała inną teksturę podłoża także po łączeniu. Włączenie tej opcji jest zaznaczone na diagramie poprzez X na kaflach danej mapy.
6. Wybieramy katalog, gdzie ma być zapisana połączona mapa.
7. Wpisujemy nazwę nowej mapy (wyświetli się przy wyborze mapy w OMSI).
8. Naciskamy **Merge maps!**
9. Jeśli są ostrzeżenia, to zostaniemy o nich poinformowani i będziemy mogli zrezygnować z zapisu mapy. Jeśli tego nie zrobimy, mapa zostanie zapisana.
10. Jest możliwość ponownego wczytania mapy lub jej części, przesunięcia itp., a następnie ponownego zapisu mapy.
