echo 'Running test cases...'
coverage run -m nose2 -s local_tests
echo 'Generating test coverage report...'
coverage report -m
sleep infinity