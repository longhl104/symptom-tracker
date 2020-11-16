import unittest
from unittest.mock import Mock
from ..app import app as tingle
from unittest import mock
from flask import url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
import pg8000

class AppTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    #! test methods' name must start with "test_"

    def test_void(self):
        pass

#     # add mock patch to the function you want to mock
    @mock.patch('project.app.check_password_hash')
    @mock.patch('project.database.get_account')
    def test_login_post(self, db, cph):
        with tingle.test_client() as client:
            db.return_value = None
            response = client.post('/', data=dict(
                email='long',
                password='12345678'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))

            db.return_value = [{
                'ac_id': 12, 'ac_email': 'long', 'ac_password': '12345678', 'ac_firstname': 'Long',
                'ac_lastname': 'Nguyen', 'ac_age': 22, 'ac_gender': 'male', 'ac_phone': '0415123456',
                'ac_type': 'clinician',
            }]
            cph.return_value = False
            response = client.post('/', data=dict(
                email='long',
                password='12345678'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))

            cph.return_value = True
            response = client.post('/', data=dict(
                email='long',
                password='12345678'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('clinician_dashboard'))

            db.return_value = [{
                'ac_id': 12, 'ac_email': 'long', 'ac_password': '12345678', 'ac_firstname': 'Long',
                'ac_lastname': 'Nguyen', 'ac_age': 22, 'ac_gender': 'male', 'ac_phone': '0415123456',
                'ac_type': 'unknown'
            }]
            cph.return_value = True
            self.assertRaises(Exception, client.post('/', data=dict(
                email='long',
                password='12345678'
            ), follow_redirects=True))
        pass

    # @mock.patch('project.app.session', {'logged_in': True})
    def test_login_get_method(self):
        with tingle.test_client() as client:
            response = client.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))
        pass

    @mock.patch('project.app.user_details', {
        'ac_id': 12, 'ac_email': 'long', 'ac_password': '12345678', 'ac_firstname': 'Long',
        'ac_lastname': 'Nguyen', 'ac_age': 22, 'ac_gender': 'male', 'ac_phone': '0415123456',
        'ac_type': 'patient',
    })
    @mock.patch('project.app.session', {'logged_in': True})
    def test_login_get_method_logged_in(self):
        with tingle.test_client() as client:
            response = client.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('patient_dashboard'))
        pass

    def test_logout(self):
        with tingle.test_client() as client:
            response = client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))
        pass

    @mock.patch('project.database.check_invitation_token_validity')
    @mock.patch('project.database.delete_account_invitation')
    @mock.patch('project.database.get_account')
    @mock.patch('project.database.add_patient')
    def test_register_post_no_token(self, db, ga, dai, citv):
        with tingle.test_client() as client:
            response = client.post('/register', data={
                'password': '12345678',
                'confirm-password': '123'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('register'))

            db.return_value = None
            response = client.post('/register', data={
                'password': '12345678',
                'confirm-password': '12345678',
                'age': '',
                'mobile-number': ''
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('register'))

            db.return_value = True
            ga.return_value = [{
                'ac_type': 'patient',
                'ac_firstname': 'Long'
            }]
            response = client.post('/register', data={
                'password': '12345678',
                'confirm-password': '12345678',
                'age': '',
                'mobile-number': '',
                'email-address': 'long@gmail.com'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('patient_dashboard'))

            ga.return_value = [{
                'ac_type': 'patient',
                'ac_firstname': 'Long'
            }]
            dai.return_value = 0
            db.return_value = True
            citv.return_value = [{'ac_email': 'long@gmail.com'}]
            response = client.post('/register/0', data={
                'email-address': 'long@gmail.com',
                'password': '12345678',
                'confirm-password': '12345678'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('patient_dashboard'))
        pass

    @mock.patch('project.app.session', {'logged_in': False})
    def test_register_post_no_token_exception(self):
        with tingle.test_client() as client:
            response = client.post('/register', data={
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('register'))
        pass

    @mock.patch('project.app.session', {'logged_in': False})
    @mock.patch('project.database.get_all_treatments')
    def test_register_get_no_token(self, gat):
        with tingle.test_client() as client:
            gat.return_value = None
            response = client.get('/register', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('register'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.database.get_all_treatments')
    def test_register_get_no_token_logged_in(self, gat):
        with tingle.test_client() as client:
            gat.return_value = None
            response = client.get('/register', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('patient_dashboard'))
        pass

    @mock.patch('project.database.add_patient')
    @mock.patch('project.database.check_invitation_token_validity')
    def test_register_post_has_token(self, citv, ap):
        with tingle.test_client() as client:
            citv.return_value = [{'ac_email': 'foo@bar.com'}]
            response = client.post('/register/0', data={
                'email-address': 'long@gmail.com'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('register', token='0'))

            citv.return_value = [{'ac_email': 'long@gmail.com'}]
            response = client.post('/register/0', data={
                'email-address': 'long@gmail.com',
                'password': '123',
                'confirm-password': '12345678'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('register', token='0'))

            ap.return_value = None
            citv.return_value = [{'ac_email': 'long@gmail.com'}]
            response = client.post('/register/0', data={
                'email-address': 'long@gmail.com',
                'password': '12345678',
                'confirm-password': '12345678'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('register', token='0'))
        pass

    @mock.patch('project.app.session', {'logged_in': False})
    def test_register_post_has_token_exception(self):
        with tingle.test_client() as client:
            response = client.post('/register/0', data={
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('register', token='0'))

            response = client.get('/researcher', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))

            response = client.get('/clinician', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))

            response = client.get(
                '/clinician/view_patients/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))

            response = client.get(
                '/patient', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))

            response = client.get(
                '/patient/record-symptom', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))

            response = client.get(
                '/patient/account', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))

            response = client.get(
                '/admin', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))
        pass

    @mock.patch('project.database.check_invitation_token_validity')
    def test_register_get_has_token(self, citv):
        with tingle.test_client() as client:
            citv.return_value = True
            response = client.get('/register/0', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('register', token='0'))

            citv.return_value = False
            response = client.get('/register/0', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))
        pass

    @mock.patch('project.email_handler.send_email')
    @mock.patch('project.email_handler.setup_email')
    @mock.patch('project.database.add_password_key')
    @mock.patch('project.database.check_key_exists')
    def test_forgot_password_post(self, cke, apk, sue, see):
        with tingle.test_client() as client:
            cke.return_value = False
            apk.return_value = None
            sue.return_value = 'hi'
            see.return_value = None
            response = client.post('/forgot-password', data={
                'email': 'test@example.com',
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('forgot_password'))

            cke.return_value = [True]
            apk.return_value = None
            sue.return_value = 'hi'
            see.return_value = None
            response = client.post('/forgot-password', data={
                'email': 'test@example.com',
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('forgot_password'))
        pass

    @mock.patch('project.email_handler.send_email')
    @mock.patch('project.email_handler.setup_email')
    @mock.patch('project.database.add_password_key')
    @mock.patch('project.database.check_key_exists')
    def test_forgot_password_post_key_exists(self, cke, apk, sue, see):
        with tingle.test_client() as client:
            cke.return_value = False
            apk.return_value = None
            apk.side_effect = Mock(side_effect=pg8000.core.IntegrityError())
            sue.return_value = 'hi'
            see.return_value = None
            response = client.post('/forgot-password', data={
                'email': 'test@example.com',
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(request.path, url_for('forgot_password'))

            cke.return_value = False
            apk.return_value = None
            apk.side_effect = Mock(side_effect=pg8000.core.ProgrammingError())
            response = client.post('/forgot-password', data={
                'email': 'test@example.com',
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('forgot_password'))
        pass

    def test_forgot_password_get(self):
        with tingle.test_client() as client:
            response = client.get('/forgot-password', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('forgot_password'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'clinician'})
    def test_researcher_dashboard_logged_in(self):
        with tingle.test_client() as client:
            response = client.get('/researcher', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('clinician_dashboard'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'researcher'})
    def test_researcher_dashboard_logged_in_is_researcher(self):
        with tingle.test_client() as client:
            response = client.get('/researcher', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('researcher_dashboard'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'researcher'})
    def test_clinician_dashboard_logged_in(self):
        with tingle.test_client() as client:
            response = client.get('/clinician', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('researcher_dashboard'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'clinician'})
    def test_clinician_dashboard_logged_in_is_clinician(self):
        with tingle.test_client() as client:
            response = client.get('/clinician', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('clinician_dashboard'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'researcher'})
    def test_view_patients_not_clinician(self):
        with tingle.test_client() as client:
            self.assertRaises(Exception, client.get(
                '/clinician/view_patients', follow_redirects=True))
        pass

    @mock.patch('project.database.get_all_patients')
    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {
        'ac_type': 'clinician',
        'ac_id': '1'
    })
    def test_view_patients_is_clinician(self, gap):
        with tingle.test_client() as client:
            gap.return_value = [{'row': '1,2,3,4'}]
            response = client.get(
                '/clinician/view_patients', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('view_patients'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'researcher'})
    def test_view_patients_with_id_not_clinician(self):
        with tingle.test_client() as client:
            self.assertRaises(Exception, client.get(
                '/clinician/view_patients/1', follow_redirects=True))
        pass

    @mock.patch('project.database.get_all_symptoms')
    @mock.patch('project.database.check_clinician_link')
    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'clinician', 'ac_id': '1'})
    def test_view_patients_history_is_clinician(self, ccl, gap):
        with tingle.test_client() as client:
            ccl.return_value = []
            response = client.get(
                '/clinician/view_patients/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('clinician_dashboard'))

            ccl.return_value = [1]
            gap.return_value = [{'row': '1,:00,3,4,5,6,7'}]
            response = client.get(
                '/clinician/view_patients/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for(
                'view_patients_history', id=1))
        pass

    @mock.patch('project.database.delete_token')
    @mock.patch('project.database.update_password')
    def test_reset_password_post(self, up, dt):
        with tingle.test_client() as client:
            response = client.post(
                '/reset-password/abc', data={
                    'pw': '123',
                    'pw_confirm': '1234'
                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for(
                'reset_password', url_key='abc'))

            response = client.post(
                '/reset-password/abc', data={
                    'pw': '123',
                    'pw_confirm': '123'
                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for(
                'reset_password', url_key='abc'))

            up.return_value = False
            response = client.post(
                '/reset-password/abc', data={
                    'pw': '12345678',
                    'pw_confirm': '12345678'
                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for(
                'reset_password', url_key='abc'))

            up.return_value = True
            dt.return_value = None
            response = client.post(
                '/reset-password/abc', data={
                    'pw': '12345678',
                    'pw_confirm': '12345678'
                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for(
                'reset_password', url_key='abc'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'clinician'})
    def test_patient_dashboard_not_patient(self):
        with tingle.test_client() as client:
            response = client.get(
                '/patient', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('clinician_dashboard'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'clinician'})
    def test_record_symptom_is_clinician(self):
        with tingle.test_client() as client:
            response = client.get(
                '/patient/record-symptom', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('clinician_dashboard'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'researcher'})
    def test_record_symptom_is_researcher(self):
        with tingle.test_client() as client:
            response = client.get(
                '/patient/record-symptom', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('researcher_dashboard'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'unknown'})
    def test_record_symptom_is_unknown(self):
        with tingle.test_client() as client:
            self.assertRaises(Exception, client.get(
                '/patient/record-symptom', follow_redirects=True))
        pass

    @mock.patch('project.database.delete_symptom_record')
    @mock.patch('project.database.record_symptom')
    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'patient', 'ac_email': 'long@gmail.com'})
    def test_record_symptom_is_patient_post(self, rs, dsr):
        with tingle.test_client() as client:
            rs.return_value = None
            response = client.post(
                '/patient/record-symptom',
                data={
                    'id': ['1'],
                    'symptom': ['Other', 'abc'],
                    'location': ['Other', 'abc'],
                    'severity': ['0'],
                    'occurence': ['sometimes'],
                    'date': ['2014'],
                    'notes': ['This is']
                },
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('record_symptom'))

            rs.return_value = True
            response = client.post(
                '/patient/record-symptom',
                data={
                    'id': ['1'],
                    'symptom': ['Other', 'abc'],
                    'location': ['Other', 'abc'],
                    'severity': ['0'],
                    'occurence': ['sometimes'],
                    'date': ['2014'],
                    'notes': ['This is']
                },
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('symptom_history'))

            dsr.return_value = None
            rs.return_value = True
            response = client.delete(
                '/patient/record-symptom/1',
                data={
                    'id': ['1'],
                    'symptom': ['Other', 'abc'],
                    'location': ['Other', 'abc'],
                    'severity': ['0'],
                    'occurence': ['sometimes'],
                    'date': ['2014'],
                    'notes': ['This is']
                })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('record_symptom', id='1'))
        pass

    @mock.patch('project.app.session', {'logged_in': False})
    @mock.patch('project.app.user_details', {'ac_type': 'unknown', 'ac_email': None})
    def test_symptom_history_no_user(self):
        with tingle.test_client() as client:
            response = client.get(
                '/patient/symptom-history',
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('login'))
        pass

    @mock.patch('project.database.get_all_symptoms')
    @mock.patch('project.app.user_details', {'ac_type': 'unknown', 'ac_email': 'long@gmail.com'})
    def test_symptom_history_has_user(self, gas):
        with tingle.test_client() as client:
            gas.return_value = [{'row': '1,:00,3,4,5,6,7'}]
            response = client.get(
                '/patient/symptom-history',
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('symptom_history'))
        pass

    def test_patient_reports(self):
        with tingle.test_client() as client:
            response = client.get(
                '/patient/reports',
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('patient_reports'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'clinician', 'ac_email': 'long@gmail.com'})
    def test_patient_account_not_patient_is_clinician(self):
        with tingle.test_client() as client:
            response = client.get(
                '/patient/account',
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('clinician_dashboard'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'researcher', 'ac_email': 'long@gmail.com'})
    def test_patient_account_not_patient_is_researcher(self):
        with tingle.test_client() as client:
            response = client.get(
                '/patient/account',
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('researcher_dashboard'))
        pass

    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'unknown', 'ac_email': 'long@gmail.com'})
    def test_patient_account_not_patient_is_unknown(self):
        with tingle.test_client() as client:
            self.assertRaises(Exception, client.get(
                '/patient/account',
                follow_redirects=True))
        pass

    @mock.patch('project.database.add_patient_clinician_link')
    @mock.patch('project.database.get_account')
    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'patient', 'ac_email': 'long@gmail.com', 'ac_id': '1'})
    def test_patient_account_post(self, ga, apcl):
        with tingle.test_client() as client:
            ga.return_value = None
            response = client.post(
                '/patient/account',
                data={
                    'clinician_email': ['']
                },
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('patient_account'))

            ga.return_value = [{'ac_id': '1', 'ac_type': 'clinician'}]
            apcl.return_value = None
            response = client.post(
                '/patient/account',
                data={
                    'clinician_email': ['clinic@gmail.com']
                },
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('patient_account'))

            ga.return_value = [{'ac_id': '1', 'ac_type': 'clinician'}]
            apcl.return_value = True
            response = client.post(
                '/patient/account',
                data={
                    'clinician_email': ['clinic@gmail.com']
                },
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('patient_account'))

            apcl.side_effect = Mock(side_effect=pg8000.core.IntegrityError())
            ga.return_value = [{'ac_id': '1', 'ac_type': 'clinician'}]
            apcl.return_value = None
            response = client.post(
                '/patient/account',
                data={
                    'clinician_email': ['clinic@gmail.com']
                },
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('patient_account'))
        pass

    @mock.patch('project.database.get_account_by_id')
    @mock.patch('project.database.get_linked_clinicians')
    @mock.patch('project.database.delete_patient_clinician_link')
    @mock.patch('project.database.get_account')
    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.app.user_details', {'ac_type': 'patient', 'ac_email': 'long@gmail.com', 'ac_id': '1'})
    def test_patient_account_delete(self, ga, dpcl, glc, gabi):
        with tingle.test_client() as client:
            ga.return_value = None
            # dpcl.return_value = None
            glc.return_value = None
            response = client.delete(
                '/patient/account/clinic@gmail.com',
                data={
                    'clinician_email': ['clinic@gmail.com']
                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('patient_account'))

            ga.return_value = [{'ac_type': 'clinician', 'ac_id': '1'}]
            dpcl.return_value = None
            glc.return_value = None
            response = client.delete(
                '/patient/account/clinic@gmail.com',
                data={
                    'clinician_email': ['clinic@gmail.com']
                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('patient_account'))

            ga.return_value = [{'ac_type': 'clinician', 'ac_id': '1'}]
            dpcl.return_value = True
            glc.return_value = [{'clinician_id': '1'}]
            gabi.return_value = [
                {'ac_type': 'clinician', 'ac_email': 'clinic@gmail.com'}]
            response = client.delete(
                '/patient/account/clinic.gmail.com',
                data={
                    'clinician_email': ['clinic.gmail.com']
                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for(
                'patient_account', clinician_email='clinic.gmail.com'))
        pass

    @mock.patch('project.app.user_details', {'ac_type': 'clinician', 'ac_email': 'long@gmail.com', 'ac_id': '1'})
    @mock.patch('project.app.session', {'logged_in': True})
    def test_admin_dashboard_not_admin(self):
        with tingle.test_client() as client:
            response = client.get(
                '/admin', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('clinician_dashboard'))
        pass

    @mock.patch('project.app.user_details', {'ac_type': 'admin', 'ac_email': 'long@gmail.com', 'ac_id': '1'})
    @mock.patch('project.app.session', {'logged_in': True})
    def test_admin_dashboard_is_admin(self):
        with tingle.test_client() as client:
            response = client.get(
                '/admin', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('admin_dashboard'))
        pass

    @mock.patch('project.email_handler.send_email')
    @mock.patch('project.email_handler.setup_invitation')
    @mock.patch('project.database.add_account_invitation')
    @mock.patch('project.database.update_role_in_account_invitation')
    @mock.patch('project.database.check_email_in_account_invitation')
    @mock.patch('project.app.user_details', {'ac_type': 'admin', 'ac_email': 'long@gmail.com', 'ac_id': '1'})
    @mock.patch('project.app.session', {'logged_in': True})
    @mock.patch('project.database.get_account')
    def test_invite_user_post(self, ga, ceiai, uriai, aai, si,se):
        with tingle.test_client() as client:
            ga.return_value = True
            response = client.post(
                '/admin/invite',
                data={
                    'email-address': ['admin@example.com'],
                    'role': ['admin'],
                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('admin_dashboard'))

            ga.return_value = False
            ceiai.return_value = [{
                'role': 'labor'
            }]
            uriai.return_value = [{
                'token': '1',
                'role': 'labor'
            }]
            response = client.post(
                '/admin/invite',
                data={
                    'email-address': ['admin@example.com'],
                    'role': ['admin'],
                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('admin_dashboard'))

            ga.return_value = False
            ceiai.return_value = False
            aai.return_value = None
            si.return_value = None
            se.return_value = None
            uriai.return_value = [{
                'token': '1',
                'role': 'labor'
            }]
            response = client.post(
                '/admin/invite',
                data={
                    'email-address': ['admin@example.com'],
                    'role': ['admin'],
                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, url_for('admin_dashboard'))

            ga.return_value = False
            ceiai.return_value = False
            aai.return_value = None
            aai.side_effect = Mock(side_effect=pg8000.core.IntegrityError())
            si.return_value = None
            se.return_value = None
            uriai.return_value = [{
                'token': '1',
                'role': 'labor'
            }]
            response = client.post(
                '/admin/invite',
                data={
                    'email-address': ['admin@example.com'],
                    'role': ['admin'],
                }, follow_redirects=True)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(request.path, url_for('invite_user'))
        pass
    
    def test_service_worker_js(self):
        with tingle.test_client() as client:
            response = client.get('/service-worker.js', content_type='html/text')
            self.assertEqual(response.status_code, 200)
        pass


if __name__ == '__main__':
    unittest.main()
