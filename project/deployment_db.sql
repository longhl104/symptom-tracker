--
-- PostgreSQL database dump
--

-- Dumped from database version 13.0
-- Dumped by pg_dump version 13.0

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

--
-- Name: tingleserver; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA tingleserver;


--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

-- CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: -
--

-- COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


--
-- Name: add_account(character varying, character varying, character varying, date, character varying, character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: tingleserver; Owner: -
--

CREATE FUNCTION tingleserver.add_account(first_name character varying, last_name character varying, gender character varying, dob date, mobile character varying, email character varying, password_hash character varying, user_role character varying, consent character varying) RETURNS smallint
    LANGUAGE plpgsql
    AS $$
DECLARE account_id smallint;
BEGIN
INSERT INTO tingleserver."Account" (ac_email,
ac_password,
ac_firstname,
ac_lastname,
ac_dob,
ac_gender,
ac_phone,
ac_type
  )
   	VALUES(email, password_hash, first_name, last_name, dob, gender, mobile, user_role);

SELECT ac_id INTO account_id
FROM tingleserver."Account"
WHERE ac_email = email;
IF LOWER(user_role) = 'patient' THEN
INSERT INTO tingleserver."Patient" (ac_id, consent) VALUES(account_id, consent);
ELSIF LOWER(user_role) = 'clinician' THEN
INSERT INTO tingleserver."Clinician" (ac_id) VALUES(account_id);
ELSIF LOWER(user_role) = 'researcher' THEN
INSERT INTO tingleserver."Researcher" (ac_id) VALUES(account_id);
ELSIF LOWER(user_role) = 'admin' THEN
INSERT INTO tingleserver."Admin" (ac_id) VALUES(account_id);
END IF;
RETURN account_id;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Account; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Account" (
    ac_id smallint NOT NULL,
    ac_email character varying(255) NOT NULL,
    ac_password character varying(255) NOT NULL,
    ac_firstname character varying(255) NOT NULL,
    ac_lastname character varying(255) NOT NULL,
    ac_gender character varying(6),
    ac_phone character varying(20),
    ac_type character varying(50),
    ac_dob date
);


--
-- Name: Account_Invitation; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Account_Invitation" (
    token character varying(255) NOT NULL,
    ac_email character varying(255) NOT NULL,
    role character varying(20) NOT NULL
);


--
-- Name: Account_ac_id_seq; Type: SEQUENCE; Schema: tingleserver; Owner: -
--

CREATE SEQUENCE tingleserver."Account_ac_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Account_ac_id_seq; Type: SEQUENCE OWNED BY; Schema: tingleserver; Owner: -
--

ALTER SEQUENCE tingleserver."Account_ac_id_seq" OWNED BY tingleserver."Account".ac_id;


--
-- Name: Admin; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Admin" (
    ac_id smallint NOT NULL
);


--
-- Name: Clinician; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Clinician" (
    ac_id smallint NOT NULL
);


--
-- Name: Forgot_password; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Forgot_password" (
    key character(24) NOT NULL,
    ac_email character varying(255)
);


--
-- Name: Patient; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Patient" (
    ac_id smallint NOT NULL,
    consent character varying(3)
);


--
-- Name: Patient_Clinician; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Patient_Clinician" (
    patient_id smallint NOT NULL,
    clinician_id smallint NOT NULL
);


--
-- Name: Patient_Receives_Questionnaire; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Patient_Receives_Questionnaire" (
    ac_id smallint NOT NULL,
    questionnaire_id smallint NOT NULL,
    opened boolean DEFAULT false NOT NULL,
    completed boolean DEFAULT false NOT NULL
);


--
-- Name: Patient_Receives_Treatment; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Patient_Receives_Treatment" (
    patient_id smallint NOT NULL,
    treatment_id smallint NOT NULL
);


--
-- Name: Questionnaire; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Questionnaire" (
    name character varying(255) NOT NULL,
    link character varying(255) NOT NULL,
    end_date date NOT NULL,
    id integer NOT NULL
);


--
-- Name: Questionnaire_id_seq; Type: SEQUENCE; Schema: tingleserver; Owner: -
--

CREATE SEQUENCE tingleserver."Questionnaire_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Questionnaire_id_seq; Type: SEQUENCE OWNED BY; Schema: tingleserver; Owner: -
--

ALTER SEQUENCE tingleserver."Questionnaire_id_seq" OWNED BY tingleserver."Questionnaire".id;


--
-- Name: Researcher; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Researcher" (
    ac_id smallint
);


--
-- Name: Symptom; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Symptom" (
    symptom_id integer NOT NULL,
    patient_username character varying(255) NOT NULL,
    severity character varying(20),
    recorded_date date,
    symptom_name character varying(255) NOT NULL,
    notes character varying(255),
    location character varying(255),
    occurence character varying(12)
);


--
-- Name: Symptom_symptom_id_seq; Type: SEQUENCE; Schema: tingleserver; Owner: -
--

CREATE SEQUENCE tingleserver."Symptom_symptom_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Symptom_symptom_id_seq; Type: SEQUENCE OWNED BY; Schema: tingleserver; Owner: -
--

ALTER SEQUENCE tingleserver."Symptom_symptom_id_seq" OWNED BY tingleserver."Symptom".symptom_id;


--
-- Name: Treatment; Type: TABLE; Schema: tingleserver; Owner: -
--

CREATE TABLE tingleserver."Treatment" (
    treatment_id smallint NOT NULL,
    treatment_name character varying(255) NOT NULL
);


--
-- Name: Treatment_treatment_id_seq; Type: SEQUENCE; Schema: tingleserver; Owner: -
--

CREATE SEQUENCE tingleserver."Treatment_treatment_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Treatment_treatment_id_seq; Type: SEQUENCE OWNED BY; Schema: tingleserver; Owner: -
--

ALTER SEQUENCE tingleserver."Treatment_treatment_id_seq" OWNED BY tingleserver."Treatment".treatment_id;


--
-- Name: Account ac_id; Type: DEFAULT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Account" ALTER COLUMN ac_id SET DEFAULT nextval('tingleserver."Account_ac_id_seq"'::regclass);


--
-- Name: Questionnaire id; Type: DEFAULT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Questionnaire" ALTER COLUMN id SET DEFAULT nextval('tingleserver."Questionnaire_id_seq"'::regclass);


--
-- Name: Symptom symptom_id; Type: DEFAULT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Symptom" ALTER COLUMN symptom_id SET DEFAULT nextval('tingleserver."Symptom_symptom_id_seq"'::regclass);


--
-- Name: Treatment treatment_id; Type: DEFAULT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Treatment" ALTER COLUMN treatment_id SET DEFAULT nextval('tingleserver."Treatment_treatment_id_seq"'::regclass);


--
-- Data for Name: Account; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Account" (ac_id, ac_email, ac_password, ac_firstname, ac_lastname, ac_gender, ac_phone, ac_type, ac_dob) FROM stdin;
56	patient@test.com	pbkdf2:sha256:150000$fDjsnkNU$bef2af8fb99ba74eb24525a68133a366a53f2a8169ef2eb0de19b05065bea3be	Jane	Doe	Female	0412345678	patient	\N
57	clinician@test.com	pbkdf2:sha256:150000$y4Yk3EIp$70ca6e06f8319728d9a4673d20494657744a973ba1691dd97f160346d1dccda3	John	Doe	Male	0421312324	clinician	\N
58	researcher@test.com	pbkdf2:sha256:150000$DSr6jvtl$ccc61a69ae3e610118e5fae80c39e859c3889495e856e4bcfd31d615f6a3d501	Jake	Doe	Male	0423212389	researcher	\N
61	admin@test.com	pbkdf2:sha256:150000$WT5eNrHI$fabc60fc188bcebf165644501d540f27c33998ff5da2f381e743b9097462463e	Admin	Account	Female	0123456789	admin	\N
\.


--
-- Data for Name: Account_Invitation; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Account_Invitation" (token, ac_email, role) FROM stdin;
\.


--
-- Data for Name: Admin; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Admin" (ac_id) FROM stdin;
61
\.


--
-- Data for Name: Clinician; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Clinician" (ac_id) FROM stdin;
57
\.


--
-- Data for Name: Forgot_password; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Forgot_password" (key, ac_email) FROM stdin;
\.


--
-- Data for Name: Patient; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Patient" (ac_id, consent) FROM stdin;
56	yes
\.


--
-- Data for Name: Patient_Clinician; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Patient_Clinician" (patient_id, clinician_id) FROM stdin;
\.


--
-- Data for Name: Patient_Receives_Questionnaire; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Patient_Receives_Questionnaire" (ac_id, questionnaire_id, opened, completed) FROM stdin;
\.


--
-- Data for Name: Patient_Receives_Treatment; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Patient_Receives_Treatment" (patient_id, treatment_id) FROM stdin;
56	1
\.


--
-- Data for Name: Questionnaire; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Questionnaire" (name, link, end_date, id) FROM stdin;
\.


--
-- Data for Name: Researcher; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Researcher" (ac_id) FROM stdin;
58
\.


--
-- Data for Name: Symptom; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Symptom" (symptom_id, patient_username, severity, recorded_date, symptom_name, notes, location, occurence) FROM stdin;
15	patient@test.com	Somewhat	2020-10-14	Tingling		Hands	Daytime
13	patient@test.com	Quite a bit	2020-10-08	Numbness		Hands	Daytime
14	patient@test.com	A little bit	2020-10-13	Pain		Legs	Morning
17	patient@test.com	A little bit	2020-11-16	Test222	ASDASDASD	Test1111	Night-time
\.


--
-- Data for Name: Treatment; Type: TABLE DATA; Schema: tingleserver; Owner: -
--

COPY tingleserver."Treatment" (treatment_id, treatment_name) FROM stdin;
1	Oxaliplatin (Eloxatin, Oxalatin, Oxaliccord, Xalox, FOLFOX, XELOX)
2	Cisplatin (Cisplatinum, Platinol)
3	Carboplatin (Carbaccord)
4	Paclitaxel (Taxol, Anzatax, Plaxel, Abraxane)
5	Docetaxel (Taxotere, Dotax, Oncotaxel)
6	Cabazitaxel (Jevtana)
7	Vincristine
8	Vinblastine
9	Vinorelbine (Navelbine)
10	Thalidomide (Thalomid)
11	Bortezomib (Velcade)
12	Lenalidomide (Revlimid)
13	Pomalidomide (Pomalyst)
14	Eribulin (Halaven)
\.


--
-- Name: Account_ac_id_seq; Type: SEQUENCE SET; Schema: tingleserver; Owner: -
--

SELECT pg_catalog.setval('tingleserver."Account_ac_id_seq"', 82, true);


--
-- Name: Questionnaire_id_seq; Type: SEQUENCE SET; Schema: tingleserver; Owner: -
--

SELECT pg_catalog.setval('tingleserver."Questionnaire_id_seq"', 62, true);


--
-- Name: Symptom_symptom_id_seq; Type: SEQUENCE SET; Schema: tingleserver; Owner: -
--

SELECT pg_catalog.setval('tingleserver."Symptom_symptom_id_seq"', 17, true);


--
-- Name: Treatment_treatment_id_seq; Type: SEQUENCE SET; Schema: tingleserver; Owner: -
--

SELECT pg_catalog.setval('tingleserver."Treatment_treatment_id_seq"', 1, false);


--
-- Name: Account_Invitation Account_Invitation_pkey; Type: CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Account_Invitation"
    ADD CONSTRAINT "Account_Invitation_pkey" PRIMARY KEY (token);


--
-- Name: Account Account_pkey; Type: CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "Account_pkey" PRIMARY KEY (ac_id);


--
-- Name: Admin Admin_ac_id_key; Type: CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT "Admin_ac_id_key" UNIQUE (ac_id);


--
-- Name: Clinician Clinician_ac_id_key; Type: CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_key" UNIQUE (ac_id);


--
-- Name: Patient Patient_ac_id_key; Type: CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_key" UNIQUE (ac_id);


--
-- Name: Researcher Researcher_ac_id_key; Type: CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Researcher"
    ADD CONSTRAINT "Researcher_ac_id_key" UNIQUE (ac_id);


--
-- Name: Treatment Treatment_pkey; Type: CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Treatment"
    ADD CONSTRAINT "Treatment_pkey" PRIMARY KEY (treatment_id);


--
-- Name: Account ac_email; Type: CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT ac_email UNIQUE (ac_email);


--
-- Name: Questionnaire id; Type: CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Questionnaire"
    ADD CONSTRAINT id PRIMARY KEY (id);


--
-- Name: Forgot_password key; Type: CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Forgot_password"
    ADD CONSTRAINT key PRIMARY KEY (key);


--
-- Name: Patient_Clinician patient_clinician_unique_key; Type: CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT patient_clinician_unique_key UNIQUE (patient_id, clinician_id);


--
-- Name: Symptom symptom_id; Type: CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT symptom_id PRIMARY KEY (symptom_id);


--
-- Name: fki_id_key_ac_email_fkey; Type: INDEX; Schema: tingleserver; Owner: -
--

CREATE INDEX fki_id_key_ac_email_fkey ON tingleserver."Forgot_password" USING btree (ac_email);


--
-- Name: Admin Admin_ac_id_fkey; Type: FK CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT "Admin_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;


--
-- Name: Clinician Clinician_ac_id_fkey; Type: FK CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;


--
-- Name: Patient_Receives_Treatment Patient_Receives_Treatment_patient_id_fkey; Type: FK CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey" FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: Patient_Receives_Treatment Patient_Receives_Treatment_treatment_id_fkey; Type: FK CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey" FOREIGN KEY (treatment_id) REFERENCES tingleserver."Treatment"(treatment_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: Patient Patient_ac_id_fkey; Type: FK CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED NOT VALID;


--
-- Name: Researcher Researcher_ac_id_fkey; Type: FK CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Researcher"
    ADD CONSTRAINT "Researcher_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id);


--
-- Name: Patient_Clinician clinician_id_fk; Type: FK CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT clinician_id_fk FOREIGN KEY (clinician_id) REFERENCES tingleserver."Clinician"(ac_id);


--
-- Name: Forgot_password key_ac_email_fkey; Type: FK CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Forgot_password"
    ADD CONSTRAINT key_ac_email_fkey FOREIGN KEY (ac_email) REFERENCES tingleserver."Account"(ac_email);


--
-- Name: Patient_Receives_Questionnaire patient_fk; Type: FK CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Patient_Receives_Questionnaire"
    ADD CONSTRAINT patient_fk FOREIGN KEY (ac_id) REFERENCES tingleserver."Patient"(ac_id);


--
-- Name: Patient_Clinician patient_id_fk; Type: FK CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT patient_id_fk FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id);


--
-- Name: Patient_Receives_Questionnaire questionnaire_fk; Type: FK CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Patient_Receives_Questionnaire"
    ADD CONSTRAINT questionnaire_fk FOREIGN KEY (questionnaire_id) REFERENCES tingleserver."Questionnaire"(id);


--
-- Name: Symptom username; Type: FK CONSTRAINT; Schema: tingleserver; Owner: -
--

ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT username FOREIGN KEY (patient_username) REFERENCES tingleserver."Account"(ac_email) NOT VALID;


--
-- PostgreSQL database dump complete
--

