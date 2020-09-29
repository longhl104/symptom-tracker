import unittest
from app import app
import database


class DatabaseTest(unittest.TestCase):
    #! test methods' name must start with "test_"
    def test_database_connect_simple_connection(self):
        conn = database.database_connect();
        self.assertIsNotNone(conn);

    def test_database_connect_database_is_not_presented(self):
        f = open('sample-config.ini', 'r')
        back_up = f.read()
        f.close()

        content = """[DATABASE]
host = 127.0.0.1
user = postgres
password = tingle12345
secret_key = /TMVe0"Lw`hc*0I"""

        f = open('sample-config.ini', 'w')
        f.write(content)
        f.close()

        conn = database.database_connect()
        self.assertIsNotNone(conn)

        f = open('sample-config.ini', 'w')
        f.write(back_up)
        f.close()


if __name__ == '__main__':
    unittest.main()
