PGDMP         "            	    x           postgres    12.4    12.4 6    J           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            K           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            L           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            M           1262    13318    postgres    DATABASE     �   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';
    DROP DATABASE postgres;
                postgres    false            N           0    0    DATABASE postgres    COMMENT     N   COMMENT ON DATABASE postgres IS 'default administrative connection database';
                   postgres    false    2893                        2615    19786    tingleserver    SCHEMA        CREATE SCHEMA tingleserver;
    DROP SCHEMA tingleserver;
                postgres    false            �            1255    19878 �   add_clinician(character varying, character varying, smallint, character varying, character varying, character varying, character varying, character varying)    FUNCTION     !  CREATE FUNCTION tingleserver.add_clinician(firstname character varying, lastname character varying, gender smallint, age character varying, mobile character varying, email character varying, password character varying, type character varying) RETURNS smallint
    LANGUAGE plpgsql
    AS $$
DECLARE
	v_clinician_id smallint;
begin
	insert into tingleserver."Account" (ac_email,
										ac_password,
										ac_firstname,
										ac_lastname,
										ac_age,
										ac_gender,
										ac_phone,
										ac_type
									   )
   		values (email, password, firstname, lastname, age, gender, mobile, type);
		
	select max(ac_id) into v_clinician_id
		from tingleserver."Account";
		
	insert into tingleserver."Clinician" (ac_id) values (v_clinician_id);
		
	return v_clinician_id;
end;
$$;
 �   DROP FUNCTION tingleserver.add_clinician(firstname character varying, lastname character varying, gender smallint, age character varying, mobile character varying, email character varying, password character varying, type character varying);
       tingleserver          postgres    false    8            �            1255    19877 �   add_patient(character varying, character varying, character varying, smallint, character varying, character varying, character varying, character varying)    FUNCTION       CREATE FUNCTION tingleserver.add_patient(firstname character varying, lastname character varying, gender character varying, age smallint, mobile character varying, email character varying, password character varying, type character varying) RETURNS smallint
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
										ac_phone,
										ac_type
									   )
   		values (email, password, firstname, lastname, age, gender, mobile, type);
		
	select max(ac_id) into v_patient_id
		from tingleserver."Account";
		
	insert into tingleserver."Patient" (ac_id) values (v_patient_id);
		
	return v_patient_id;
end;
$$;
 �   DROP FUNCTION tingleserver.add_patient(firstname character varying, lastname character varying, gender character varying, age smallint, mobile character varying, email character varying, password character varying, type character varying);
       tingleserver          postgres    false    8            �            1255    19879 �   add_researcher(character varying, character varying, character varying, smallint, character varying, character varying, character varying, character varying)    FUNCTION     '  CREATE FUNCTION tingleserver.add_researcher(firstname character varying, lastname character varying, gender character varying, age smallint, mobile character varying, email character varying, password character varying, type character varying) RETURNS smallint
    LANGUAGE plpgsql
    AS $$
DECLARE
	v_researcher_id smallint;
begin
	insert into tingleserver."Account" (ac_email,
										ac_password,
										ac_firstname,
										ac_lastname,
										ac_age,
										ac_gender,
										ac_phone,
										ac_type
									   )
   		values (email, password, firstname, lastname, age, gender, mobile, type);
		
	select max(ac_id) into v_researcher_id
		from tingleserver."Account";
		
	insert into tingleserver."Researcher" (ac_id) values (v_researcher_id);
		
	return v_researcher_id;
end;
$$;
 �   DROP FUNCTION tingleserver.add_researcher(firstname character varying, lastname character varying, gender character varying, age smallint, mobile character varying, email character varying, password character varying, type character varying);
       tingleserver          postgres    false    8            �            1259    19788    Account    TABLE     �  CREATE TABLE tingleserver."Account" (
    ac_id smallint NOT NULL,
    ac_email character varying(255) NOT NULL,
    ac_password character varying(20) NOT NULL,
    ac_firstname character varying(255) NOT NULL,
    ac_lastname character varying(255) NOT NULL,
    ac_age smallint,
    ac_gender character varying(6) NOT NULL,
    ac_phone character varying(20),
    ac_type character varying(10)
);
 #   DROP TABLE tingleserver."Account";
       tingleserver         heap    postgres    false    8            �            1259    19794    Account_ac_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Account_ac_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE tingleserver."Account_ac_id_seq";
       tingleserver          postgres    false    203    8            O           0    0    Account_ac_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE tingleserver."Account_ac_id_seq" OWNED BY tingleserver."Account".ac_id;
          tingleserver          postgres    false    204            �            1259    19796    Admin    TABLE     C   CREATE TABLE tingleserver."Admin" (
    ac_id smallint NOT NULL
);
 !   DROP TABLE tingleserver."Admin";
       tingleserver         heap    postgres    false    8            �            1259    19799 	   Clinician    TABLE     G   CREATE TABLE tingleserver."Clinician" (
    ac_id smallint NOT NULL
);
 %   DROP TABLE tingleserver."Clinician";
       tingleserver         heap    postgres    false    8            �            1259    19802    Patient    TABLE     E   CREATE TABLE tingleserver."Patient" (
    ac_id smallint NOT NULL
);
 #   DROP TABLE tingleserver."Patient";
       tingleserver         heap    postgres    false    8            �            1259    19805    Patient_Receives_Treatment    TABLE     �   CREATE TABLE tingleserver."Patient_Receives_Treatment" (
    patient_id smallint NOT NULL,
    treatment_id smallint NOT NULL
);
 6   DROP TABLE tingleserver."Patient_Receives_Treatment";
       tingleserver         heap    postgres    false    8            �            1259    19882 
   Researcher    TABLE     G   CREATE TABLE tingleserver."Researcher" (
    ac_id integer NOT NULL
);
 &   DROP TABLE tingleserver."Researcher";
       tingleserver         heap    postgres    false    8            �            1259    19880    Researcher_ac_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Researcher_ac_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE tingleserver."Researcher_ac_id_seq";
       tingleserver          postgres    false    214    8            P           0    0    Researcher_ac_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE tingleserver."Researcher_ac_id_seq" OWNED BY tingleserver."Researcher".ac_id;
          tingleserver          postgres    false    213            �            1259    19808    Symptom    TABLE       CREATE TABLE tingleserver."Symptom" (
    symptom_id integer NOT NULL,
    patient_username character varying(255) NOT NULL,
    severity character varying(20),
    recorded_date date,
    recorded_time time without time zone,
    symptom_name character varying(255) NOT NULL
);
 #   DROP TABLE tingleserver."Symptom";
       tingleserver         heap    postgres    false    8            �            1259    19814    Symptom_symptom_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Symptom_symptom_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE tingleserver."Symptom_symptom_id_seq";
       tingleserver          postgres    false    8    209            Q           0    0    Symptom_symptom_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE tingleserver."Symptom_symptom_id_seq" OWNED BY tingleserver."Symptom".symptom_id;
          tingleserver          postgres    false    210            �            1259    19816 	   Treatment    TABLE     �   CREATE TABLE tingleserver."Treatment" (
    treatment_id smallint NOT NULL,
    treatment_name character varying(255) NOT NULL
);
 %   DROP TABLE tingleserver."Treatment";
       tingleserver         heap    postgres    false    8            �            1259    19819    Treatment_treatment_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Treatment_treatment_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE tingleserver."Treatment_treatment_id_seq";
       tingleserver          postgres    false    211    8            R           0    0    Treatment_treatment_id_seq    SEQUENCE OWNED BY     i   ALTER SEQUENCE tingleserver."Treatment_treatment_id_seq" OWNED BY tingleserver."Treatment".treatment_id;
          tingleserver          postgres    false    212            �
           2604    19821    Account ac_id    DEFAULT     ~   ALTER TABLE ONLY tingleserver."Account" ALTER COLUMN ac_id SET DEFAULT nextval('tingleserver."Account_ac_id_seq"'::regclass);
 D   ALTER TABLE tingleserver."Account" ALTER COLUMN ac_id DROP DEFAULT;
       tingleserver          postgres    false    204    203            �
           2604    19885    Researcher ac_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Researcher" ALTER COLUMN ac_id SET DEFAULT nextval('tingleserver."Researcher_ac_id_seq"'::regclass);
 G   ALTER TABLE tingleserver."Researcher" ALTER COLUMN ac_id DROP DEFAULT;
       tingleserver          postgres    false    213    214    214            �
           2604    19822    Symptom symptom_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Symptom" ALTER COLUMN symptom_id SET DEFAULT nextval('tingleserver."Symptom_symptom_id_seq"'::regclass);
 I   ALTER TABLE tingleserver."Symptom" ALTER COLUMN symptom_id DROP DEFAULT;
       tingleserver          postgres    false    210    209            �
           2604    19823    Treatment treatment_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Treatment" ALTER COLUMN treatment_id SET DEFAULT nextval('tingleserver."Treatment_treatment_id_seq"'::regclass);
 M   ALTER TABLE tingleserver."Treatment" ALTER COLUMN treatment_id DROP DEFAULT;
       tingleserver          postgres    false    212    211            <          0    19788    Account 
   TABLE DATA           �   COPY tingleserver."Account" (ac_id, ac_email, ac_password, ac_firstname, ac_lastname, ac_age, ac_gender, ac_phone, ac_type) FROM stdin;
    tingleserver          postgres    false    203   @N       >          0    19796    Admin 
   TABLE DATA           .   COPY tingleserver."Admin" (ac_id) FROM stdin;
    tingleserver          postgres    false    205   �O       ?          0    19799 	   Clinician 
   TABLE DATA           2   COPY tingleserver."Clinician" (ac_id) FROM stdin;
    tingleserver          postgres    false    206   �O       @          0    19802    Patient 
   TABLE DATA           0   COPY tingleserver."Patient" (ac_id) FROM stdin;
    tingleserver          postgres    false    207   �O       A          0    19805    Patient_Receives_Treatment 
   TABLE DATA           V   COPY tingleserver."Patient_Receives_Treatment" (patient_id, treatment_id) FROM stdin;
    tingleserver          postgres    false    208   P       G          0    19882 
   Researcher 
   TABLE DATA           3   COPY tingleserver."Researcher" (ac_id) FROM stdin;
    tingleserver          postgres    false    214   TP       B          0    19808    Symptom 
   TABLE DATA           }   COPY tingleserver."Symptom" (symptom_id, patient_username, severity, recorded_date, recorded_time, symptom_name) FROM stdin;
    tingleserver          postgres    false    209   qP       D          0    19816 	   Treatment 
   TABLE DATA           I   COPY tingleserver."Treatment" (treatment_id, treatment_name) FROM stdin;
    tingleserver          postgres    false    211   �P       S           0    0    Account_ac_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('tingleserver."Account_ac_id_seq"', 47, true);
          tingleserver          postgres    false    204            T           0    0    Researcher_ac_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('tingleserver."Researcher_ac_id_seq"', 1, false);
          tingleserver          postgres    false    213            U           0    0    Symptom_symptom_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('tingleserver."Symptom_symptom_id_seq"', 3, true);
          tingleserver          postgres    false    210            V           0    0    Treatment_treatment_id_seq    SEQUENCE SET     Q   SELECT pg_catalog.setval('tingleserver."Treatment_treatment_id_seq"', 1, false);
          tingleserver          postgres    false    212            �
           2606    19825 ,   Account Account_ac_firstname_ac_lastname_key 
   CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "Account_ac_firstname_ac_lastname_key" UNIQUE (ac_firstname, ac_lastname);
 `   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT "Account_ac_firstname_ac_lastname_key";
       tingleserver            postgres    false    203    203            �
           2606    19827    Account Account_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "Account_pkey" PRIMARY KEY (ac_id);
 H   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT "Account_pkey";
       tingleserver            postgres    false    203            �
           2606    19829    Patient Patient_ac_id_key 
   CONSTRAINT     _   ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_key" UNIQUE (ac_id);
 M   ALTER TABLE ONLY tingleserver."Patient" DROP CONSTRAINT "Patient_ac_id_key";
       tingleserver            postgres    false    207            �
           2606    19831    Treatment Treatment_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY tingleserver."Treatment"
    ADD CONSTRAINT "Treatment_pkey" PRIMARY KEY (treatment_id);
 L   ALTER TABLE ONLY tingleserver."Treatment" DROP CONSTRAINT "Treatment_pkey";
       tingleserver            postgres    false    211            �
           2606    19833    Account ac_email 
   CONSTRAINT     W   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT ac_email UNIQUE (ac_email);
 B   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT ac_email;
       tingleserver            postgres    false    203            �
           2606    19835    Symptom symptom_id 
   CONSTRAINT     `   ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT symptom_id PRIMARY KEY (symptom_id);
 D   ALTER TABLE ONLY tingleserver."Symptom" DROP CONSTRAINT symptom_id;
       tingleserver            postgres    false    209            �
           2606    19836    Admin Admin_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT "Admin_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;
 J   ALTER TABLE ONLY tingleserver."Admin" DROP CONSTRAINT "Admin_ac_id_fkey";
       tingleserver          postgres    false    203    2734    205            �
           2606    19841    Clinician Clinician_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;
 R   ALTER TABLE ONLY tingleserver."Clinician" DROP CONSTRAINT "Clinician_ac_id_fkey";
       tingleserver          postgres    false    203    206    2734            �
           2606    19846 E   Patient_Receives_Treatment Patient_Receives_Treatment_patient_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey" FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 y   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment" DROP CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey";
       tingleserver          postgres    false    207    208    2738            �
           2606    19851 G   Patient_Receives_Treatment Patient_Receives_Treatment_treatment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey" FOREIGN KEY (treatment_id) REFERENCES tingleserver."Treatment"(treatment_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 {   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment" DROP CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey";
       tingleserver          postgres    false    208    211    2742            �
           2606    19856    Patient Patient_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED NOT VALID;
 N   ALTER TABLE ONLY tingleserver."Patient" DROP CONSTRAINT "Patient_ac_id_fkey";
       tingleserver          postgres    false    203    2734    207            �
           2606    19886    Researcher ac_id    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Researcher"
    ADD CONSTRAINT ac_id FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id);
 B   ALTER TABLE ONLY tingleserver."Researcher" DROP CONSTRAINT ac_id;
       tingleserver          postgres    false    214    2734    203            �
           2606    19861    Symptom username    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT username FOREIGN KEY (patient_username) REFERENCES tingleserver."Account"(ac_email) NOT VALID;
 B   ALTER TABLE ONLY tingleserver."Symptom" DROP CONSTRAINT username;
       tingleserver          postgres    false    209    2736    203            <   D  x�}ҽn�0 ��x�<�6!�e��i�N]���_b��R޾6QB*E�|����`�S@(+�զ�]z۫q(����$�k ��`��$� m�'٢岅�qZ�CZ��@���53����ȧ�WZ2cDAj�ȜY����l�V��Cc���GwzR����t�Z1VnGg�0q'�\�1��s<|`ߛ��D����bk�Z�b�K��&p��Lw	�~*��(�LÿޔԒ+ͥ�K���m�8�t�8�A���_��8ܪ��~.�O$|E}g|c<�šE�Њ�G�*)�!��!�=i�08��?ຠ��L,�ڎ�!ϲ��߷�      >      x������ � �      ?      x�3����� Z �      @   '   x���  İ�A4'��ρ]b���C6��4oO��      A   =   x�˻� �Z����]��4W�Q1���PܼMWeuIO횺^<���'
s      G      x������ � �      B   p   x���;
�0 �zs�\ �n"�T����f�`�
����L�z8C�|\��!���1u�f��)�-% $Thj��r��Ĳ�w�̷\�C�?�~�ir�Gz�����N� !�J2      D     x�M��j�0D��W�h�)u���MJ1�)!���J^�@����_ߕM����̮���rk~,�Ɖ$�~�*��WFk�T�@�T��PքyQ֒���t�WynSQ��[��lA�k� 楒oXښF�"9��m*^���+�'C���l�5��{�������~�$�3L���8��@�'v2N��U�o#)=G��"���<�g�oz�Ʒ��(B��d�Շ'B%�ZM�X����'�,#kV��&���)ڰ<u����t��q�� 2��/     