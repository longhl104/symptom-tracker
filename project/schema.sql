DROP SCHEMA IF EXISTS accountserver CASCADE;
CREATE SCHEMA accountserver;
SET search_path TO 'accountserver';

DROP TABLE IF EXISTS Account CASCADE;
DROP TABLE IF EXISTS Patient CASCADE;
DROP TABLE IF EXISTS Clinician CASCADE;
DROP TABLE IF EXISTS Researcher CASCADE;

CREATE TABLE AccountType (
    account_type_id SERIAL PRIMARY KEY,
    account_type_name VARCHAR(100) NOT NULL
);

CREATE TABLE Account(
    account_id SERIAL PRIMARY KEY,
    account_type_id INTEGER REFERENCES AccountType(account_type_id) NOT NULL,
    ac_username TEXT NOT NULL,
    ac_password TEXT NOT NULL,
    ac_first_name TEXT NOT NULL,
    ac_last_name TEXT NOT NULL,
    ac_email TEXT,
    ac_age SMALLINT,
    ac_gender TEXT,
    ac_phone INTEGER NOT NULL,
    ac_admin SMALLINT DEFAULT 0
);

CREATE TABLE Clinician (
    clinician_id SERIAL UNIQUE REFERENCES Account(account_id),
    professions TEXT
);

CREATE TABLE Patient(
    patient_id SERIAL REFERENCES Account(account_id),
    symptoms_tracking TEXT,
    pt_clinician INTEGER NOT NULL REFERENCES Clinician(clinician_id)
);

CREATE TABLE Researcher (
    researcher_id SERIAL REFERENCES Account(account_id),
    research_assigned TEXT
);

CREATE OR REPLACE FUNCTION accountserver.addpatient(
    type TEXT,
    username TEXT,
    password TEXT,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    age SMALLINT,
    gender TEXT,
    phone INTEGER,
    assignedclinician INTEGER,
    symptoms TEXT)
RETURNS int AS
$BODY$
    WITH ins1 AS (
        INSERT INTO accountserver.Patient (pt_clinician, symptoms_tracking)
        VALUES (assignedclinician, symptoms)
        RETURNING patient_id
        ), ins2 AS (
            INSERT INTO accountserver.Account (ac_username, ac_password, ac_first_name, ac_last_name, ac_email, ac_age, ac_gender, ac_phone)
            VALUES (username, password, firstname, lastname, email, age, gender, phone)
            RETURNING account_id
        ), ins3 AS (
            INSERT INTO accountserver.AccountType (account_type_name)
            VALUES (type)
        )
		SELECT patient_id FROM accountserver.Patient;
$BODY$
LANGUAGE sql;