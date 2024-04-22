# BREW CONTROL APP


## With module designed for sendind a file 

### endpoints

#### currently it is available for a admin, but it also with crediential - allow another user, to do some file operation, with endpoint's below:

- /my-data/?format=json - you can send your file by using that, with POST METHOD :method POST/GET

- /my-data/number_doc/?format=json - that is designed for viewing a single file sended by someone :method GET

- /my-files/?format=json - you can add record to your sqlite db

- /my-files/number_doc/?format=json - that is for viewing a single record sended by someone :method GET

- /users/?format=json - it is for seeing users to apply them to some kind device