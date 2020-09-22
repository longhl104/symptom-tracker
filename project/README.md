# Tingle PWA

#### Make sure you have Python version 3.3+ installed.

#### You can check the version by running the following command:

`python --version`

#### Make sure you are in the `project` folder in your terminal.

#### Install the requirements

`pip install -r requirements.txt`

#### Add a config file
Create a copy of the sample-config.ini file and rename it to config.ini.
Fill it with the correct parameters.

#### Run this command once
`chmod +x run.sh`

OR

`chmod +x run-windows.sh` (if you're on Windows)

#### To run the app

`./run.sh`

OR

`./run-windows.sh` (if you're on Windows)

#### Check the terminal for the address of the app. It usually runs on http://127.0.0.1:5000/.
#### Whenever you make a change to a file, refreshing that file in the browser should get the latest version

#### To run all of the unit tests (the test files start with "test\_\*.py")

`nose2`

#### To check code coverage of the unit tests

`coverage run -m nose2`
`coverage report -m`
