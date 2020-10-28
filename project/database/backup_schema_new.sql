PGDMP     :                	    x           postgres    12.4    12.4 ?    c           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            d           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            e           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            f           1262    13318    postgres    DATABASE     �   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_Australia.1252' LC_CTYPE = 'English_Australia.1252';
    DROP DATABASE postgres;
                postgres    false            g           0    0    DATABASE postgres    COMMENT     N   COMMENT ON DATABASE postgres IS 'default administrative connection database';
                   postgres    false    2918            	            2615    59027    tingleserver    SCHEMA        CREATE SCHEMA tingleserver;
    DROP SCHEMA tingleserver;
                postgres    false            �            1255    59028 �   add_account(character varying, character varying, character varying, smallint, character varying, character varying, character varying, character varying, character varying)    FUNCTION     �  CREATE FUNCTION tingleserver.add_account(first_name character varying, last_name character varying, gender character varying, age smallint, mobile character varying, email character varying, password_hash character varying, user_role character varying, consent character varying) RETURNS smallint
    LANGUAGE plpgsql
    AS $$
DECLARE account_id smallint;
BEGIN
	INSERT INTO tingleserver."Account" (ac_email,
										ac_password,
										ac_firstname,
										ac_lastname,
										ac_age,
										ac_gender,
										ac_phone,
										ac_type
									   )
   		VALUES(email, password_hash, first_name, last_name, age, gender, mobile, user_role);

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
   DROP FUNCTION tingleserver.add_account(first_name character varying, last_name character varying, gender character varying, age smallint, mobile character varying, email character varying, password_hash character varying, user_role character varying, consent character varying);
       tingleserver          postgres    false    9            �            1259    59029    Account    TABLE     �  CREATE TABLE tingleserver."Account" (
    ac_id smallint NOT NULL,
    ac_email character varying(255) NOT NULL,
    ac_password character varying(255) NOT NULL,
    ac_firstname character varying(255) NOT NULL,
    ac_lastname character varying(255) NOT NULL,
    ac_age smallint,
    ac_gender character varying(6) NOT NULL,
    ac_phone character varying(20),
    ac_type character varying(50)
);
 #   DROP TABLE tingleserver."Account";
       tingleserver         heap    postgres    false    9            �            1259    59035    Account_Invitation    TABLE     �   CREATE TABLE tingleserver."Account_Invitation" (
    token character varying(255) NOT NULL,
    ac_email character varying(255) NOT NULL,
    role character varying(20) NOT NULL
);
 .   DROP TABLE tingleserver."Account_Invitation";
       tingleserver         heap    postgres    false    9            �            1259    59041    Account_ac_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Account_ac_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE tingleserver."Account_ac_id_seq";
       tingleserver          postgres    false    9    204            h           0    0    Account_ac_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE tingleserver."Account_ac_id_seq" OWNED BY tingleserver."Account".ac_id;
          tingleserver          postgres    false    206            �            1259    59043    Admin    TABLE     C   CREATE TABLE tingleserver."Admin" (
    ac_id smallint NOT NULL
);
 !   DROP TABLE tingleserver."Admin";
       tingleserver         heap    postgres    false    9            �            1259    59046 	   Clinician    TABLE     G   CREATE TABLE tingleserver."Clinician" (
    ac_id smallint NOT NULL
);
 %   DROP TABLE tingleserver."Clinician";
       tingleserver         heap    postgres    false    9            �            1259    59049    Forgot_password    TABLE     u   CREATE TABLE tingleserver."Forgot_password" (
    key character(24) NOT NULL,
    ac_email character varying(255)
);
 +   DROP TABLE tingleserver."Forgot_password";
       tingleserver         heap    postgres    false    9            �            1259    59052    Patient    TABLE     g   CREATE TABLE tingleserver."Patient" (
    ac_id smallint NOT NULL,
    consent character varying(3)
);
 #   DROP TABLE tingleserver."Patient";
       tingleserver         heap    postgres    false    9            �            1259    59055    Patient_Clinician    TABLE     x   CREATE TABLE tingleserver."Patient_Clinician" (
    patient_id smallint NOT NULL,
    clinician_id smallint NOT NULL
);
 -   DROP TABLE tingleserver."Patient_Clinician";
       tingleserver         heap    postgres    false    9            �            1259    59058    Patient_Receives_Treatment    TABLE     �   CREATE TABLE tingleserver."Patient_Receives_Treatment" (
    patient_id smallint NOT NULL,
    treatment_id smallint NOT NULL
);
 6   DROP TABLE tingleserver."Patient_Receives_Treatment";
       tingleserver         heap    postgres    false    9            �            1259    59061 
   Researcher    TABLE     ?   CREATE TABLE tingleserver."Researcher" (
    ac_id smallint
);
 &   DROP TABLE tingleserver."Researcher";
       tingleserver         heap    postgres    false    9            �            1259    59064    Symptom    TABLE     Y  CREATE TABLE tingleserver."Symptom" (
    symptom_id integer NOT NULL,
    patient_username character varying(255) NOT NULL,
    severity character varying(20),
    recorded_date date,
    symptom_name character varying(255) NOT NULL,
    notes character varying(255),
    location character varying(255),
    occurence character varying(12)
);
 #   DROP TABLE tingleserver."Symptom";
       tingleserver         heap    postgres    false    9            �            1259    59070    Symptom_symptom_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Symptom_symptom_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE tingleserver."Symptom_symptom_id_seq";
       tingleserver          postgres    false    9    214            i           0    0    Symptom_symptom_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE tingleserver."Symptom_symptom_id_seq" OWNED BY tingleserver."Symptom".symptom_id;
          tingleserver          postgres    false    215            �            1259    59072 	   Treatment    TABLE     �   CREATE TABLE tingleserver."Treatment" (
    treatment_id smallint NOT NULL,
    treatment_name character varying(255) NOT NULL
);
 %   DROP TABLE tingleserver."Treatment";
       tingleserver         heap    postgres    false    9            �            1259    59075    Treatment_treatment_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Treatment_treatment_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE tingleserver."Treatment_treatment_id_seq";
       tingleserver          postgres    false    9    216            j           0    0    Treatment_treatment_id_seq    SEQUENCE OWNED BY     i   ALTER SEQUENCE tingleserver."Treatment_treatment_id_seq" OWNED BY tingleserver."Treatment".treatment_id;
          tingleserver          postgres    false    217            �
           2604    59077    Account ac_id    DEFAULT     ~   ALTER TABLE ONLY tingleserver."Account" ALTER COLUMN ac_id SET DEFAULT nextval('tingleserver."Account_ac_id_seq"'::regclass);
 D   ALTER TABLE tingleserver."Account" ALTER COLUMN ac_id DROP DEFAULT;
       tingleserver          postgres    false    206    204            �
           2604    59078    Symptom symptom_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Symptom" ALTER COLUMN symptom_id SET DEFAULT nextval('tingleserver."Symptom_symptom_id_seq"'::regclass);
 I   ALTER TABLE tingleserver."Symptom" ALTER COLUMN symptom_id DROP DEFAULT;
       tingleserver          postgres    false    215    214            �
           2604    59079    Treatment treatment_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Treatment" ALTER COLUMN treatment_id SET DEFAULT nextval('tingleserver."Treatment_treatment_id_seq"'::regclass);
 M   ALTER TABLE tingleserver."Treatment" ALTER COLUMN treatment_id DROP DEFAULT;
       tingleserver          postgres    false    217    216            S          0    59029    Account 
   TABLE DATA           �   COPY tingleserver."Account" (ac_id, ac_email, ac_password, ac_firstname, ac_lastname, ac_age, ac_gender, ac_phone, ac_type) FROM stdin;
    tingleserver          postgres    false    204   bU       T          0    59035    Account_Invitation 
   TABLE DATA           K   COPY tingleserver."Account_Invitation" (token, ac_email, role) FROM stdin;
    tingleserver          postgres    false    205   �V       V          0    59043    Admin 
   TABLE DATA           .   COPY tingleserver."Admin" (ac_id) FROM stdin;
    tingleserver          postgres    false    207   W       W          0    59046 	   Clinician 
   TABLE DATA           2   COPY tingleserver."Clinician" (ac_id) FROM stdin;
    tingleserver          postgres    false    208   !W       X          0    59049    Forgot_password 
   TABLE DATA           @   COPY tingleserver."Forgot_password" (key, ac_email) FROM stdin;
    tingleserver          postgres    false    209   AW       Y          0    59052    Patient 
   TABLE DATA           9   COPY tingleserver."Patient" (ac_id, consent) FROM stdin;
    tingleserver          postgres    false    210   ^W       Z          0    59055    Patient_Clinician 
   TABLE DATA           M   COPY tingleserver."Patient_Clinician" (patient_id, clinician_id) FROM stdin;
    tingleserver          postgres    false    211   �W       [          0    59058    Patient_Receives_Treatment 
   TABLE DATA           V   COPY tingleserver."Patient_Receives_Treatment" (patient_id, treatment_id) FROM stdin;
    tingleserver          postgres    false    212   �W       \          0    59061 
   Researcher 
   TABLE DATA           3   COPY tingleserver."Researcher" (ac_id) FROM stdin;
    tingleserver          postgres    false    213   �W       ]          0    59064    Symptom 
   TABLE DATA           �   COPY tingleserver."Symptom" (symptom_id, patient_username, severity, recorded_date, symptom_name, notes, location, occurence) FROM stdin;
    tingleserver          postgres    false    214   �W       _          0    59072 	   Treatment 
   TABLE DATA           I   COPY tingleserver."Treatment" (treatment_id, treatment_name) FROM stdin;
    tingleserver          postgres    false    216   sX       k           0    0    Account_ac_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('tingleserver."Account_ac_id_seq"', 79, true);
          tingleserver          postgres    false    206            l           0    0    Symptom_symptom_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('tingleserver."Symptom_symptom_id_seq"', 15, true);
          tingleserver          postgres    false    215            m           0    0    Treatment_treatment_id_seq    SEQUENCE SET     Q   SELECT pg_catalog.setval('tingleserver."Treatment_treatment_id_seq"', 1, false);
          tingleserver          postgres    false    217            �
           2606    59081 *   Account_Invitation Account_Invitation_pkey 
   CONSTRAINT     u   ALTER TABLE ONLY tingleserver."Account_Invitation"
    ADD CONSTRAINT "Account_Invitation_pkey" PRIMARY KEY (token);
 ^   ALTER TABLE ONLY tingleserver."Account_Invitation" DROP CONSTRAINT "Account_Invitation_pkey";
       tingleserver            postgres    false    205            �
           2606    59083    Account Account_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "Account_pkey" PRIMARY KEY (ac_id);
 H   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT "Account_pkey";
       tingleserver            postgres    false    204            �
           2606    59085    Admin Admin_ac_id_key 
   CONSTRAINT     [   ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT "Admin_ac_id_key" UNIQUE (ac_id);
 I   ALTER TABLE ONLY tingleserver."Admin" DROP CONSTRAINT "Admin_ac_id_key";
       tingleserver            postgres    false    207            �
           2606    59087    Clinician Clinician_ac_id_key 
   CONSTRAINT     c   ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_key" UNIQUE (ac_id);
 Q   ALTER TABLE ONLY tingleserver."Clinician" DROP CONSTRAINT "Clinician_ac_id_key";
       tingleserver            postgres    false    208            �
           2606    59089    Patient Patient_ac_id_key 
   CONSTRAINT     _   ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_key" UNIQUE (ac_id);
 M   ALTER TABLE ONLY tingleserver."Patient" DROP CONSTRAINT "Patient_ac_id_key";
       tingleserver            postgres    false    210            �
           2606    59091    Researcher Researcher_ac_id_key 
   CONSTRAINT     e   ALTER TABLE ONLY tingleserver."Researcher"
    ADD CONSTRAINT "Researcher_ac_id_key" UNIQUE (ac_id);
 S   ALTER TABLE ONLY tingleserver."Researcher" DROP CONSTRAINT "Researcher_ac_id_key";
       tingleserver            postgres    false    213            �
           2606    59093    Treatment Treatment_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY tingleserver."Treatment"
    ADD CONSTRAINT "Treatment_pkey" PRIMARY KEY (treatment_id);
 L   ALTER TABLE ONLY tingleserver."Treatment" DROP CONSTRAINT "Treatment_pkey";
       tingleserver            postgres    false    216            �
           2606    59095    Account ac_email 
   CONSTRAINT     W   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT ac_email UNIQUE (ac_email);
 B   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT ac_email;
       tingleserver            postgres    false    204            �
           2606    59097    Forgot_password key 
   CONSTRAINT     Z   ALTER TABLE ONLY tingleserver."Forgot_password"
    ADD CONSTRAINT key PRIMARY KEY (key);
 E   ALTER TABLE ONLY tingleserver."Forgot_password" DROP CONSTRAINT key;
       tingleserver            postgres    false    209            �
           2606    59099 .   Patient_Clinician patient_clinician_unique_key 
   CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT patient_clinician_unique_key UNIQUE (patient_id, clinician_id);
 `   ALTER TABLE ONLY tingleserver."Patient_Clinician" DROP CONSTRAINT patient_clinician_unique_key;
       tingleserver            postgres    false    211    211            �
           2606    59101    Symptom symptom_id 
   CONSTRAINT     `   ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT symptom_id PRIMARY KEY (symptom_id);
 D   ALTER TABLE ONLY tingleserver."Symptom" DROP CONSTRAINT symptom_id;
       tingleserver            postgres    false    214            �
           1259    59102    fki_id_key_ac_email_fkey    INDEX     `   CREATE INDEX fki_id_key_ac_email_fkey ON tingleserver."Forgot_password" USING btree (ac_email);
 2   DROP INDEX tingleserver.fki_id_key_ac_email_fkey;
       tingleserver            postgres    false    209            �
           2606    59108    Clinician Clinician_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;
 R   ALTER TABLE ONLY tingleserver."Clinician" DROP CONSTRAINT "Clinician_ac_id_fkey";
       tingleserver          postgres    false    208    2741    204            �
           2606    59113 E   Patient_Receives_Treatment Patient_Receives_Treatment_patient_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey" FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 y   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment" DROP CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey";
       tingleserver          postgres    false    210    2754    212            �
           2606    59118 G   Patient_Receives_Treatment Patient_Receives_Treatment_treatment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey" FOREIGN KEY (treatment_id) REFERENCES tingleserver."Treatment"(treatment_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 {   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment" DROP CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey";
       tingleserver          postgres    false    216    2762    212            �
           2606    59123    Patient Patient_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED NOT VALID;
 N   ALTER TABLE ONLY tingleserver."Patient" DROP CONSTRAINT "Patient_ac_id_fkey";
       tingleserver          postgres    false    2741    204    210            �
           2606    59128     Researcher Researcher_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Researcher"
    ADD CONSTRAINT "Researcher_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id);
 T   ALTER TABLE ONLY tingleserver."Researcher" DROP CONSTRAINT "Researcher_ac_id_fkey";
       tingleserver          postgres    false    2741    204    213            �
           2606    59133 !   Patient_Clinician clinician_id_fk    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT clinician_id_fk FOREIGN KEY (clinician_id) REFERENCES tingleserver."Clinician"(ac_id);
 S   ALTER TABLE ONLY tingleserver."Patient_Clinician" DROP CONSTRAINT clinician_id_fk;
       tingleserver          postgres    false    211    2749    208            �
           2606    59154    Admin fk_admin_account    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT fk_admin_account FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 H   ALTER TABLE ONLY tingleserver."Admin" DROP CONSTRAINT fk_admin_account;
       tingleserver          postgres    false    207    2741    204            �
           2606    59138 !   Forgot_password key_ac_email_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Forgot_password"
    ADD CONSTRAINT key_ac_email_fkey FOREIGN KEY (ac_email) REFERENCES tingleserver."Account"(ac_email);
 S   ALTER TABLE ONLY tingleserver."Forgot_password" DROP CONSTRAINT key_ac_email_fkey;
       tingleserver          postgres    false    2743    209    204            �
           2606    59143    Patient_Clinician patient_id_fk    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT patient_id_fk FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id);
 Q   ALTER TABLE ONLY tingleserver."Patient_Clinician" DROP CONSTRAINT patient_id_fk;
       tingleserver          postgres    false    2754    210    211            �
           2606    59148    Symptom username    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT username FOREIGN KEY (patient_username) REFERENCES tingleserver."Account"(ac_email) NOT VALID;
 B   ALTER TABLE ONLY tingleserver."Symptom" DROP CONSTRAINT username;
       tingleserver          postgres    false    204    2743    214            S   r  x���Mk1��w�4�I9%��$�\�R
�����^{[��&io��އwX�Q�Ѧ�n��|S{w,����y����/�����}��*փ��K�E#Y	āU *�(�r�@�rh�7�\<{�b��ܓN��s���ug�$���4GWw�4�Q�+�_�m���諊y�	!ǐZV��-x�$#��E��c�HҠ����a3���w�X \l��iN�dg�S���m��$�?�ݪ�*����<@2�j�W̖8WL)S�e�R{Ch�E�������6�6�-��8��Ӷ�u��3����qյT�BJ�ZYa!Z��!VĜS��4tL`��d�#I As���}��������������N*�S      T      x������ � �      V      x�33�����       W      x�35����� -      X      x������ � �      Y      x�35�L-����� �x      Z      x������ � �      [      x������ � �      \      x�3������� 4       ]   �   x�eα
1�9}���G{���ࠇ��KN�hS����n"������+x�2�n��6��"���к�-|��,c(أ<2����e�?Ϭd��#��9B9WDW[X5ПQ�N�p�1�1MR2���~�<�      _     x�M��j�0D��W�h�)u���MJ1�)!���J^�@����_ߕM����̮���rk~,�Ɖ$�~�*��WFk�T�@�T��PքyQ֒���t�WynSQ��[��lA�k� 楒oXښF�"9��m*^���+�'C���l�5��{�������~�$�3L���8��@�'v2N��U�o#)=G��"���<�g�oz�Ʒ��(B��d�Շ'B%�ZM�X����'�,#kV��&���)ڰ<u����t��q�� 2��/     