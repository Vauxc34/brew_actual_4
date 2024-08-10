# BREW CONTROL APP

#### Z modułem dostosowanym odpowiednio pod przesył plików CSV, które zostały by wykorzystane dla generowanych wykresów.

## Gdzie znajduje się folder od plików CSV w aplikacji?

### W plikach samej aplikacji, pod nazwa energy_reports 
### i jest on domyślnie ustawiony jako przysłowiowy
### agregator plików CSV 

## FrontEnd Django App

## Gdzie znajduje się aplikacja Django główna?

### W folderze testapp, gdzie dostępne sa wszystkie inne odnośniki do podstron

1. #### Główny ekran aplikacji

![2](https://github.com/user-attachments/assets/594dad30-f1e9-45a3-af76-d4e71b757020)
![Screenshot 2024-07-02 175026](https://github.com/user-attachments/assets/113d721e-b3b9-4a0a-86a5-5e322d1f6bef)
![Screenshot 2024-07-11 134952](https://github.com/user-attachments/assets/57f8b3db-aafa-4801-9bb2-dabd4228ccd4)

## W tej części aplikacji z łatwościa sprawdzisz przesłany plik CSV z danymi pod względem generowanego wykresu po przesłaniu pliku. Generowany wykres możesz potem podejrzeć patrzac całościowo na jeden miesiac, albo poprzez wybór dnia we wskazanym miesiacu w selektorze obok przycisku "Wyślij"

2. #### Ekran urzadzeń aplikacji 

![3](https://github.com/user-attachments/assets/b7f5ad81-2df2-4c4d-8096-e98353353451)

## Możliwe jest także dodanie urządzenia z dodatkowymi parametrami internetowymi. 

## Odnośniki od podstron

### https://localhost:????/devices - lista wszystkich urzadzeń aplikacji

### https://localhost:????/devices/?id-urzadzenia/update - Po kliknięciu w nazwę urzadzenia, z listy wyświetlanej z wcześniej podanego linku - Zobaczysz pod wskazanym adresem formularz do zmiany parametrów urzadzenia

### https://localhost:????/devices/?id-urzadzenia/delete - Kliknięcie w link, o podtytule "delete" jednoznacznie powoduje usunięcie urzadzenia z listy

3. #### Ekran zmiennych aplikacji

![4](https://github.com/user-attachments/assets/d66fd51e-674e-47e0-9f49-15aa19b7173a)

## Do wybranego urzadzenia jesteś w stanie dopisać specjalna zmienna

# Odnośniki od podstron

### https://localhost:????/variables - lista wszystkich zmiennych dla urzadzeń w aplikacji

### https://localhost:????/variables/?id-zmiennej/update - Po kliknięciu w nazwę zmiennej, z listy wyświetlanej z wcześniej podanego linku - Zobaczysz pod wskazanym adresem formularz do zmiany parametrów zmiennej

### https://localhost:????/variables/?id-zmiennej/delete - Kliknięcie w link, o podtytule "delete" jednoznacznie powoduje usunięcie zmiennej z tabeli

## Możesz dodać dodatkowe zmienne, które możesz przypisać do już dodanych urządzeń przez inną osobę lub administratora aplikacji

## Aplikacja Rest API (przykładowo dla spięcia front endu aplikacji z inna dostępna na frameworku ReactJs np.)

### endpointy

## Gdzie znajduje się aplikacja REST?

### W folderze testproject, gdzie dostępne sa wszystkie inne odnośniki do podstron REST, a niektóre z nich sa wymienione poniżej:

#### jest dostępny dla administratora, ale także z poświadczeniami - pozwól innemu użytkownikowi wykonać pewne operacje na plikach, z poniższymi punktami końcowymi:

-  https://localhost:????/new-app/my-data/?format=json - możesz wysłać swój plik za pomocą tego, używając POST METHOD:method POST/GET

-  https://localhost:????/new-app/my-data/number_doc/?format=json - przeznaczony do przeglądania pojedynczego pliku przesłanego przez kogoś:method GET

-  https://localhost:????/new-app/my-files/?format=json - możesz dodać rekord do swojej bazy danych sqlite

-  https://localhost:????/new-app/my-files/number_doc/?format=json - to jest do przeglądania pojedynczego rekordu wysłanego przez kogoś :method GET

-  https://localhost:????/new-app/users/?format=json - chodzi o to, aby zobaczyć, jak użytkownicy stosują je na jakimś urządzeniu

## Jak zainstalować aplikacje?

#### Najpierw powinieneś aktywować wirtualne środowisko wpisując polecenie:

### source venv/bin/activate

#### Następnie będziesz mógł uruchomić polecenia związane z poniższą kolejnością:

### 1. python3 manage.py makemigrations

### 2. python3 manage.py migrate

### 3. python3 manage.py runserver

#### Następnie pomyślnie zobaczysz aplikację uruchomioną na porcie 8000 - pod adresem w Twojej przeglądarce internetowej: http://localhost:8000