import unittest
from app import app as tingle
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

    # add mock patch to the function you want to mock
    @mock.patch('database.check_login')
    def test_login_no_data(self, db):
        # db.return_value = [{'ac_id': 12, 'ac_email': 'long', 'ac_password': '12345678', 'ac_firstname': 'Long',
        #                     'ac_lastname': 'Nguyen', 'ac_age': 22, 'ac_gender': 'male', 'ac_phone': '0415123456'}]
        with tingle.test_client() as client:
            # set the return value
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
        with tingle.test_client() as client:
            db.return_value = [{'ac_id': 12, 'ac_email': 'long', 'ac_password': '12345678', 'ac_firstname': 'Long',
                                'ac_lastname': 'Nguyen', 'ac_age': 22, 'ac_gender': 'male', 'ac_phone': '0415123456'}]
            response = client.post('/', data=dict(
                email='long',
                password='12345678'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/patient/')
        pass

    def test_login_get_method(self):
        with tingle.test_client() as client:
            response = client.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/')
        pass

    @mock.patch('database.add_patient')
    def test_register_post_method_failed(self, db):
        with tingle.test_client() as client:
            db.return_value = None
            response = client.post('/register', data={
                'first-name': 'foo',
                'last-name': 'bar',
                'gender': 'Male',
                'age': '12',
                'mobile-number': '04123456789',
                'treatment': 'A',
                'email-address': 'foo@bar.com',
                'password': '12345678',
                'consent': 'yes'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/patient/')
        pass

    @mock.patch('database.add_patient')
    def test_register_post_method_successful(self, db):
        with tingle.test_client() as client:
            db.return_value = 1
            response = client.post('/register', data={
                'first-name': 'foo',
                'last-name': 'bar',
                'gender': 'Male',
                'age': '12',
                'mobile-number': '04123456789',
                'treatment': 'A',
                'email-address': 'foo@bar.com',
                'password': '12345678',
                'consent': 'yes'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('patient_dashboard'))
        pass

    @mock.patch('database.add_patient')
    def test_register_post_method_exception(self, db):
        with tingle.test_client() as client:
            db.side_effect = Exception('Database error')
            response = client.post('/register', data={
                'first-name': 'foo',
                'last-name': 'bar',
                'gender': 'Male',
                'age': '12',
                'mobile-number': '04123456789',
                'treatment': 'A',
                'email-address': 'foo@bar.com',
                'password': '12345678',
                'consent': 'yes'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/patient/')
        pass

    def test_register_get_method_logged_in(self):
        with tingle.test_client() as client:
            response = client.get('/register', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/patient/')
        pass

    @mock.patch('app.session', {'logged_in': False})
    def test_register_get_method_not_logged_in(self):
        with tingle.test_client() as client:
            response = client.get('/register', follow_redirects=True)
            # self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/register')
        pass

    def test_patient_dashboard(self):
        with tingle.test_client() as client:
            response = client.get('/patient', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/patient/')
        pass


if __name__ == '__main__':
    unittest.main()
