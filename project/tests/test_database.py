import unittest
import testing.postgresql
from app import app
import database


class DatabaseTest(unittest.TestCase):
    #! test methods' name must start with "test_"
    def setUp(self):
        self.postgresql = testing.postgresql.Postgresql()

    def tearDown(self):
        self.postgresql.stop()


if __name__ == '__main__':
    unittest.main()
