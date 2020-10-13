import unittest
from unittest import mock
from unittest.mock import mock_open
import database
import sys
from contextlib import contextmanager
from io import BytesIO, StringIO, TextIOWrapper
import pg8000


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('pg8000.connect')
    def test_database_connection_no_error(self, conn):
        conn.return_value = True
        self.assertEqual(database.database_connect(), True)
    pass

    @mock.patch('pg8000.connect')
    def test_database_connection_operational_error(self, conn):
        with captured_output() as (out, err):
            conn.side_effect = pg8000.OperationalError
            self.assertTrue(database.database_connect() is None)
        pass

    def test_print_sql_string_with_params(self):
        with captured_output() as (out, err):
            query = "SELECT * FROM tingleserver.\"Treatment\" WHERE %s='long'"
            database.print_sql_string(query, ('name'))

            # This can go inside or outside the `with` block
            output = out.getvalue().strip()
            self.assertEqual(
                output, "SELECT * FROM tingleserver.\"Treatment\" WHERE 'name'='long'")
        pass

    def test_check_login(self):

        pass


if __name__ == '__main__':
    unittest.main()
