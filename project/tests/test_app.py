import unittest
from app import app
from unittest import mock
from flask import url_for, request


class AppTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    
    #! test methods' name must start with "test_"
    def test_void(self):
        pass

    @mock.patch('database.check_login')
    def test_login_no_data(self, db):
        # db.return_value = [{'ac_id': 12, 'ac_email': 'long', 'ac_password': '12345678', 'ac_firstname': 'Long',
        #                     'ac_lastname': 'Nguyen', 'ac_age': 22, 'ac_gender': 'male', 'ac_phone': '0415123456'}]
        with app.test_client() as client:
            db.return_value = None
            response = client.post('/', data=dict(
                email='long',
                password='12345678'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/patient/')
        pass

    @mock.patch('database.check_login')
    def test_login_has_data(self, db):
        with app.test_client() as client:
            db.return_value = [{'ac_id': 12, 'ac_email': 'long', 'ac_password': '12345678', 'ac_firstname': 'Long',                    'ac_lastname': 'Nguyen', 'ac_age': 22, 'ac_gender': 'male', 'ac_phone': '0415123456'}]
            response = client.post('/', data=dict(
                email='long',
                password='12345678'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/patient/')
        pass

if __name__ == '__main__':
    unittest.main()
