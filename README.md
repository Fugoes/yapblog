# yapb

`yapb` is acronym for `yet another personal blog`.

# Requirement

Please install `python3`, `flask`, `flask_sqlalchemy`.

# Project Structure

+ `yapb/models`
  Data models for interact with database using `flask_sqlalchemy`.
+ `yapb/views`
  Available views.
  + `/api/user` is the api for user related operations.

# A example

First, run `python3 manage.py create-database` to init the database. Then run `python3 run.py` to start the server. Open another terminal, run `python3 -m tests.test_api_user`, this will insert a user into the database. Now, browse `http://localhost:8080/test/show_users`, this will show all users and this page is rendered on the server side. Browse `http://locahost:8080/test/show_users_with_api`, this will show all users using ajax and `/api/user`.
