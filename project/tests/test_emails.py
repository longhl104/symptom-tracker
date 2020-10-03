import unittest
from email_handler import email_handler

class EmailTests(unittest.TestCase):
    def test_email_setup(self):
        message = email_handler.setup_email("test@address.com")
        self.assertEqual(message['recipient'],"test@address.com")
        self.assertEqual(message['sender'],"brainandmindcentre.usyd@gmail.com")
