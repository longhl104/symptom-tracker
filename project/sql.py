import sqlite3


class SQLDatabase():

    def __init__(self, database_arg=":memory:"):
        self.conn = sqlite3.connect(database_arg,check_same_thread=False)
        self.cur = self.conn.cursor()


    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
                return out

    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------


    def database_setup(self, admin_password='admin'):

        self.execute('''
            DROP TABLE IF EXISTS Account;
            DROP TABLE IF EXISTS Patient;
            DROP TABLE IF EXISTS Clinician;
            DROP TABLE IF EXISTS Researcher;
        ''')
        self.commit()

        # Create the users table
        self.execute('''
        CREATE TABLE Account(
            Accountid INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            FirstName TEXT,
            LastName TEXT,
            Email TEXT,
            Age INTEGER,
            Gender TEXT,
            Phone INTEGER,
            AccountType TEXT,
            admin INTEGER DEFAULT 0
        );

        CREATE TABLE Patient(
            id INTEGER FOREIGN KEY REFERENCES Account(Accountid),
            SympotomsTracking TEXT,
            Clinician INTEGER NOT NULL REFERENCES Clinician(id)
        );

        CREATE TABLE Clinician (
            id INTEGER FOREIGN KEY REFERENCES Account(Accountid),
            Professions TEXT
        );
        CREATE TABLE Researcher (
            id INTEGER FOREIGN KEY REFERENCES Account(Accountid),
            researchs TEXT
        );
        ''')

        self.commit()

           # Add our admin user
        self.add_user('admin', admin_password, admin=1)
        self.add_user('boss', admin_password, admin=1)





    #-----------------------------------------------------------------------------
    # User handling(need more editing)
    #-----------------------------------------------------------------------------

    def add_user(self, username, password, admin=0):

        sql_cmd = """
                INSERT INTO Users(username,password,admin)
                VALUES(?,?,?)
            """
        tup = (username, password, admin)
        self.cur.execute(sql_cmd,tup)
        self.commit()
        # If our aquery returns
        if self.cur.fetchone():
            print("successz")
        return True


    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT 1
                FROM Users
                WHERE username = ? AND password = ?
            """

        # If our aquery returns
        self.cur.execute(sql_query,(username,password))
        self.commit()
        if self.cur.fetchall():
            return True
        else:
            return False

    def check_exist(self, username):

        sql_query = """
                SELECT 1
                FROM Account
                WHERE username = ?
            """

        # If our aquery returns
        self.cur.execute(sql_query,(username,))
        self.commit()
        if self.cur.fetchall():
            return True
        else:
            return False
    def user_show(self, username, password):
        sql_query = """
                SELECT *
                FROM Account

            """.format(username=username, password=password)

        # If our aquery returns
        self.execute(sql_query)
        self.commit()
        if self.cur.fetchall():
            return True
        else:
            return False

    def user_show_all(self):
        sql_query = """
                SELECT *
                FROM Account

            """

        # If our aquery returns
        self.execute(sql_query)
        self.commit()
        return self.cur.fetchall()



    def check_user_exists(self,name):
        sql_query = """
            SELECT *
            FROM Account
            WHERE username=?
        """
        self.cur.execute(sql_query,(name,))
        self.commit()
        if len(self.cur.fetchall()) > 0:
            return True
        else:
            return False
