SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP SCHEMA IF EXISTS tingleserver CASCADE;
CREATE SCHEMA tingleserver;
SET search_path TO 'tingleserver';

ALTER SCHEMA tingleserver OWNER TO postgres;
SET default_tablespace = '';
SET default_table_access_method = heap;

DROP TABLE IF EXISTS Account CASCADE;
DROP TABLE IF EXISTS Patient CASCADE;
DROP TABLE IF EXISTS Clinician CASCADE;
DROP TABLE IF EXISTS Researcher CASCADE;

CREATE TABLE AccountType (
    account_type_id SERIAL PRIMARY KEY,
    account_type_name VARCHAR(100) NOT NULL
);

ALTER TABLE tingleserver."AccountType" OWNER TO postgres;

CREATE TABLE Account(
    account_id SERIAL PRIMARY KEY,
    account_type_id INTEGER REFERENCES AccountType(account_type_id) NOT NULL,
    ac_password TEXT NOT NULL,
    ac_first_name TEXT NOT NULL,
    ac_last_name TEXT NOT NULL,
    ac_email TEXT,
    ac_age SMALLINT,
    ac_gender TEXT,
    ac_phone INTEGER NOT NULL,
    ac_admin SMALLINT DEFAULT 0
);

ALTER TABLE ONLY tingleserver."Account"
	ADD CONSTRAINT ac_email UNIQUE (username);
COMMENT ON CONSTRAINT ac_email ON tingleserver."Account" IS 'Email must be unique';

ALTER TABLE tingleserver."Account" OWNER TO postgres;

CREATE TABLE Clinician (
    clinician_id SERIAL UNIQUE REFERENCES Account(account_id),
    professions TEXT
);

ALTER TABLE tingleserver."Clinician" OWNER TO postgres;

CREATE TABLE Patient(
    patient_id SERIAL REFERENCES Account(account_id),
    symptoms_tracking TEXT,
    pt_clinician INTEGER NOT NULL REFERENCES Clinician(clinician_id)
);

ALTER TABLE tingleserver."Patient" OWNER TO postgres;

CREATE TABLE Researcher (
    researcher_id SERIAL REFERENCES Account(account_id),
    research_assigned TEXT
);

ALTER TABLE tingleserver."Researcher" OWNER TO postgres;

CREATE OR REPLACE FUNCTION tingleserver.addpatient(
    type TEXT,
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
        INSERT INTO tingleserver.Patient (pt_clinician, symptoms_tracking)
        VALUES (assignedclinician, symptoms)
        RETURNING patient_id
        ), ins2 AS (
            INSERT INTO tingleserver.Account (ac_password, ac_first_name, ac_last_name, ac_email, ac_age, ac_gender, ac_phone)
            VALUES (password, firstname, lastname, email, age, gender, phone)
            RETURNING account_id
        ), ins3 AS (
            INSERT INTO tingleserver.AccountType (account_type_name)
            VALUES (type)
        )
		SELECT patient_id FROM tingleserver.Patient;
$BODY$
LANGUAGE sql;