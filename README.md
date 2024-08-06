# BREW CONTROL APP

#### With module designed for sendind a file, checking chart from exact month, year & etc.

## FrontEnd Django App

1. #### MainAppScreen

![2](https://github.com/user-attachments/assets/594dad30-f1e9-45a3-af76-d4e71b757020)

## In that part of app, you can easily check thing's related with your already sent CSV file's with all data from for example, last 6 months. The chart generated after uploading file's with month data is adjusted to spot months in overall calendar year & also to check more detailed info related with month

2. #### DevicesAppScreen

3. #### 


## RestApi Application

### endpoints

#### it is available for a admin, but it also with crediential - allow another user, to do some file operation, with endpoint's below:

- /my-data/?format=json - you can send your file by using that, with POST METHOD :method POST/GET

- /my-data/number_doc/?format=json - that is designed for viewing a single file sended by someone :method GET

- /my-files/?format=json - you can add record to your sqlite db

- /my-files/number_doc/?format=json - that is for viewing a single record sended by someone :method GET

- /users/?format=json - it is for seeing users to apply them to some kind device