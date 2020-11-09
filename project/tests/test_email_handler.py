import unittest
from project import email_handler
from unittest import mock
from email.mime.text import MIMEText


class AppTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('project.email_handler.MIMEText')
    def test_setup_email(self, mime):
        mime.return_value = {}
        self.assertEqual({
            'Subject': 'Reset your password',
            'From': 'example@example.com',
            'To': 'toemail'
        }, email_handler.setup_email('toemail', 'key'))
        pass

    @mock.patch('project.email_handler.MIMEText')
    def test_setup_invitation(self, mime):
        mime.return_value = {}
        self.assertEqual({
            'Subject': 'Symptom Tracker Invitation',
            'From': 'example@example.com',
            'To': 'toemail'
        }, email_handler.setup_invitation('admin', 'toemail', 'key'))
        pass

    @mock.patch('smtplib.SMTP.sendmail')
    @mock.patch('smtplib.SMTP.login')
    @mock.patch('ssl.create_default_context')
    def test_send_email(self, cdc, sl, ss):
        cdc.return_value = None
        sl.return_value = None
        ss.return_value = None
        message = MIMEText('text', "plain")
        message["Subject"] = "Symptom Tracker Invitation"
        message["From"] = 'fromemail'
        message["To"] = 'toemail'
        email_handler.send_email(message)
        pass


if __name__ == '__main__':
    unittest.main()
