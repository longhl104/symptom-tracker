import unittest
from app import app


class AppTest(unittest.TestCase):
    #! test methods' name must start with "test_"
    def test_void(self):
        pass


if __name__ == '__main__':
    unittest.main()

@mock.patch('')