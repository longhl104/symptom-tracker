--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.4

-- Started on 2020-09-21 16:29:41

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
-- TOC entry 7 (class 2615 OID 17665)
-- Name: tingleserver; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tingleserver;


ALTER SCHEMA tingleserver OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 246 (class 1259 OID 17666)
-- Name: Account; Type: TABLE; Schema: tingleserver; Owner: postgres
--

CREATE TABLE tingleserver."Account" (
    "accountID" smallint NOT NULL,
    "firstName" character varying(255)[] NOT NULL,
    "lastName" character varying(255)[] NOT NULL,
    username character varying(20)[] NOT NULL,
    password character varying(20)[] NOT NULL,
    age smallint NOT NULL,
    email character varying(255)[] NOT NULL,
    phonenumber character varying(20)[] NOT NULL,
    gender smallint NOT NULL
);


ALTER TABLE tingleserver."Account" OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 17669)
-- Name: Account_accountID_seq; Type: SEQUENCE; Schema: tingleserver; Owner: postgres
--

CREATE SEQUENCE tingleserver."Account_accountID_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tingleserver."Account_accountID_seq" OWNER TO postgres;

--
-- TOC entry 2984 (class 0 OID 0)
-- Dependencies: 247
-- Name: Account_accountID_seq; Type: SEQUENCE OWNED BY; Schema: tingleserver; Owner: postgres
--

ALTER SEQUENCE tingleserver."Account_accountID_seq" OWNED BY tingleserver."Account"."accountID";


--
-- TOC entry 249 (class 1259 OID 17689)
-- Name: Clinician; Type: TABLE; Schema: tingleserver; Owner: postgres
--

CREATE TABLE tingleserver."Clinician" (
    profession character varying(255)[] NOT NULL
)
INHERITS (tingleserver."Account");


ALTER TABLE tingleserver."Clinician" OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 17789)
-- Name: Clinician_looks_after_Patient; Type: TABLE; Schema: tingleserver; Owner: postgres
--

CREATE TABLE tingleserver."Clinician_looks_after_Patient" (
    "patientID" smallint NOT NULL,
    "clinicianID" smallint NOT NULL
);


ALTER TABLE tingleserver."Clinician_looks_after_Patient" OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 17682)
-- Name: Patient; Type: TABLE; Schema: tingleserver; Owner: postgres
--

CREATE TABLE tingleserver."Patient" (
)
INHERITS (tingleserver."Account");


ALTER TABLE tingleserver."Patient" OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 17696)
-- Name: Researcher; Type: TABLE; Schema: tingleserver; Owner: postgres
--

CREATE TABLE tingleserver."Researcher" (
)
INHERITS (tingleserver."Account");


ALTER TABLE tingleserver."Researcher" OWNER TO postgres;

--
-- TOC entry 2833 (class 2604 OID 17671)
-- Name: Account accountID; Type: DEFAULT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Account" ALTER COLUMN "accountID" SET DEFAULT nextval('tingleserver."Account_accountID_seq"'::regclass);


--
-- TOC entry 2835 (class 2604 OID 17692)
-- Name: Clinician accountID; Type: DEFAULT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Clinician" ALTER COLUMN "accountID" SET DEFAULT nextval('tingleserver."Account_accountID_seq"'::regclass);


--
-- TOC entry 2834 (class 2604 OID 17685)
-- Name: Patient accountID; Type: DEFAULT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Patient" ALTER COLUMN "accountID" SET DEFAULT nextval('tingleserver."Account_accountID_seq"'::regclass);


--
-- TOC entry 2836 (class 2604 OID 17699)
-- Name: Researcher accountID; Type: DEFAULT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Researcher" ALTER COLUMN "accountID" SET DEFAULT nextval('tingleserver."Account_accountID_seq"'::regclass);


--
-- TOC entry 2838 (class 2606 OID 17679)
-- Name: Account Account_pkey; Type: CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "Account_pkey" PRIMARY KEY ("accountID");


--
-- TOC entry 2846 (class 2606 OID 17788)
-- Name: Clinician Clinician_pkey; Type: CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_pkey" PRIMARY KEY ("accountID");


--
-- TOC entry 2850 (class 2606 OID 17793)
-- Name: Clinician_looks_after_Patient PK_clinicianID_patientID; Type: CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Clinician_looks_after_Patient"
    ADD CONSTRAINT "PK_clinicianID_patientID" PRIMARY KEY ("patientID", "clinicianID");


--
-- TOC entry 2844 (class 2606 OID 17800)
-- Name: Patient Patient_pkey; Type: CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_pkey" PRIMARY KEY ("accountID");


--
-- TOC entry 2848 (class 2606 OID 17807)
-- Name: Researcher Researcher_pkey; Type: CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Researcher"
    ADD CONSTRAINT "Researcher_pkey" PRIMARY KEY ("accountID");


--
-- TOC entry 2840 (class 2606 OID 17756)
-- Name: Account uc_accountID; Type: CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "uc_accountID" UNIQUE ("accountID");


--
-- TOC entry 2842 (class 2606 OID 17681)
-- Name: Account uc_username; Type: CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT uc_username UNIQUE (username);


--
-- TOC entry 2985 (class 0 OID 0)
-- Dependencies: 2842
-- Name: CONSTRAINT uc_username ON "Account"; Type: COMMENT; Schema: tingleserver; Owner: postgres
--

COMMENT ON CONSTRAINT uc_username ON tingleserver."Account" IS 'Username must be unique';


--
-- TOC entry 2851 (class 2606 OID 17794)
-- Name: Clinician_looks_after_Patient FK_Clinician_accountID; Type: FK CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Clinician_looks_after_Patient"
    ADD CONSTRAINT "FK_Clinician_accountID" FOREIGN KEY ("clinicianID") REFERENCES tingleserver."Clinician"("accountID");


--
-- TOC entry 2852 (class 2606 OID 17801)
-- Name: Clinician_looks_after_Patient FK_Patient_accountID; Type: FK CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Clinician_looks_after_Patient"
    ADD CONSTRAINT "FK_Patient_accountID" FOREIGN KEY ("patientID") REFERENCES tingleserver."Patient"("accountID") NOT VALID;


-- Completed on 2020-09-21 16:29:41

--
-- PostgreSQL database dump complete
--

