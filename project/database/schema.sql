drop schema if exists accountserver cascade;
create schema accountserver;
set search_path to 'accountserver';

DROP TABLE IF EXISTS Account CASCADE;
DROP TABLE IF EXISTS Patient CASCADE;
DROP TABLE IF EXISTS Clinician CASCADE;
DROP TABLE IF EXISTS Researcher CASCADE;

CREATE TABLE AccountType (
    account_type_id SERIAL PRIMARY KEY,
    account_type_name VARCHAR(100) NOT NULL
)

CREATE TABLE Account(
    account_id SERIAL PRIMARY KEY,
    account_type_id INTEGER REFERENCES AccountType(account_type_id) NOT NULL,
    ac_username TEXT NOT NULL,
    ac_password TEXT NOT NULL,
    ac_first_name TEXT NOT NULL,
    ac_last_name TEXT NOT NULL,
    ac_email TEXT,
    ac_dob DATE,
    ac_gender TEXT,
    ac_phone INTEGER NOT NULL,
    ac_admin SMALLINT DEFAULT 0
);

CREATE TABLE Patient(
    patient_id SERIAL REFERENCES Account(account_id),
    symptoms_tracking TEXT,
    pt_clinician INTEGER NOT NULL REFERENCES Clinician(id)
);

CREATE TABLE Clinician (
    clinician_id SERIAL REFERENCES Account(account_id),
    professions TEXT
);

CREATE TABLE Researcher (
    researcher_id SERIAL REFERENCES Account(account_id),
    research_assigned TEXT
);

CREATE OR REPLACE FUNCTION accountserver.addpatient(
    type TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT,
    age SMALLINT,
    gender TEXT,
    phone INTEGER NOT NULL,
    assignedclinician INTEGER NOT NULL,
    symptoms)
RETURNS int AS
$ADD$
    WITH ins1 AS (
        INSERT INTO accountserver.Patient (patient_id, pt_clinician, symptoms_tracking)
        VALUES (assignedclinician, symptoms)
        RETURNING patient_id
        ) ins2 AS (
            INSERT INTO accountserver.Account (ac_username, ac_password, ac_firstname, ac_lastname, ac_email, ac_dob, ac_gender, ac_phone)
            VALUES (username, password, firstname, lastname, email, dob, gender, phone)
            RETURNING account_id
        ) ins3 AS (
            INSERT INTO accountserver.AccountType (account_type_name)
            VALUES (type)
            SELECT account_id FROM ins2
        )
$ADD$
LANGUAGE sql;