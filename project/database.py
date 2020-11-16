import os
import logging
import configparser
import json
import sys
import pg8000
from datetime import date
import sqlalchemy

class DatabaseHandler:
    def __init__(self, debug=True):
        if debug:
            # Read the config file
            config = configparser.ConfigParser()
            config.read('config.ini')
            self.db_user = config['DATABASE']['user']
            self.db_name = config['DATABASE']['database']
            self.db_pass = config['DATABASE']['password']
            self.db_host = config['DATABASE']['host']
            self.query = {}
        else:
            self.db_user = os.environ.get("DB_USER")
            self.db_pass = os.environ.get("DB_PASS")
            self.db_name = os.environ.get("DB_NAME")
            self.db_host = os.environ.get("DB_HOST")
            db_socket_dir = "/cloudsql"
            cloud_sql_connection_name = os.environ.get("CONNECTION_NAME")
            self.query = {
                "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                    db_socket_dir,
                    cloud_sql_connection_name)
            }

    def connect(self):
        db_config = {
            "pool_size": 5,
            "max_overflow": 2,
            "pool_timeout": 30,
            "pool_recycle": 1800,
        }
        pool = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername="postgres+pg8000",
                username=self.db_user,
                password=self.db_pass,
                database=self.db_name,
                query=self.query
            ),
            **db_config
        )
        return pool  

db = DatabaseHandler().connect()

def check_login(email, password):
    """
    Check that the users information exists in the database.
        - True => return the user data
        - False => return None
    """
    with db.connect() as conn:
        try:
            sql = """
                SELECT *
                FROM tingleserver."Account"
                WHERE ac_email=:email AND ac_password=:password
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, email=email, password=password).fetchone()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error Invalid Login")
    return None

def get_account(email):
    with db.connect() as conn:
        try:
            sql = """
                SELECT *
                FROM tingleserver."Account"
                WHERE ac_email=:email
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, email=email).fetchone()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't get account by email")
    return None

def get_account_by_id(id):
    with db.connect() as conn:
        try:
            sql = """
                SELECT *
                FROM tingleserver."Account"
                WHERE ac_id=:ac_id
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, ac_id=id).fetchone()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't get account by ID")
    return None

def get_all_treatments():
    with db.connect() as conn:
        try:
            sql = """
                SELECT tingleserver."Treatment".treatment_name 
                FROM tingleserver."Treatment"
            """
            result = conn.execute(sql).fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting All Treatments:", sys.exc_info()[0])
            raise
    return None


def add_patient(firstname, lastname, gender, age, mobile, treatment, email, original_password, password_hash, role, consent):

    # Catching boundary cases
    # TODO: return error message to user
    # ! We can have this done by using javascript
    if len(firstname) > 255:
        print("First name entered is greater than maximum length of 255.")
        return None
    if len(lastname) > 255:
        print("Last name entered is greater than maximum length of 255.")
        return None
    elif len(original_password) < 8 or len(original_password) > 20:
        print("Password should be between 8 and 20 characters.")
        return None
    elif len(email) > 255:
        print("Email entered is greater than maximum length of 255.")
        return None
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            # Try executing the SQL and get from the database
            sql = """
                SELECT tingleserver.add_account(:firstname, :lastname, :gender, :age, :mobile, :email, :password_hash, :role, :consent)
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, firstname=firstname, lastname=lastname, gender=gender, age=age, mobile=mobile, email=email, password_hash=password_hash, role=role, consent=consent).fetchone()
            patient_id = result[0]
            if role == 'patient':
                if treatment is not None and len(treatment) > 0:
                    for t in treatment:
                        sql = """
                            SELECT treatment_id
                            FROM tingleserver."Treatment"
                            WHERE treatment_name=:name;
                        """
                        stmt = sqlalchemy.text(sql)
                        result = conn.execute(stmt, name=t).fetchone()
                        treatment_id = result[0]
                        sql = """
                            INSERT INTO tingleserver."Patient_Receives_Treatment"(
                                patient_id, treatment_id)
                                VALUES (:patient_id, :treatment_id);
                        """
                        stmt = sqlalchemy.text(sql)
                        conn.execute(stmt, patient_id=patient_id, treatment_id=treatment_id)
            transaction.commit()
            return patient_id
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error adding a patient:", sys.exc_info()[0])
            transaction.rollback()
            raise
    return None

def record_symptom(id, email, symptom, location, severity, occurence, date, notes):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            # Try executing the SQL and get from the database
            if len(id) == 0:
                sql = """
                    INSERT INTO tingleserver."Symptom"(
                        patient_username, symptom_name, location, severity, occurence, recorded_date, notes)
                        VALUES(:email, :symptom, :location, :severity, :occurence, :date, :notes);
                """
                stmt = sqlalchemy.text(sql)
                conn.execute(stmt, email=email, symptom=symptom, location=location, severity=severity, occurence=occurence, date=date, notes=notes)
            else:
                sql = """
                    UPDATE tingleserver."Symptom" SET
                        symptom_name = :symptom, location = :location, severity = :severity, occurence = :occurence, recorded_date = :date, notes = :notes
                        WHERE symptom_id = :id AND patient_username = :email
                """
                stmt = sqlalchemy.text(sql)
                conn.execute(stmt, symptom=symptom, location=location, severity=severity, occurence=occurence, date=date, notes=notes, id=id, email=email)
            transaction.commit()
            return email
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error adding a patient:", sys.exc_info()[0])
            transaction.rollback()
            raise
    return None

def get_all_symptoms(email):
    with db.connect() as conn:
        try:
            sql = """
                SELECT (symptom_id, recorded_date, symptom_name, location, severity, occurence, notes)
                FROM tingleserver."Symptom" 
                WHERE patient_username = :patient_username
                ORDER BY recorded_date DESC
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, patient_username=email).fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all symptoms: ", sys.exc_info()[0])
            raise
    return None

def get_name_symptoms(email):
    with db.connect() as conn:
        try:
            sql = """
                SELECT (symptom_name)
                FROM tingleserver."Symptom" 
                WHERE patient_username = :patient_username 
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, patient_username=email).fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all symptoms: ", sys.exc_info()[0])
            raise
    return None


def get_all_consent():
    with db.connect() as conn:
        try:
            sql = """
                SELECT (A.ac_email, A.ac_id, A.ac_age, A.ac_gender, T.treatment_name)
                FROM tingleserver."Patient" AS P
                INNER JOIN 
                tingleserver."Account" AS A
                ON P.ac_id = A.ac_id 
                INNER JOIN
                tingleserver."Patient_Receives_Treatment" AS PRT
                ON A.ac_id = PRT.patient_id
                INNER JOIN
                tingleserver."Treatment" AS T
                ON PRT.treatment_id  = T.treatment_id
                WHERE P.consent = :consent
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, consent="yes").fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all symptoms: ", sys.exc_info()[0])
            raise
    return None

def get_all_consent_export_all():
    with db.connect() as conn:
        try:
            sql = """
                SELECT (A.ac_id, A.ac_age, A.ac_gender, T.treatment_name, S.symptom_name, S.location, S.recorded_date, S.severity, S.occurence)
                FROM tingleserver."Patient" AS P
                INNER JOIN 
                tingleserver."Account" AS A
                ON P.ac_id = A.ac_id 
                INNER JOIN
                tingleserver."Symptom" AS S
                ON A.ac_email = S.patient_username
                INNER JOIN
                tingleserver."Patient_Receives_Treatment" AS PRT
                ON A.ac_id = PRT.patient_id
                INNER JOIN
                tingleserver."Treatment" AS T
                ON PRT.treatment_id  = T.treatment_id
                WHERE P.consent =:consent
                ORDER BY A.ac_id, S.recorded_date, CASE WHEN S.occurence = 'Morning' THEN 1
                                            WHEN S.occurence = 'Daytime' THEN 2
                                            WHEN S.occurence = 'Night-time' THEN 3
                                            WHEN S.occurence = 'All the time' THEN 4
                                            WHEN S.occurence = 'Sporadic' THEN 5 
                                    END
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, consent="yes").fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all data: ", sys.exc_info()[0])
            raise
    return None

def get_consent_export_filters(age_low, age_high, gender, symptom, chemo):
    if gender == "":
        single_gender = ""
    else :
        single_gender = " AND A.gender=:gender"

    if symptom == "":
        single_symptom = ""
    else :
        single_symptom = " AND S.symptom_name=:symptom"

    if chemo == "":
        single_chemo = ""
    else :
        single_chemo = " AND T.treatment_name=:treatment"

    age_query = ""
    if age_low == "" and age_high != "":
        date_query = " AND A.age <= :age_high"
    elif age_low != "" and age_high == "":
        date_query = " AND A.age >= :age_low"
    elif age_low != "" and age_high != "":
        date_query = " AND A.age BETWEEN :age_low AND :age_high"

    with db.connect() as conn:
        try:
            sql = None
            r = None
            sql = """
                SELECT (A.ac_id, A.ac_age, A.ac_gender, T.treatment_name, S.symptom_name, S.location, S.recorded_date, S.severity, S.occurence)
                FROM tingleserver."Patient" AS P
                INNER JOIN 
                tingleserver."Account" AS A
                ON P.ac_id = A.ac_id 
                INNER JOIN
                tingleserver."Symptom" AS S
                ON A.ac_email = S.patient_username
                INNER JOIN
                tingleserver."Patient_Receives_Treatment" AS PRT
                ON A.ac_id = PRT.patient_id
                INNER JOIN
                tingleserver."Treatment" AS T
                ON PRT.treatment_id  = T.treatment_id
                WHERE P.consent =:consent{single_gender}{single_symptom}{single_chemo}{age_query}
                ORDER BY A.ac_id, S.recorded_date, CASE WHEN S.occurence = 'Morning' THEN 1
                                            WHEN S.occurence = 'Daytime' THEN 2
                                            WHEN S.occurence = 'Night-time' THEN 3
                                            WHEN S.occurence = 'All the time' THEN 4
                                            WHEN S.occurence = 'Sporadic' THEN 5 
                                    END
            """.format(single_gender=single_gender, single_symptom=single_symptom, single_chemo=single_chemo, age_query=age_query)
            params = {
                "consent": "yes"
            }

            if gender != "":
                params["gender"] = gender
            if symptom != "":
                params["symptom"] = symptom
            if chemo != "":
                params["chemo"] = chemo
            if age_low != "":
                params["age_low"] = age_low
            if age_high != "":
                params["age_high"] = age_high
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, **params).fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all symptoms: ", sys.exc_info()[0])
            raise
    return None

def get_all_patients(email):
    with db.connect() as conn:
        try:
            sql = """
                SELECT (tingleserver."Account".ac_id,tingleserver."Account".ac_email,tingleserver."Account".ac_firstname,tingleserver."Account".ac_lastname,tingleserver."Account".ac_age,tingleserver."Account".ac_gender)
                FROM tingleserver."Patient_Clinician" INNER JOIN tingleserver."Account" ON tingleserver."Patient_Clinician".patient_id = tingleserver."Account".ac_id 
                WHERE tingleserver."Patient_Clinician".clinician_id=:clinician_id
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, clinician_id=email).fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all symptoms: ", sys.exc_info()[0])
            raise
    return None

def check_clinician_link(clinician_id, patient_email):
    with db.connect() as conn:
        try:
            sql = """
                SELECT *
                FROM tingleserver."Patient_Clinician" INNER JOIN tingleserver."Account" ON tingleserver."Patient_Clinician".patient_id = tingleserver."Account".ac_id 
                WHERE tingleserver."Patient_Clinician".clinician_id =:clinician_id
                AND tingleserver."Account".ac_email = :ac_email
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, clinician_id=clinician_id, ac_email=patient_email).fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting link: ", sys.exc_info()[0])
            raise
    return None

def check_key_exists(email):
    with db.connect() as conn:
        try:
            sql = """
                SELECT * 
                FROM tingleserver."Forgot_password"
                WHERE ac_email = :ac_email
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, ac_email=email).fetchone()
            return result
        except:
            print("Unexpected error retrieving key: ", sys.exc_info()[0])
            raise
    return None

def add_password_key(key, email):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                INSERT INTO tingleserver."Forgot_password"(
                    key, ac_email)
                    VALUES(:key, :email);
            """
            stmt = sqlalchemy.text(sql)
            conn.execute(stmt, key=key, email=email)
            transaction.commit()
            return email
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error creating a unique key: ", sys.exc_info()[0])
            transaction.rollback()
            raise
    return None

def update_password(ac_password, url_key):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                UPDATE tingleserver."Account"
                    SET ac_password = :ac_password
                    WHERE ac_email = (
                        SELECT ac_email
                        FROM tingleserver."Forgot_password"
                        WHERE key=:key
                    );
            """
            stmt = sqlalchemy.text(sql)
            conn.execute(stmt, key=url_key, ac_password=ac_password)
            transaction.commit()
            stmt = sqlalchemy.text('SELECT * FROM tingleserver."Forgot_password" WHERE key=:key')
            result = conn.execute(stmt, key=url_key).fetchone()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error updating password: ", sys.exc_info()[0])
            transaction.rollback()
    return None

def delete_token(url_key):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                DELETE FROM tingleserver."Forgot_password"
                WHERE key = :key;
            """
            stmt = sqlalchemy.text(sql)
            conn.execute(stmt, key=url_key)
            transaction.commit()
            return None
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error deleting token: ", sys.exc_info()[0])
            transaction.rollback()
            raise
    return None

def delete_symptom_record(email, id):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                DELETE FROM tingleserver."Symptom" WHERE patient_username = :email AND symptom_id = :id
            """
            stmt = sqlalchemy.text(sql)
            conn.execute(stmt, email=email, id=id)
            transaction.commit()
            sql = """
                SELECT COUNT(*) FROM tingleserver."Symptom" WHERE patient_username = :email AND symptom_id = :id
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, email=email, id=id).fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error deleting:", sys.exc_info()[0])
            raise
    return None

def add_patient_clinician_link(patient_id, clinician_id):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                INSERT INTO tingleserver."Patient_Clinician"(
                    patient_id, clinician_id)
                    VALUES(:patient_id, :clinician_id);
            """
            stmt = sqlalchemy.text(sql)
            conn.execute(stmt, patient_id=patient_id, clinician_id=clinician_id)
            transaction.commit()
            return patient_id
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error linking patient and clinician ", sys.exc_info()[0])
            transaction.rollback()
            raise
    return None

def delete_patient_clinician_link(patient_id, clinician_id):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                DELETE FROM tingleserver."Patient_Clinician" WHERE patient_id = :patient_id AND clinician_id = :clinician_id
            """
            stmt = sqlalchemy.text(sql)
            conn.execute(stmt, patient_id=patient_id, clinician_id=clinician_id)
            transaction.commit()
            return patient_id
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error deleting patient-clinician link:", sys.exc_info()[0])
            raise
    return None

def get_linked_clinicians(patient_id):
    with db.connect() as conn:
        try:
            sql = """
                SELECT clinician_id
                FROM tingleserver."Patient_Clinician" WHERE patient_id = :patient_id
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, patient_id=patient_id).fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all clinicians: ", sys.exc_info()[0])
            raise
    return None

def check_invitation_token_validity(token):
    with db.connect() as conn:
        try:
            sql = """
                SELECT ac_email, role
                FROM tingleserver."Account_Invitation"
                WHERE token=:token
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, token=token).fetchone()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't get account invitation")
    return None

def check_email_in_account_invitation(email):
    with db.connect() as conn:
        try:
            sql = """
                SELECT *
                FROM tingleserver."Account_Invitation"
                WHERE ac_email=:ac_email
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, ac_email=email).fetchone()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't get account invitation")
    return None

def update_role_in_account_invitation(email, role):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                UPDATE tingleserver."Account_Invitation"
                SET role=:role
                WHERE ac_email=:ac_email
                RETURNING token, role;
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, role=role, ac_email=email).fetchone()
            transaction.commit()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't update account invitation")
    return None

def add_account_invitation(token, email, role):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                INSERT INTO tingleserver."Account_Invitation" (token, ac_email, role)
                VALUES(:token, :email, :role);
            """
            stmt = sqlalchemy.text(sql)
            conn.execute(stmt, role=role, email=email, token=token)
            transaction.commit()
            return email
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error inserting invitation: ", sys.exc_info()[0])
            transaction.rollback()
            raise
    return None

def delete_account_invitation(token, email):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                DELETE FROM tingleserver."Account_Invitation"
                WHERE ac_email=:email
                AND token=:token;
            """
            stmt = sqlalchemy.text(sql)
            conn.execute(stmt, email=email, token=token)
            transaction.commit()
            return email
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error inserting invitation: ", sys.exc_info()[0])
            transaction.rollback()
            raise
    return None

def get_all_questionnaires():
    with db.connect() as conn:
        try:
            sql = """
                SELECT id, name, end_date FROM tingleserver."Questionnaire"
                ORDER BY name
            """
            result = conn.execute(sql).fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all questionnaires: ", sys.exc_info()[0])
            raise
    return None

def get_export_data(email, symptom, location, start_date, end_date, with_notes):
    notes_var = ""
    extra_vars = ""
    single_symptom = " AND symptom_name=:symptom"
    single_location = " AND location=:location"
    if symptom == "All":
        extra_vars = "symptom_name, location, "
        single_symptom = ""
    if location == "All":
        extra_vars = "symptom_name, location, "
        single_location = ""
    if (with_notes):
        notes_var = ", notes"

    date_query = ""
    if start_date == "" and end_date != "":
        date_query = " AND recorded_date <= :end_date"
    elif start_date != "" and end_date == "":
        date_query = " AND recorded_date >= :start_date"
    elif start_date != "" and end_date != "":
        date_query = " AND recorded_date BETWEEN :start_date AND :end_date"

    with db.connect() as conn:
        try:
            sql = None
            r = None
            sql = """
                SELECT ({extra_vars}recorded_date, severity, occurence{notes_var}) 
                FROM tingleserver."Symptom"
                WHERE patient_username=:email{single_symptom}{single_location}{date_query}
                ORDER BY recorded_date, CASE WHEN occurence = 'Morning' THEN 1
                                            WHEN occurence = 'Daytime' THEN 2
                                            WHEN occurence = 'Night-time' THEN 3
                                            WHEN occurence = 'All the time' THEN 4
                                            WHEN occurence = 'Sporadic' THEN 5 
                                    END
            """.format(extra_vars = extra_vars, notes_var=notes_var, single_symptom=single_symptom, single_location=single_location, date_query=date_query)
            params = {
                "email": email,
            }

            if symptom != "All":
                params["symptom"] = symptom
            if location != "All":
                params["location"] = location
            if start_date != "":
                params["start_date"] = start_date
            if end_date != "":
                params["end_date"] = end_date
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, **params).fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all symptoms: ", sys.exc_info()[0])
            raise
    return None

def get_patient_by_email(email):
    with db.connect() as conn:
        try:
            sql = """
                SELECT ac_id FROM tingleserver."Account" NATURAL JOIN tingleserver."Patient"
                WHERE ac_email = :email;
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, email=email).fetchone()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't get patient by email")
    return None

def get_patient_name(email):
    with db.connect() as conn:
        try:
            sql = """
                SELECT ac_firstname, ac_lastname FROM tingleserver."Account" NATURAL JOIN tingleserver."Patient"
                WHERE ac_email=:email;
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, email=email).fetchone()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't get patient by email")
    return None

def get_questionnaire(link, id=None):
    with db.connect() as conn:
        try:
            sql = """
                SELECT *
                FROM tingleserver."Questionnaire"
                WHERE link=:link
                OR id=:id
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, link=link, id=id).fetchone()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't get questionnaire by link")
    return None

def delete_questionnaire(id):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                DELETE FROM tingleserver."Patient_Receives_Questionnaire"
                WHERE questionnaire_id=:id;
            """
            stmt = sqlalchemy.text(sql)
            conn.execute(stmt, id=id)
            sql = """
                DELETE FROM tingleserver."Questionnaire"
                WHERE id=:id;
            """
            stmt = sqlalchemy.text(sql)
            conn.execute(stmt, id=id)
            transaction.commit()
            return id
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't delete questionnaire by id")
    return None

def get_patient_questionnaires(id):
    with db.connect() as conn:
        try:
            today = str(date.today())
            sql = """
                SELECT id, name, end_date, opened FROM tingleserver."Questionnaire" Q
                JOIN tingleserver."Patient_Receives_Questionnaire" PRQ ON (Q.id = PRQ.questionnaire_id)
                WHERE ac_id=:ac_id
                AND end_date >=:end_date
                AND completed=:completed;
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, ac_id=id, end_date=today, completed=False).fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting questionnaire: ", sys.exc_info()[0])
            raise
    return None

def add_questionnaire(name, link, end_date):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                INSERT INTO tingleserver."Questionnaire" (name, link, end_date)
                VALUES(:name, :link, :end_date)
                RETURNING id;
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, name=name, link=link, end_date=end_date).fetchone()
            transaction.commit()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error inserting questionnaire: ", sys.exc_info()[0])
            transaction.rollback()
            raise
    return None

def update_questionnaire(id, name, link, end_date):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                UPDATE tingleserver."Questionnaire"
                    SET name=:name,
                        link=:link,
                        end_date=:end_date
                    WHERE id=:id;
            """
            stmt = sqlalchemy.text(sql)
            conn.execute(stmt, name=name, link=link, end_date=end_date, id=id)
            transaction.commit()
            sql = """SELECT *
                    FROM tingleserver."Questionnaire"
                    WHERE id=:id"""
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, id=id).fetchone()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error updating questionnaire: ", sys.exc_info()[0])
            transaction.rollback()
            raise
    return None

def link_questionnaire_to_patient(questionnaire_id, valid_recipients):
    successful_records = []
    with db.connect() as conn:
        transaction = conn.begin()
        for id, email in valid_recipients:
            try:
                sql = """
                    INSERT INTO tingleserver."Patient_Receives_Questionnaire"
                    (ac_id, questionnaire_id)
                    VALUES (:ac_id, :questionnaire_id)
                    RETURNING ac_id;
                """
                stmt = sqlalchemy.text(sql)
                result = conn.execute(stmt, ac_id=id, questionnaire_id=questionnaire_id).fetchone()
                transaction.commit()
                successful_records.append(email)
            except:
                # If there were any errors, return a NULL row printing an error to the debug
                print("Error: can't link questionnaire and patient")
                continue
    return successful_records

def get_all_patients_in_db():
    with db.connect() as conn:
        try:
            sql = """
                SELECT ac_id, ac_email FROM tingleserver."Account" NATURAL JOIN tingleserver."Patient";
            """
            result = conn.execute(sql).fetchall()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all patients:", sys.exc_info()[0])
            raise
    return None

def mark_questionnaire_as_opened(patient_id, questionnaire_id):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                UPDATE tingleserver."Patient_Receives_Questionnaire"
                SET opened=:opened
                WHERE ac_id=:patient_id
                AND questionnaire_id=:questionnaire_id
                RETURNING opened;
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, opened=True, patient_id=patient_id, questionnaire_id=questionnaire_id).fetchone()
            transaction.commit()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't update questionnaire 'opened' column")
    return None

def mark_questionnaire_as_completed(patient_id, questionnaire_id):
    with db.connect() as conn:
        transaction = conn.begin()
        try:
            sql = """
                UPDATE tingleserver."Patient_Receives_Questionnaire"
                SET completed=:completed
                WHERE ac_id=:patient_id
                AND questionnaire_id=:questionnaire_id
                RETURNING completed;
            """
            stmt = sqlalchemy.text(sql)
            result = conn.execute(stmt, completed=True, patient_id=patient_id, questionnaire_id=questionnaire_id).fetchone()
            transaction.commit()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't update questionnaire 'completed' column")
    return None
