echo 'Running test cases...'
coverage run -m nose2
echo 'Generating test coverage report...'
coverage report -m
sleep infinity