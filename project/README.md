# Tingle PWA

Make sure you have **Python version 3.3+** installed.

You can check the version by running the following command:

`python --version`

Make sure you are in the `project` folder in your terminal.

## Install the requirements

`pip install -r requirements.txt`

## Run this command once

`chmod +x run.sh`

OR

`chmod +x run-windows.sh` (if you're on Windows)

## To run the app

`./run.sh`

OR

`./run-windows.sh` (if you're on Windows)

Check the terminal for the address of the app. It usually runs on <http://127.0.0.1:5000/>.
Whenever you make a change to a file, refreshing that file in the browser should get the latest version

## Testing

To run all of the unit tests (the test files start with "test\_\*.py")

`nose2`

To check code coverage of the unit tests

`coverage run -m nose2`
`coverage report -m`

## Pgadmin and Postgresql set up

- You need to download the latest version of PgAdmin <https://www.pgadmin.org/download/>

- We should use the same username and password for pgadmin server for synchronization

  - host: 127.0.0.1
  - username: postgres
  - database name: postgres
  - password = tingle12345

- Click "Query Tool" in "Tools" tab. Copy the code in the [backup sql file](project\database\backup_schema.sql) and paste it into the query tool editor. Then click run. Now the schema "tingleserver" has been created.
