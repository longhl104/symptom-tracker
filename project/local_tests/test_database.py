import unittest
from unittest import mock
from unittest.mock import Mock, mock_open
import database
import sys
from contextlib import contextmanager
from io import BytesIO, StringIO, TextIOWrapper
import pg8000


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class DatabaseTest(unittest.TestCase):
    def sql_helper_void(self, sql, args=()):
        conn = database.database_connect()
        cur = conn.cursor()
        cur.execute(sql, args)
        conn.commit()
        cur.close()                 # Close the cursor
        conn.close()
        pass

    def sql_helper_fetchone(self, sql, args=()):
        conn = database.database_connect()
        cur = conn.cursor()
        ret = database.dictfetchone(cur, sql, args)
        conn.commit()
        cur.close()                 # Close the cursor
        conn.close()
        return ret[0]

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('pg8000.connect')
    def test_database_connection_no_error(self, conn):
        conn.return_value = True
        self.assertEqual(database.database_connect(), True)
    pass

    @mock.patch('pg8000.connect')
    def test_database_connection_operational_error(self, conn):
        with captured_output() as (out, err):
            conn.side_effect = pg8000.OperationalError
            self.assertTrue(database.database_connect() is None)
        pass

    def test_print_sql_string_with_params(self):
        with captured_output() as (out, err):
            query = "SELECT * FROM tingleserver.\"Treatment\" WHERE %s='long'"
            database.print_sql_string(query, ('name'))

            # This can go inside or outside the `with` block
            output = out.getvalue().strip()
            self.assertEqual(
                output, "SELECT * FROM tingleserver.\"Treatment\" WHERE 'name'='long'")
        pass

    def test_check_login_has_connection(self):
        ret = database.check_login(
            'admin@test.com', 'pbkdf2:sha256:150000$WT5eNrHI$fabc60fc188bcebf165644501d540f27c33998ff5da2f381e743b9097462463e')
        self.assertIsNotNone(ret)

        ret = database.check_login(
            'admin@test.com', '123')
        self.assertIsNone(ret)
        pass

    @mock.patch('pg8000.connect')
    def test_check_login_no_connection(self, conn):
        conn.return_value = None
        ret = database.check_login(
            'admin@test.com', 'pbkdf2:sha256:150000$WT5eNrHI$fabc60fc188bcebf165644501d540f27c33998ff5da2f381e743b9097462463e')
        self.assertIsNone(ret)
        pass

    def test_get_account_has_connection(self):
        ret = database.get_account('admin@test.com')
        self.assertIsNotNone(ret)

        ret = database.get_account('123')
        self.assertIsNone(ret)
        pass

    @mock.patch('pg8000.connect')
    def test_get_account_no_connection(self, conn):
        conn.return_value = None
        ret = database.get_account('admin@test.com')
        self.assertIsNone(ret)
        pass

    def test_get_account_by_id_has_connection(self):
        ret = database.get_account_by_id('56')
        self.assertIsNotNone(ret)

        ret = database.get_account_by_id('1')
        self.assertIsNone(ret)
        pass

    @mock.patch('pg8000.connect')
    def test_get_account_by_id_no_connection(self, conn):
        conn.return_value = None
        ret = database.get_account_by_id('56')
        self.assertIsNone(ret)
        pass

    def test_get_all_treatments_has_connection(self):
        ret = database.get_all_treatments()
        self.assertIsNotNone(ret)
        pass

    @mock.patch('pg8000.connect')
    def test_get_all_treatments_no_connection(self, conn):
        conn.return_value = None
        ret = database.get_all_treatments()
        self.assertIsNone(ret)
        pass

    def test_add_patient_has_connection(self):
        long_str = "0" * 256
        ret = database.add_patient(long_str, 'Nguyen', 'male', '22', '0415147439',
                                   'no treatment', 'long@gmail.com', '12345678', 'hashed', 'admin', 'yes')
        self.assertIsNone(ret)

        ret = database.add_patient('Long', long_str, 'male', '22', '0415147439',
                                   'no treatment', 'long@gmail.com', '12345678', 'hashed', 'admin', 'yes')
        self.assertIsNone(ret)

        ret = database.add_patient('Long', 'Nguyen', 'male', '22', '0415147439',
                                   'no treatment', 'long@gmail.com', long_str, 'hashed', 'admin', 'yes')
        self.assertIsNone(ret)

        ret = database.add_patient('Long', 'Nguyen', 'male', '22', '0415147439',
                                   'no treatment', long_str, '12345678', 'hashed', 'admin', 'yes')
        self.assertIsNone(ret)

        ret = database.add_patient('Long', 'Nguyen', 'male', '22', '0415147439',
                                   'no treatment', 'long@gmail.com', '12345678', 'hashed', 'admin', 'yes')
        self.assertIsNotNone(ret)
        self.sql_helper_void(
            "delete from tingleserver.\"Account\" where ac_id=%s", (ret, ))

        ret = database.add_patient('Long', 'Nguyen', 'male', '22', '0415147439',
                                   ['Oxaliplatin (Eloxatin, Oxalatin, Oxaliccord, Xalox, FOLFOX, XELOX)'], 'long@gmail.com', '12345678', 'hashed', 'patient', 'yes')
        self.assertIsNotNone(ret)
        self.sql_helper_void(
            "delete from tingleserver.\"Account\" where ac_id=%s", (ret, ))
        pass

    @mock.patch('pg8000.connect')
    def test_add_patient_no_connection(self, conn):
        conn.return_value = None
        ret = database.add_patient('Long', 'Nguyen', 'male', '22', '0415147439',
                                   ['Oxaliplatin (Eloxatin, Oxalatin, Oxaliccord, Xalox, FOLFOX, XELOX)'], 'long@gmail.com', '12345678', 'hashed', 'patient', 'yes')
        self.assertIsNone(ret)
        pass

    def test_record_symptom_has_connection(self):
        ret = database.record_symptom(
            '', 'patient@test.com', 'Numbness', 'Hands', 'Quite a bit', 'Daytime', '2020-10-08', '')
        self.assertEqual(ret, 'patient@test.com')
        id = self.sql_helper_fetchone(
            "select max(symptom_id) from tingleserver.\"Symptom\"")['max']

        ret = database.record_symptom(str(
            id), 'patient@test.com', 'Numbness', 'Hands', 'Quite a bit', 'Daytime', '2020-10-08', '')
        self.assertEqual(ret, 'patient@test.com')

        self.sql_helper_void(
            "delete from tingleserver.\"Symptom\" where symptom_id=%s", (id, ))

        pass

    @mock.patch('pg8000.connect')
    def test_record_symptom_no_connection(self, conn):
        conn.return_value = None
        ret = database.record_symptom(
            '', 'patient@test.com', 'Numbness', 'Hands', 'Quite a bit', 'Daytime', '2020-10-08', '')
        self.assertIsNone(ret)
        pass

    def test_get_all_symptoms_has_connection(self):
        ret = database.get_all_symptoms('patient@test.com')
        self.assertEqual(
            [{'row': '(15,2020-10-14,Tingling,Hands,Somewhat,Daytime,"")'}, {'row': '(14,2020-10-13,Pain,Legs,"A little bit",Morning,"")'},
             {'row': '(13,2020-10-08,Numbness,Hands,"Quite a bit",Daytime,"")'}],
            ret
        )
        pass

    @mock.patch('pg8000.connect')
    def test_get_all_symptoms_no_connection(self, conn):
        conn.return_value = None
        ret = database.get_all_symptoms('patient@test.com')
        self.assertIsNone(ret)
        pass

    # def test_get_all_patients_has_connection(self):
    #     ret = database.get_all_patients('clinician@test.com')
    #     print(ret)
    #     pass

    @mock.patch('pg8000.connect')
    def test_get_all_patients_no_connection(self, conn):
        conn.return_value = None
        ret = database.get_all_patients('clinician@test.com')
        self.assertIsNone(ret)
        pass

    def test_check_clinician_lick_has_connection(self):

        pass

if __name__ == '__main__':
    unittest.main()
