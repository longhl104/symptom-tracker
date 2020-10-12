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
    @mock.patch('database.get_all_treatments')
    def test_register_get_method_not_logged_in_none_treatments(self, db):
        with tingle.test_client() as client:
            db.return_value = None
            response = client.get('/register', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/register')
        pass

    def test_patient_dashboard_logged_in(self):
        with tingle.test_client() as client:
            response = client.get('/patient', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/patient/')
        pass

    @mock.patch('app.session', {'logged_in': False})
    def test_patient_dashboard_not_logged_in(self):
        with tingle.test_client() as client:
            response = client.get('/patient/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/')
        pass

    @mock.patch('app.session', {'logged_in': False})
    def test_record_symptom_not_logged_in(self):
        with tingle.test_client() as client:
            response = client.get(
                '/patient/record-symptom', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/')
        pass

    @mock.patch('database.record_symptom')
    def test_record_symptom_logged_in_other_symptom_other_activity_none_record(self, db):
        with tingle.test_client() as client:
            db.return_value = None
            response = client.post('/patient/record-symptom',
                                   data={
                                       'symptom': ['Other', 'Itchy'],
                                       'activity': ['Other', 'Coding'],
                                       'severity': ['Bad'],
                                       'date': ['13/10/2020'],
                                       'time': ['12:55 AM'],
                                       'notes': ['Note']
                                   },
                                   follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/patient/record-symptom')
        pass

    @mock.patch('database.record_symptom')
    def test_record_symptom_logged_in_other_symptom_other_activity_not_none_record(self, db):
        with tingle.test_client() as client:
            db.return_value = True
            response = client.post('/patient/record-symptom',
                                   data={
                                       'symptom': ['Other', 'Itchy'],
                                       'activity': ['Other', 'Coding'],
                                       'severity': ['Bad'],
                                       'date': ['13/10/2020'],
                                       'time': ['12:55 AM'],
                                       'notes': ['Note']
                                   },
                                   follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/patient/')
        pass

    @mock.patch('app.user_details', {'ac_email': None})
    def test_symptom_history_none_email(self):
        with tingle.test_client() as client:
            response = client.get(
                '/patient/symptom-history', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/patient/')
        pass

    @mock.patch('app.user_details', {'ac_email': 'foo@bar.com'})
    @mock.patch('database.get_all_symptoms')
    def test_symptom_history_not_none_email(self, db):
        with tingle.test_client() as client:
            db.return_value = [
                {
                    'row': 'abc,def,cab,fea,aij'
                }
            ]
            response = client.get(
                '/patient/symptom-history', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/patient/symptom-history')
        pass


if __name__ == '__main__':
    unittest.main()
