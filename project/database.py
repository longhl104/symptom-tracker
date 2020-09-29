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
    config.read('sample-config.ini')
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
    if(conn is None):
        return None
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
def get_UserID(email, password):
    """
        - get UserID from db
        - True => return the user data
        - False => return None
    """
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = """
            SELECT tingleserver."account_id"
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
        print("Invalid details")
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


def get_all_treatments():
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = """
            SELECT tingleserver."Treatment".treatment_name FROM tingleserver."Treatment"
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


def add_patient(firstname, lastname, gender, age, mobile, treatment, email, password, consent):
    print(firstname, lastname, gender, age, mobile,
          treatment, email, password, consent)
    # Consent to exposing personal data to research should be optional
    # if consent == 'no':
    #     return None

    # Catching boundary cases
    if len(firstname) > 255:
        print("First name entered is greater than maximum length of 255.")
        raise
    if len(lastname) > 255:
        print("Last name entered is greater than maximum length of 255.")
        raise
    elif len(password) > 20:
        print("Password entered is greater than maximum length of 20.")
        raise
    elif len(email) > 255:
        print("Email entered is greater than maximum length of 255.")
        raise
    elif len(mobile) > 20:
        print("Phone number entered is greater than maximum length of 20.")
        raise

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
            SELECT tingleserver.add_patient(%s,%s,%s,%s,%s,%s,%s);
        """
        cur.execute(sql, (firstname, lastname, gender, age,
                          mobile, email, password))
        conn.commit()
        patient_id = cur.fetchone()[0]

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
        conn.commit()                     # Close the cursor
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

def record_symptom(email,symptom,severity,date,time):
    print(email,symptom,severity,date,time)

    if date is None or date == '':     #if invalid date exist *to-do*
        print('Invalid date entered.')
        raise
    elif time is None or time == '':
        print("Invalid time entered.")
        raise
    elif email is None or email == '':
        print("User not found.")
        raise

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
            SELECT tingleserver.record_symptom(%s,%s,%s,%s,%s,);
        """
        cur.execute(sql, (email,symptom,severity,date,time))
        conn.commit()
        patient_id = cur.fetchone()[0]


        cur.close()
        conn.commit()                     # Close the cursor
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
