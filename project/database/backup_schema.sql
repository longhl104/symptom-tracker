--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.4

-- Started on 2020-09-25 12:28:27

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
-- TOC entry 8 (class 2615 OID 17808)
-- Name: tingleserver; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tingleserver;


ALTER SCHEMA tingleserver OWNER TO postgres;

--
-- TOC entry 224 (class 1255 OID 34279)
-- Name: add_patient(character varying, character varying, character varying, smallint, character varying, character varying, character varying); Type: FUNCTION; Schema: tingleserver; Owner: postgres
--

CREATE FUNCTION tingleserver.add_patient(firstname character varying, lastname character varying, gender character varying, age smallint, mobile character varying, email character varying, password character varying) RETURNS smallint
    LANGUAGE plpgsql
    AS $$
DECLARE
	v_patient_id smallint;
begin
	insert into tingleserver."Account" (ac_email,
										ac_password,
										ac_firstname,
										ac_lastname,
										ac_age,
										ac_gender,
										ac_phone
									   )
   		values (email, password, firstname, lastname, age, gender, mobile);
		
	select max(ac_id) into v_patient_id
		from tingleserver."Account";
		
	insert into tingleserver."Patient" (ac_id) values (v_patient_id);
		
	return v_patient_id;
end;
$$;


ALTER FUNCTION tingleserver.add_patient(firstname character varying, lastname character varying, gender character varying, age smallint, mobile character varying, email character varying, password character varying) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 210 (class 1259 OID 26069)
-- Name: Account; Type: TABLE; Schema: tingleserver; Owner: postgres
--

CREATE TABLE tingleserver."Account" (
    ac_id smallint NOT NULL,
    ac_email character varying(255) NOT NULL,
    ac_password character varying(20) NOT NULL,
    ac_firstname character varying(255) NOT NULL,
    ac_lastname character varying(255) NOT NULL,
    ac_age smallint,
    ac_gender character varying(6) NOT NULL,
    ac_phone character varying(20)
);


ALTER TABLE tingleserver."Account" OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 26067)
-- Name: Account_ac_id_seq; Type: SEQUENCE; Schema: tingleserver; Owner: postgres
--

CREATE SEQUENCE tingleserver."Account_ac_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tingleserver."Account_ac_id_seq" OWNER TO postgres;

--
-- TOC entry 2862 (class 0 OID 0)
-- Dependencies: 209
-- Name: Account_ac_id_seq; Type: SEQUENCE OWNED BY; Schema: tingleserver; Owner: postgres
--

ALTER SEQUENCE tingleserver."Account_ac_id_seq" OWNED BY tingleserver."Account".ac_id;


--
-- TOC entry 206 (class 1259 OID 26032)
-- Name: Admin; Type: TABLE; Schema: tingleserver; Owner: postgres
--

CREATE TABLE tingleserver."Admin" (
    ac_id smallint NOT NULL
);


ALTER TABLE tingleserver."Admin" OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 26018)
-- Name: Clinician; Type: TABLE; Schema: tingleserver; Owner: postgres
--

CREATE TABLE tingleserver."Clinician" (
    ac_id smallint NOT NULL
);


ALTER TABLE tingleserver."Clinician" OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 26011)
-- Name: Patient; Type: TABLE; Schema: tingleserver; Owner: postgres
--

CREATE TABLE tingleserver."Patient" (
    ac_id smallint NOT NULL
);


ALTER TABLE tingleserver."Patient" OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 34240)
-- Name: Patient_Receives_Treatment; Type: TABLE; Schema: tingleserver; Owner: postgres
--

CREATE TABLE tingleserver."Patient_Receives_Treatment" (
    patient_id smallint NOT NULL,
    treatment_id smallint NOT NULL
);


ALTER TABLE tingleserver."Patient_Receives_Treatment" OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 26041)
-- Name: Treatment; Type: TABLE; Schema: tingleserver; Owner: postgres
--

CREATE TABLE tingleserver."Treatment" (
    treatment_id smallint NOT NULL,
    treatment_name character varying(255) NOT NULL
);


ALTER TABLE tingleserver."Treatment" OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 26039)
-- Name: Treatment_treatment_id_seq; Type: SEQUENCE; Schema: tingleserver; Owner: postgres
--

CREATE SEQUENCE tingleserver."Treatment_treatment_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tingleserver."Treatment_treatment_id_seq" OWNER TO postgres;

--
-- TOC entry 2863 (class 0 OID 0)
-- Dependencies: 207
-- Name: Treatment_treatment_id_seq; Type: SEQUENCE OWNED BY; Schema: tingleserver; Owner: postgres
--

ALTER SEQUENCE tingleserver."Treatment_treatment_id_seq" OWNED BY tingleserver."Treatment".treatment_id;


--
-- TOC entry 2717 (class 2604 OID 26072)
-- Name: Account ac_id; Type: DEFAULT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Account" ALTER COLUMN ac_id SET DEFAULT nextval('tingleserver."Account_ac_id_seq"'::regclass);


--
-- TOC entry 2716 (class 2604 OID 26044)
-- Name: Treatment treatment_id; Type: DEFAULT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Treatment" ALTER COLUMN treatment_id SET DEFAULT nextval('tingleserver."Treatment_treatment_id_seq"'::regclass);


--
-- TOC entry 2723 (class 2606 OID 26112)
-- Name: Account Account_ac_firstname_ac_lastname_key; Type: CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "Account_ac_firstname_ac_lastname_key" UNIQUE (ac_firstname, ac_lastname);


--
-- TOC entry 2725 (class 2606 OID 26077)
-- Name: Account Account_pkey; Type: CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "Account_pkey" PRIMARY KEY (ac_id);


--
-- TOC entry 2719 (class 2606 OID 34246)
-- Name: Patient Patient_ac_id_key; Type: CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_key" UNIQUE (ac_id);


--
-- TOC entry 2721 (class 2606 OID 26046)
-- Name: Treatment Treatment_pkey; Type: CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Treatment"
    ADD CONSTRAINT "Treatment_pkey" PRIMARY KEY (treatment_id);


--
-- TOC entry 2728 (class 2606 OID 26078)
-- Name: Admin Admin_ac_id_fkey; Type: FK CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT "Admin_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;


--
-- TOC entry 2727 (class 2606 OID 26083)
-- Name: Clinician Clinician_ac_id_fkey; Type: FK CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;


--
-- TOC entry 2729 (class 2606 OID 34247)
-- Name: Patient_Receives_Treatment Patient_Receives_Treatment_patient_id_fkey; Type: FK CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey" FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 2730 (class 2606 OID 34252)
-- Name: Patient_Receives_Treatment Patient_Receives_Treatment_treatment_id_fkey; Type: FK CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey" FOREIGN KEY (treatment_id) REFERENCES tingleserver."Treatment"(treatment_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 2726 (class 2606 OID 26113)
-- Name: Patient Patient_ac_id_fkey; Type: FK CONSTRAINT; Schema: tingleserver; Owner: postgres
--

ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED NOT VALID;


-- Completed on 2020-09-25 12:28:27

--
-- PostgreSQL database dump complete
--

