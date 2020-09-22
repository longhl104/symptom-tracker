import unittest
from app import app


class BasicTestCase(unittest.TestCase):
    #! test methods' name must start with "test_"
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_service_worker_js(self):
        tester = app.test_client(self)
        response = tester.get('/service-worker.js', content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
