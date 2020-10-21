import configparser
import json
import sys
import pg8000

def database_connect():
    """
    Connects to the database using the connection string.
    If 'None' was returned it means there was an issue connecting to
    the database. It would be wise to handle this ;)
    """
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'database' not in config['DATABASE']:
        config['DATABASE']['database'] = config['DATABASE']['user']

    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['database'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as operation_error:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(operation_error)
        return None

    # return the connection to use
    return connection

##################################################
# Print a SQL string to see how it would insert  #
##################################################


def print_sql_string(inputstring, params=None):
    """
    Prints out a string as a SQL string parameterized assuming all strings
    """

    if params is not None and len(params) != 0:
        inputstring = inputstring.replace("%s", "'%s'")

    print(inputstring % params)

#####################################################
#   SQL Dictionary Fetch
#   useful for pulling particular items as a dict
#   (No need to touch
#       (unless the exception is potatoing))
#   Expected return:
#       singlerow:  [{col1name:col1value,col2name:col2value, etc.}]
#       multiplerow: [{col1name:col1value,col2name:col2value, etc.},
#           {col1name:col1value,col2name:col2value, etc.},
#           etc.]
#####################################################


def dictfetchall(cursor, sqltext, params=()):
    """ Returns query results as list of dictionaries."""

    result = []
    if len(params) == 0:
        print(sqltext)
    else:
        print("we HAVE PARAMS!")
        print_sql_string(sqltext, params)

    cursor.execute(sqltext, params)
    cols = [a[0].decode("utf-8") for a in cursor.description]
    print(cols)
    returnres = cursor.fetchall()
    for row in returnres:
        result.append({a: b for a, b in zip(cols, row)})
    # cursor.close()
    return result


def dictfetchone(cursor, sqltext, params=()):
    """ Returns query results as list of dictionaries."""
    # cursor = conn.cursor()
    result = []
    cursor.execute(sqltext, params)
    cols = [a[0].decode("utf-8") for a in cursor.description]
    returnres = cursor.fetchone()
    result.append({a: b for a, b in zip(cols, returnres)})
    return result

def check_login(email, password):
    """
    Check that the users information exists in the database.
        - True => return the user data
        - False => return None
    """
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                SELECT *
                FROM tingleserver."Account"
                WHERE ac_email=%s AND ac_password=%s
            """
            cur.execute(sql, (email, password))
            # r = cur.fetchone()

            r = dictfetchone(cur, sql, (email, password))
            print(r)
            cur.close()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return r
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error Invalid Login")
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def get_account(email):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                SELECT *
                FROM tingleserver."Account"
                WHERE ac_email=%s
            """
            cur.execute(sql, (email,))
            # r = cur.fetchone()

            r = dictfetchone(cur, sql, (email,))
            cur.close()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return r
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't get account by email")
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def get_account_by_id(id):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                SELECT *
                FROM tingleserver."Account"
                WHERE ac_id=%s
            """
            cur.execute(sql, (id,))
            # r = cur.fetchone()

            r = dictfetchone(cur, sql, (id,))
            cur.close()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return r
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't get hashed password")
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def get_all_treatments():
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                SELECT tingleserver."Treatment".treatment_name 
                FROM tingleserver."Treatment"
            """

            r = dictfetchall(cur, sql)
            print("return val is:")
            print(r)
            cur.close()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return r
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting All Treatments:", sys.exc_info()[0])
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
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

    conn = database_connect()

    if conn:
        cur = conn.cursor()
        try:
            # Try executing the SQL and get from the database
            sql = """
                SELECT tingleserver.add_account(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (firstname, lastname, gender, age, mobile, email, password_hash, role, consent))
            conn.commit()
            patient_id = cur.fetchone()[0]
            if role == 'patient':
                if treatment is not None and len(treatment) > 0:
                    for t in treatment:
                        sql = """
                            SELECT treatment_id
                            FROM tingleserver."Treatment"
                            WHERE treatment_name=%s;
                        """
                        cur.execute(sql, (t,))
                        conn.commit()
                        treatment_id = cur.fetchone()[0]
                        print(treatment_id)

                        sql = """
                            INSERT INTO tingleserver."Patient_Receives_Treatment"(
                                patient_id, treatment_id)
                                VALUES (%s, %s);
                        """
                        cur.execute(sql, (patient_id, treatment_id))
                        conn.commit()

            cur.close()
            conn.close()                    # Close the connection to the db
            return patient_id
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error adding a patient:", sys.exc_info()[0])
            conn.rollback()
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def record_symptom(id, email, symptom, location, severity, occurence, date, notes):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            print(email)
            # Try executing the SQL and get from the database
            if len(id) == 0:
                sql = """
                    INSERT INTO tingleserver."Symptom"(
                        patient_username, symptom_name, location, severity, occurence, recorded_date, notes)
                        VALUES(%s, %s, %s, %s, %s, %s, %s);
                """
                cur.execute(sql, (email, symptom, location, severity, occurence, date, notes))
            else:
                sql = """
                    UPDATE tingleserver."Symptom" SET
                        symptom_name = %s, location = %s, severity = %s, occurence = %s, recorded_date = %s, notes = %s
                        WHERE symptom_id = %s AND patient_username = %s
                """
                cur.execute(sql, (symptom, location, severity, occurence, date, notes, id, email))
            conn.commit()
            cur.close()
            return email
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error adding a patient:", sys.exc_info()[0])
            conn.rollback()
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def get_all_symptoms(email):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                SELECT (symptom_id, recorded_date, symptom_name, location, severity, occurence, notes)
                FROM tingleserver."Symptom" 
                WHERE patient_username = %s 
                ORDER BY recorded_date DESC
            """

            r = dictfetchall(cur, sql, (email,))
            print("return val is:")
            print(r)
            cur.close()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return r
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all symptoms: ", sys.exc_info()[0])
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None


def get_all_patients(email):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                SELECT (tingleserver."Account".ac_id,tingleserver."Account".ac_email,tingleserver."Account".ac_firstname,tingleserver."Account".ac_lastname,tingleserver."Account".ac_age,tingleserver."Account".ac_gender)
                FROM tingleserver."Patient_Clinician" INNER JOIN tingleserver."Account" ON tingleserver."Patient_Clinician".patient_id = tingleserver."Account".ac_id 
                WHERE tingleserver."Patient_Clinician".clinician_id =%s
            """

            r = dictfetchall(cur, sql, (email,))
            cur.close()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return r
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all symptoms: ", sys.exc_info()[0])
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None
def check_clinician_link(clinician_id, patient_email):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                SELECT *
                FROM tingleserver."Patient_Clinician" INNER JOIN tingleserver."Account" ON tingleserver."Patient_Clinician".patient_id = tingleserver."Account".ac_id 
                WHERE tingleserver."Patient_Clinician".clinician_id =%s
                AND tingleserver."Account".ac_email = %s
            """

            cur.execute(sql,(clinician_id,patient_email))
            r = dictfetchall(cur, sql, (clinician_id,patient_email,))
            cur.close()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return r
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting link: ", sys.exc_info()[0])
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None
def check_key_exists(email):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                SELECT * 
                FROM tingleserver."Forgot_password"
                WHERE ac_email = %s
            """
            cur.execute(sql, (email, ))
            result = cur.fetchone()
            conn.commit()
            cur.close()
            return result
        except:
            print("Unexpected error retrieving key: ", sys.exc_info()[0])
            conn.rollback()
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def add_password_key(key, email):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                INSERT INTO tingleserver."Forgot_password"(
                    key, ac_email)
                    VALUES(%s, %s);
            """
            cur.execute(sql, (key, email))
            conn.commit()
            cur.close()
            return email
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error creating a unique key: ", sys.exc_info()[0])
            conn.rollback()
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def update_password(ac_password, url_key):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                UPDATE tingleserver."Account"
                    SET ac_password = %s
                    WHERE ac_email = (
                        SELECT ac_email
                        FROM tingleserver."Forgot_password"
                        WHERE key=%s
                    );
            """
            cur.execute(sql, (ac_password, url_key))
            result = dictfetchone(cur, """SELECT *
                                            FROM tingleserver."Forgot_password"
                                            WHERE key=%s""", (url_key,))
            conn.commit()
            cur.close()
            return result
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error updating password: ", sys.exc_info()[0])
            conn.rollback()
        cur.close()                     # Close the cursor
        conn.close()  
    return None

def delete_token(url_key):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                DELETE FROM tingleserver."Forgot_password"
                WHERE key = %s;
            """
            cur.execute(sql, (url_key,))
            conn.commit()
            cur.close()
            return None
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error deleting token: ", sys.exc_info()[0])
            conn.rollback()
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def delete_symptom_record(email, id):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                DELETE FROM tingleserver."Symptom" WHERE patient_username = %s AND symptom_id = %s
            """
            print_sql_string(sql, (email,id,))
            cur.execute(sql, (email,id,))
            sql = """
                SELECT COUNT(*) FROM tingleserver."Symptom" WHERE patient_username = %s AND symptom_id = %s
            """
            r = dictfetchall(cur, sql, (email,id,))
            print("return val is:")
            print(r)
            conn.commit()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return r
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error deleting:", sys.exc_info()[0])
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def add_patient_clinician_link(patient_id, clinician_id):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                INSERT INTO tingleserver."Patient_Clinician"(
                    patient_id, clinician_id)
                    VALUES(%s, %s);
            """
            cur.execute(sql, (patient_id, clinician_id))
            conn.commit()
            cur.close()
            return patient_id
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error linking patient and clinician ", sys.exc_info()[0])
            conn.rollback()
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def delete_patient_clinician_link(patient_id, clinician_id):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                DELETE FROM tingleserver."Patient_Clinician" WHERE patient_id = %s AND clinician_id = %s
            """
            cur.execute(sql, (patient_id,clinician_id,))
            conn.commit()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return patient_id
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error deleting patient-clinician link:", sys.exc_info()[0])
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def get_linked_clinicians(patient_id):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                SELECT clinician_id
                FROM tingleserver."Patient_Clinician" WHERE patient_id = %s
            """
            r = dictfetchall(cur, sql, (patient_id,))
            cur.close()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return r
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error getting all clinicians: ", sys.exc_info()[0])
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def check_invitation_token_validity(token):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                SELECT *
                FROM tingleserver."Account_Invitation"
                WHERE token=%s
            """
            cur.execute(sql, (token,))
            r = dictfetchone(cur, sql, (token,))
            cur.close()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return r
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't get account invitation")
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def check_email_in_account_invitation(email):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                SELECT *
                FROM tingleserver."Account_Invitation"
                WHERE ac_email=%s
            """
            cur.execute(sql, (email,))
            r = dictfetchone(cur, sql, (email,))
            cur.close()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return r
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't get account invitation")
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def update_role_in_account_invitation(email, role):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                UPDATE tingleserver."Account_Invitation"
                SET role=%s
                WHERE ac_email=%s
                RETURNING token, role;
            """
            r = dictfetchone(cur, sql, (role, email,))
            conn.commit()
            cur.close()                     # Close the cursor
            conn.close()                    # Close the connection to the db
            return r
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Error: can't update account invitation")
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def add_account_invitation(token, email, role):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                INSERT INTO tingleserver."Account_Invitation" (token, ac_email, role)
                VALUES(%s, %s, %s);
            """
            cur.execute(sql, (token, email, role))
            conn.commit()
            cur.close()
            return email
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error inserting invitation: ", sys.exc_info()[0])
            conn.rollback()
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None

def delete_account_invitation(token, email):
    conn = database_connect()
    if conn:
        cur = conn.cursor()
        try:
            sql = """
                DELETE FROM tingleserver."Account_Invitation"
                WHERE ac_email=%s
                AND token=%s;
            """
            cur.execute(sql, (email, token))
            conn.commit()
            cur.close()
            return email
        except:
            # If there were any errors, return a NULL row printing an error to the debug
            print("Unexpected error inserting invitation: ", sys.exc_info()[0])
            conn.rollback()
            raise
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
    return None