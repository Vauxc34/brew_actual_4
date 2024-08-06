# BREW CONTROL APP

#### With module designed for sendind a file, checking chart from exact month, year & etc.

## FrontEnd Django App

1. #### MainAppScreen

![2](https://github.com/user-attachments/assets/594dad30-f1e9-45a3-af76-d4e71b757020)
![Screenshot 2024-07-02 175026](https://github.com/user-attachments/assets/113d721e-b3b9-4a0a-86a5-5e322d1f6bef)
![Screenshot 2024-07-11 134952](https://github.com/user-attachments/assets/57f8b3db-aafa-4801-9bb2-dabd4228ccd4)

## In that part of app, you can easily check thing's related with your already sent CSV file's with all data from for example, last 6 months. The chart generated after uploading file's with month data is adjusted to spot months in overall calendar year & also to check more detailed info related with month

2. #### DevicesAppScreen

![3](https://github.com/user-attachments/assets/b7f5ad81-2df2-4c4d-8096-e98353353451)

## It is also possible, to add some device with additional advanced internet parameter's

3. #### VariablesAppScreen

![4](https://github.com/user-attachments/assets/d66fd51e-674e-47e0-9f49-15aa19b7173a)

## You can add additional variables, that you can assign to already added device's by someone or maybe administrator of app

## RestApi Application

### endpoints

#### it is available for a admin, but it also with crediential - allow another user, to do some file operation, with endpoint's below:

- /my-data/?format=json - you can send your file by using that, with POST METHOD :method POST/GET

- /my-data/number_doc/?format=json - that is designed for viewing a single file sended by someone :method GET

- /my-files/?format=json - you can add record to your sqlite db

- /my-files/number_doc/?format=json - that is for viewing a single record sended by someone :method GET

- /users/?format=json - it is for seeing users to apply them to some kind device

## How to install it?

#### At first you should activate virtual env by typing command:

### source venv/bin/activate

#### Then you will be able to run commands related with order below :

### 1. python3 manage.py makemigrations

### 2. python3 manage.py migrate

### 3. python3 manage.py runserver

#### After that you will succesfully see, a app launched in a port 8000 - on address in your web browser: http://localhost:8000