# Tingle PWA

Make sure you have **Python version 3.3+** installed.

You can check the version by running the following command:

`python --version`

Make sure you are in the `project` folder in your terminal.

## Install the requirements

`pip install -r requirements.txt`

## Add a config file

Create a copy of the sample-config.ini file and rename it to config.ini.
Fill it with the correct parameters.

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

- We should use the same username and password for pgadmin server for synchronization (below is just an example, you need to set up your own `config.ini`)

  - host: 127.0.0.1
  - username: postgres
  - database name: postgres
  - password = tingle12345
  - secret_key = abcdefghijklmnopqrst

- Click "Query Tool" in "Tools" tab. Copy the code in the [backup sql file](project\database\backup_schema.sql) and paste it into the query tool editor. Then click run. Now the schema "tingleserver" has been created.

## Alert messages

### For front-end

Copy this chunk of code into where you want to the alert message to show up.

```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
      {% for category, message in messages %}
        <div class="alert" role="alert">
          <span class="{{ category }}-message">{{ message }}</span>
        </div>
      {% endfor %}
  {% endif %}
{% endwith %}
```

You can change CSS code and add more message styles in [base.css](project\static\css\base.css).

I added `warning-message` for example:

```CSS
.error-message {
  text-align: center;
  color: #FF4141;
}

.warning-message {
  text-align: center;
  color: #ffcc00;
}
```

### For back-end

Use function `flash` with this format `flash('_error_message_', "_category_")`

```Python
flash('Incorrect email/password, please try again', "error")
```

`category` can be seen in CSS above, for example, `error`, `warning`, etc.