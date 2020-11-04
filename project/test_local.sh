echo 'Running test cases...'
coverage run -m nose2 -s local_tests
# coverage run -m nose2 -s local_tests test_database
# coverage run -m nose2 -s local_tests test_email_handler
echo 'Generating test coverage report...'
coverage report -m
sleep infinity