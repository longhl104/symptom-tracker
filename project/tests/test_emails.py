import unittest
import email_handler

class EmailTests(unittest.TestCase):
    def test_email_setup(self):
        message = email_handler.setup_email("test@address.com", "key123")
        self.assertEqual(message['To'],"test@address.com")
        self.assertEqual(message['From'],"brainandmindcentre.usyd@gmail.com")
        self.assertEqual(message['Subject'],"Reset your password")
