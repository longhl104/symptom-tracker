import unittest
from app import app


class BasicTestCase(unittest.TestCase):
    #! test methods' name must start with "test_"
    def tearDown(self):
        pass


    def test_forgot_password(self):
        tester = app.test_client(self)
        response = tester.get('/forgot-password', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_register_extra(self):
        tester = app.test_client(self)
        response = tester.get('/register-extra', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    def test_patient_dashboard_without_being_logged_in(self):
        tester = app.test_client(self)
        response = tester.get('/patient/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_patient_record_symptom_without_being_logged_in(self):
        tester = app.test_client(self)
        response = tester.get('/patient/record-symptom', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_patient_reports(self):
        tester = app.test_client(self)
        response = tester.get('/patient/reports', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_patient_account(self):
        tester = app.test_client(self)
        response = tester.get('/patient/account', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_service_worker_js(self):
        tester = app.test_client(self)
        response = tester.get('/service-worker.js', content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
