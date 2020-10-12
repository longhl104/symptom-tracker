PGDMP                     	    x           postgres    12.4    12.4 /    ?           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            @           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            A           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            B           1262    13318    postgres    DATABASE     �   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_Australia.1252' LC_CTYPE = 'English_Australia.1252';
    DROP DATABASE postgres;
                postgres    false            C           0    0    DATABASE postgres    COMMENT     N   COMMENT ON DATABASE postgres IS 'default administrative connection database';
                   postgres    false    2882                        2615    50629    tingleserver    SCHEMA        CREATE SCHEMA tingleserver;
    DROP SCHEMA tingleserver;
                postgres    false                        3079    16384 	   adminpack 	   EXTENSION     A   CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;
    DROP EXTENSION adminpack;
                   false            D           0    0    EXTENSION adminpack    COMMENT     M   COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';
                        false    1            �            1255    50630 �   add_patient(character varying, character varying, character varying, smallint, character varying, character varying, character varying)    FUNCTION     �  CREATE FUNCTION tingleserver.add_patient(firstname character varying, lastname character varying, gender character varying, age smallint, mobile character varying, email character varying, password character varying) RETURNS smallint
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
 �   DROP FUNCTION tingleserver.add_patient(firstname character varying, lastname character varying, gender character varying, age smallint, mobile character varying, email character varying, password character varying);
       tingleserver          postgres    false    7            �            1259    50631    Account    TABLE     m  CREATE TABLE tingleserver."Account" (
    ac_id smallint NOT NULL,
    ac_email character varying(255) NOT NULL,
    ac_password character varying(255) NOT NULL,
    ac_firstname character varying(255) NOT NULL,
    ac_lastname character varying(255) NOT NULL,
    ac_age smallint,
    ac_gender character varying(6) NOT NULL,
    ac_phone character varying(20)
);
 #   DROP TABLE tingleserver."Account";
       tingleserver         heap    postgres    false    7            �            1259    50637    Account_ac_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Account_ac_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE tingleserver."Account_ac_id_seq";
       tingleserver          postgres    false    204    7            E           0    0    Account_ac_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE tingleserver."Account_ac_id_seq" OWNED BY tingleserver."Account".ac_id;
          tingleserver          postgres    false    205            �            1259    50639    Admin    TABLE     C   CREATE TABLE tingleserver."Admin" (
    ac_id smallint NOT NULL
);
 !   DROP TABLE tingleserver."Admin";
       tingleserver         heap    postgres    false    7            �            1259    50642 	   Clinician    TABLE     G   CREATE TABLE tingleserver."Clinician" (
    ac_id smallint NOT NULL
);
 %   DROP TABLE tingleserver."Clinician";
       tingleserver         heap    postgres    false    7            �            1259    50645    Patient    TABLE     E   CREATE TABLE tingleserver."Patient" (
    ac_id smallint NOT NULL
);
 #   DROP TABLE tingleserver."Patient";
       tingleserver         heap    postgres    false    7            �            1259    50648    Patient_Receives_Treatment    TABLE     �   CREATE TABLE tingleserver."Patient_Receives_Treatment" (
    patient_id smallint NOT NULL,
    treatment_id smallint NOT NULL
);
 6   DROP TABLE tingleserver."Patient_Receives_Treatment";
       tingleserver         heap    postgres    false    7            �            1259    50651    Symptom    TABLE     ^  CREATE TABLE tingleserver."Symptom" (
    symptom_id integer NOT NULL,
    patient_username character varying(255) NOT NULL,
    severity character varying(20),
    recorded_date date,
    recorded_time time without time zone,
    symptom_name character varying(255) NOT NULL,
    notes character varying(255),
    activity character varying(255)
);
 #   DROP TABLE tingleserver."Symptom";
       tingleserver         heap    postgres    false    7            �            1259    50657    Symptom_symptom_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Symptom_symptom_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE tingleserver."Symptom_symptom_id_seq";
       tingleserver          postgres    false    210    7            F           0    0    Symptom_symptom_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE tingleserver."Symptom_symptom_id_seq" OWNED BY tingleserver."Symptom".symptom_id;
          tingleserver          postgres    false    211            �            1259    50659 	   Treatment    TABLE     �   CREATE TABLE tingleserver."Treatment" (
    treatment_id smallint NOT NULL,
    treatment_name character varying(255) NOT NULL
);
 %   DROP TABLE tingleserver."Treatment";
       tingleserver         heap    postgres    false    7            �            1259    50662    Treatment_treatment_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Treatment_treatment_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE tingleserver."Treatment_treatment_id_seq";
       tingleserver          postgres    false    212    7            G           0    0    Treatment_treatment_id_seq    SEQUENCE OWNED BY     i   ALTER SEQUENCE tingleserver."Treatment_treatment_id_seq" OWNED BY tingleserver."Treatment".treatment_id;
          tingleserver          postgres    false    213            �
           2604    50664    Account ac_id    DEFAULT     ~   ALTER TABLE ONLY tingleserver."Account" ALTER COLUMN ac_id SET DEFAULT nextval('tingleserver."Account_ac_id_seq"'::regclass);
 D   ALTER TABLE tingleserver."Account" ALTER COLUMN ac_id DROP DEFAULT;
       tingleserver          postgres    false    205    204            �
           2604    50665    Symptom symptom_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Symptom" ALTER COLUMN symptom_id SET DEFAULT nextval('tingleserver."Symptom_symptom_id_seq"'::regclass);
 I   ALTER TABLE tingleserver."Symptom" ALTER COLUMN symptom_id DROP DEFAULT;
       tingleserver          postgres    false    211    210            �
           2604    50666    Treatment treatment_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Treatment" ALTER COLUMN treatment_id SET DEFAULT nextval('tingleserver."Treatment_treatment_id_seq"'::regclass);
 M   ALTER TABLE tingleserver."Treatment" ALTER COLUMN treatment_id DROP DEFAULT;
       tingleserver          postgres    false    213    212            3          0    50631    Account 
   TABLE DATA              COPY tingleserver."Account" (ac_id, ac_email, ac_password, ac_firstname, ac_lastname, ac_age, ac_gender, ac_phone) FROM stdin;
    tingleserver          postgres    false    204   /=       5          0    50639    Admin 
   TABLE DATA           .   COPY tingleserver."Admin" (ac_id) FROM stdin;
    tingleserver          postgres    false    206   >       6          0    50642 	   Clinician 
   TABLE DATA           2   COPY tingleserver."Clinician" (ac_id) FROM stdin;
    tingleserver          postgres    false    207   5>       7          0    50645    Patient 
   TABLE DATA           0   COPY tingleserver."Patient" (ac_id) FROM stdin;
    tingleserver          postgres    false    208   T>       8          0    50648    Patient_Receives_Treatment 
   TABLE DATA           V   COPY tingleserver."Patient_Receives_Treatment" (patient_id, treatment_id) FROM stdin;
    tingleserver          postgres    false    209   w>       9          0    50651    Symptom 
   TABLE DATA           �   COPY tingleserver."Symptom" (symptom_id, patient_username, severity, recorded_date, recorded_time, symptom_name, notes, activity) FROM stdin;
    tingleserver          postgres    false    210   �>       ;          0    50659 	   Treatment 
   TABLE DATA           I   COPY tingleserver."Treatment" (treatment_id, treatment_name) FROM stdin;
    tingleserver          postgres    false    212   �>       H           0    0    Account_ac_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('tingleserver."Account_ac_id_seq"', 39, true);
          tingleserver          postgres    false    205            I           0    0    Symptom_symptom_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('tingleserver."Symptom_symptom_id_seq"', 4, true);
          tingleserver          postgres    false    211            J           0    0    Treatment_treatment_id_seq    SEQUENCE SET     Q   SELECT pg_catalog.setval('tingleserver."Treatment_treatment_id_seq"', 1, false);
          tingleserver          postgres    false    213            �
           2606    50668 ,   Account Account_ac_firstname_ac_lastname_key 
   CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "Account_ac_firstname_ac_lastname_key" UNIQUE (ac_firstname, ac_lastname);
 `   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT "Account_ac_firstname_ac_lastname_key";
       tingleserver            postgres    false    204    204            �
           2606    50670    Account Account_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "Account_pkey" PRIMARY KEY (ac_id);
 H   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT "Account_pkey";
       tingleserver            postgres    false    204            �
           2606    50672    Patient Patient_ac_id_key 
   CONSTRAINT     _   ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_key" UNIQUE (ac_id);
 M   ALTER TABLE ONLY tingleserver."Patient" DROP CONSTRAINT "Patient_ac_id_key";
       tingleserver            postgres    false    208            �
           2606    50674    Treatment Treatment_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY tingleserver."Treatment"
    ADD CONSTRAINT "Treatment_pkey" PRIMARY KEY (treatment_id);
 L   ALTER TABLE ONLY tingleserver."Treatment" DROP CONSTRAINT "Treatment_pkey";
       tingleserver            postgres    false    212            �
           2606    50676    Account ac_email 
   CONSTRAINT     W   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT ac_email UNIQUE (ac_email);
 B   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT ac_email;
       tingleserver            postgres    false    204            �
           2606    50678    Symptom symptom_id 
   CONSTRAINT     `   ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT symptom_id PRIMARY KEY (symptom_id);
 D   ALTER TABLE ONLY tingleserver."Symptom" DROP CONSTRAINT symptom_id;
       tingleserver            postgres    false    210            �
           2606    50679    Admin Admin_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT "Admin_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;
 J   ALTER TABLE ONLY tingleserver."Admin" DROP CONSTRAINT "Admin_ac_id_fkey";
       tingleserver          postgres    false    2726    206    204            �
           2606    50684    Clinician Clinician_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;
 R   ALTER TABLE ONLY tingleserver."Clinician" DROP CONSTRAINT "Clinician_ac_id_fkey";
       tingleserver          postgres    false    204    2726    207            �
           2606    50689 E   Patient_Receives_Treatment Patient_Receives_Treatment_patient_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey" FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 y   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment" DROP CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey";
       tingleserver          postgres    false    2730    209    208            �
           2606    50694 G   Patient_Receives_Treatment Patient_Receives_Treatment_treatment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey" FOREIGN KEY (treatment_id) REFERENCES tingleserver."Treatment"(treatment_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 {   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment" DROP CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey";
       tingleserver          postgres    false    2734    209    212            �
           2606    50699    Patient Patient_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED NOT VALID;
 N   ALTER TABLE ONLY tingleserver."Patient" DROP CONSTRAINT "Patient_ac_id_fkey";
       tingleserver          postgres    false    204    2726    208            �
           2606    50704    Symptom username    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT username FOREIGN KEY (patient_username) REFERENCES tingleserver."Account"(ac_email) NOT VALID;
 B   ALTER TABLE ONLY tingleserver."Symptom" DROP CONSTRAINT username;
       tingleserver          postgres    false    2728    210    204            3   �   x���;k�@���;T�����+CR�G�.ͽVQ,K�D��\�"S~��eW@�4��4�z7��V�_��?�Z��	��}y�����@��&��"��A�� J�1UB!�r�9*�� b6�8��q5��9��X�$���e��ָ7U��ןk�ȯ}a8�`%{��*2p�)%�����Z�-��������Z�y�����%����u�/&�T�      5      x������ � �      6      x�3����� Z �      7      x�3��2������ 
��      8      x������ � �      9      x������ � �      ;     x�M��j�0D��W�h�)u���MJ1�)!���J^�@����_ߕM����̮���rk~,�Ɖ$�~�*��WFk�T�@�T��PքyQ֒���t�WynSQ��[��lA�k� 楒oXښF�"9��m*^���+�'C���l�5��{�������~�$�3L���8��@�'v2N��U�o#)=G��"���<�g�oz�Ʒ��(B��d�Շ'B%�ZM�X����'�,#kV��&���)ڰ<u����t��q�� 2��/     