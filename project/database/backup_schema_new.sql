PGDMP     "                
    x           postgres    13.0    13.0 ?    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    13707    postgres    DATABASE     S   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'C';
    DROP DATABASE postgres;
                postgres    false            �           0    0    DATABASE postgres    COMMENT     N   COMMENT ON DATABASE postgres IS 'default administrative connection database';
                   postgres    false    3471                        2615    17062    tingleserver    SCHEMA        CREATE SCHEMA tingleserver;
    DROP SCHEMA tingleserver;
                postgres    false                       1255    17063 �   add_account(character varying, character varying, character varying, smallint, character varying, character varying, character varying, character varying, character varying)    FUNCTION     �  CREATE FUNCTION tingleserver.add_account(first_name character varying, last_name character varying, gender character varying, age smallint, mobile character varying, email character varying, password_hash character varying, user_role character varying, consent character varying) RETURNS smallint
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
       tingleserver          postgres    false    7            �            1259    17064    Account    TABLE     �  CREATE TABLE tingleserver."Account" (
    ac_id smallint NOT NULL,
    ac_email character varying(255) NOT NULL,
    ac_password character varying(255) NOT NULL,
    ac_firstname character varying(255) NOT NULL,
    ac_lastname character varying(255) NOT NULL,
    ac_age smallint,
    ac_gender character varying(6),
    ac_phone character varying(20),
    ac_type character varying(50)
);
 #   DROP TABLE tingleserver."Account";
       tingleserver         heap    postgres    false    7            �            1259    17070    Account_Invitation    TABLE     �   CREATE TABLE tingleserver."Account_Invitation" (
    token character varying(255) NOT NULL,
    ac_email character varying(255) NOT NULL,
    role character varying(20) NOT NULL
);
 .   DROP TABLE tingleserver."Account_Invitation";
       tingleserver         heap    postgres    false    7            �            1259    17076    Account_ac_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Account_ac_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE tingleserver."Account_ac_id_seq";
       tingleserver          postgres    false    7    243            �           0    0    Account_ac_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE tingleserver."Account_ac_id_seq" OWNED BY tingleserver."Account".ac_id;
          tingleserver          postgres    false    245            �            1259    17078    Admin    TABLE     C   CREATE TABLE tingleserver."Admin" (
    ac_id smallint NOT NULL
);
 !   DROP TABLE tingleserver."Admin";
       tingleserver         heap    postgres    false    7            �            1259    17081 	   Clinician    TABLE     G   CREATE TABLE tingleserver."Clinician" (
    ac_id smallint NOT NULL
);
 %   DROP TABLE tingleserver."Clinician";
       tingleserver         heap    postgres    false    7            �            1259    17084    Forgot_password    TABLE     u   CREATE TABLE tingleserver."Forgot_password" (
    key character(24) NOT NULL,
    ac_email character varying(255)
);
 +   DROP TABLE tingleserver."Forgot_password";
       tingleserver         heap    postgres    false    7            �            1259    17087    Patient    TABLE     g   CREATE TABLE tingleserver."Patient" (
    ac_id smallint NOT NULL,
    consent character varying(3)
);
 #   DROP TABLE tingleserver."Patient";
       tingleserver         heap    postgres    false    7            �            1259    17090    Patient_Clinician    TABLE     x   CREATE TABLE tingleserver."Patient_Clinician" (
    patient_id smallint NOT NULL,
    clinician_id smallint NOT NULL
);
 -   DROP TABLE tingleserver."Patient_Clinician";
       tingleserver         heap    postgres    false    7            �            1259    17093    Patient_Receives_Treatment    TABLE     �   CREATE TABLE tingleserver."Patient_Receives_Treatment" (
    patient_id smallint NOT NULL,
    treatment_id smallint NOT NULL
);
 6   DROP TABLE tingleserver."Patient_Receives_Treatment";
       tingleserver         heap    postgres    false    7            �            1259    17096 
   Researcher    TABLE     ?   CREATE TABLE tingleserver."Researcher" (
    ac_id smallint
);
 &   DROP TABLE tingleserver."Researcher";
       tingleserver         heap    postgres    false    7            �            1259    17099    Symptom    TABLE     Y  CREATE TABLE tingleserver."Symptom" (
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
       tingleserver         heap    postgres    false    7            �            1259    17105    Symptom_symptom_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Symptom_symptom_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE tingleserver."Symptom_symptom_id_seq";
       tingleserver          postgres    false    7    253            �           0    0    Symptom_symptom_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE tingleserver."Symptom_symptom_id_seq" OWNED BY tingleserver."Symptom".symptom_id;
          tingleserver          postgres    false    254            �            1259    17107 	   Treatment    TABLE     �   CREATE TABLE tingleserver."Treatment" (
    treatment_id smallint NOT NULL,
    treatment_name character varying(255) NOT NULL
);
 %   DROP TABLE tingleserver."Treatment";
       tingleserver         heap    postgres    false    7                        1259    17110    Treatment_treatment_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Treatment_treatment_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE tingleserver."Treatment_treatment_id_seq";
       tingleserver          postgres    false    7    255            �           0    0    Treatment_treatment_id_seq    SEQUENCE OWNED BY     i   ALTER SEQUENCE tingleserver."Treatment_treatment_id_seq" OWNED BY tingleserver."Treatment".treatment_id;
          tingleserver          postgres    false    256            �           2604    17112    Account ac_id    DEFAULT     ~   ALTER TABLE ONLY tingleserver."Account" ALTER COLUMN ac_id SET DEFAULT nextval('tingleserver."Account_ac_id_seq"'::regclass);
 D   ALTER TABLE tingleserver."Account" ALTER COLUMN ac_id DROP DEFAULT;
       tingleserver          postgres    false    245    243            �           2604    17113    Symptom symptom_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Symptom" ALTER COLUMN symptom_id SET DEFAULT nextval('tingleserver."Symptom_symptom_id_seq"'::regclass);
 I   ALTER TABLE tingleserver."Symptom" ALTER COLUMN symptom_id DROP DEFAULT;
       tingleserver          postgres    false    254    253            �           2604    17114    Treatment treatment_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Treatment" ALTER COLUMN treatment_id SET DEFAULT nextval('tingleserver."Treatment_treatment_id_seq"'::regclass);
 M   ALTER TABLE tingleserver."Treatment" ALTER COLUMN treatment_id DROP DEFAULT;
       tingleserver          postgres    false    256    255            |          0    17064    Account 
   TABLE DATA           �   COPY tingleserver."Account" (ac_id, ac_email, ac_password, ac_firstname, ac_lastname, ac_age, ac_gender, ac_phone, ac_type) FROM stdin;
    tingleserver          postgres    false    243   �T       }          0    17070    Account_Invitation 
   TABLE DATA           K   COPY tingleserver."Account_Invitation" (token, ac_email, role) FROM stdin;
    tingleserver          postgres    false    244   ~V                 0    17078    Admin 
   TABLE DATA           .   COPY tingleserver."Admin" (ac_id) FROM stdin;
    tingleserver          postgres    false    246   �V       �          0    17081 	   Clinician 
   TABLE DATA           2   COPY tingleserver."Clinician" (ac_id) FROM stdin;
    tingleserver          postgres    false    247   �V       �          0    17084    Forgot_password 
   TABLE DATA           @   COPY tingleserver."Forgot_password" (key, ac_email) FROM stdin;
    tingleserver          postgres    false    248   �V       �          0    17087    Patient 
   TABLE DATA           9   COPY tingleserver."Patient" (ac_id, consent) FROM stdin;
    tingleserver          postgres    false    249   �V       �          0    17090    Patient_Clinician 
   TABLE DATA           M   COPY tingleserver."Patient_Clinician" (patient_id, clinician_id) FROM stdin;
    tingleserver          postgres    false    250   W       �          0    17093    Patient_Receives_Treatment 
   TABLE DATA           V   COPY tingleserver."Patient_Receives_Treatment" (patient_id, treatment_id) FROM stdin;
    tingleserver          postgres    false    251   9W       �          0    17096 
   Researcher 
   TABLE DATA           3   COPY tingleserver."Researcher" (ac_id) FROM stdin;
    tingleserver          postgres    false    252   VW       �          0    17099    Symptom 
   TABLE DATA           �   COPY tingleserver."Symptom" (symptom_id, patient_username, severity, recorded_date, symptom_name, notes, location, occurence) FROM stdin;
    tingleserver          postgres    false    253   vW       �          0    17107 	   Treatment 
   TABLE DATA           I   COPY tingleserver."Treatment" (treatment_id, treatment_name) FROM stdin;
    tingleserver          postgres    false    255   X       �           0    0    Account_ac_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('tingleserver."Account_ac_id_seq"', 67, true);
          tingleserver          postgres    false    245            �           0    0    Symptom_symptom_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('tingleserver."Symptom_symptom_id_seq"', 15, true);
          tingleserver          postgres    false    254            �           0    0    Treatment_treatment_id_seq    SEQUENCE SET     Q   SELECT pg_catalog.setval('tingleserver."Treatment_treatment_id_seq"', 1, false);
          tingleserver          postgres    false    256            �           2606    17116 *   Account_Invitation Account_Invitation_pkey 
   CONSTRAINT     u   ALTER TABLE ONLY tingleserver."Account_Invitation"
    ADD CONSTRAINT "Account_Invitation_pkey" PRIMARY KEY (token);
 ^   ALTER TABLE ONLY tingleserver."Account_Invitation" DROP CONSTRAINT "Account_Invitation_pkey";
       tingleserver            postgres    false    244            �           2606    17118    Account Account_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "Account_pkey" PRIMARY KEY (ac_id);
 H   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT "Account_pkey";
       tingleserver            postgres    false    243            �           2606    17120    Admin Admin_ac_id_key 
   CONSTRAINT     [   ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT "Admin_ac_id_key" UNIQUE (ac_id);
 I   ALTER TABLE ONLY tingleserver."Admin" DROP CONSTRAINT "Admin_ac_id_key";
       tingleserver            postgres    false    246            �           2606    17122    Clinician Clinician_ac_id_key 
   CONSTRAINT     c   ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_key" UNIQUE (ac_id);
 Q   ALTER TABLE ONLY tingleserver."Clinician" DROP CONSTRAINT "Clinician_ac_id_key";
       tingleserver            postgres    false    247            �           2606    17124    Patient Patient_ac_id_key 
   CONSTRAINT     _   ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_key" UNIQUE (ac_id);
 M   ALTER TABLE ONLY tingleserver."Patient" DROP CONSTRAINT "Patient_ac_id_key";
       tingleserver            postgres    false    249            �           2606    17126    Researcher Researcher_ac_id_key 
   CONSTRAINT     e   ALTER TABLE ONLY tingleserver."Researcher"
    ADD CONSTRAINT "Researcher_ac_id_key" UNIQUE (ac_id);
 S   ALTER TABLE ONLY tingleserver."Researcher" DROP CONSTRAINT "Researcher_ac_id_key";
       tingleserver            postgres    false    252            �           2606    17128    Treatment Treatment_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY tingleserver."Treatment"
    ADD CONSTRAINT "Treatment_pkey" PRIMARY KEY (treatment_id);
 L   ALTER TABLE ONLY tingleserver."Treatment" DROP CONSTRAINT "Treatment_pkey";
       tingleserver            postgres    false    255            �           2606    17130    Account ac_email 
   CONSTRAINT     W   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT ac_email UNIQUE (ac_email);
 B   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT ac_email;
       tingleserver            postgres    false    243            �           2606    17132    Forgot_password key 
   CONSTRAINT     Z   ALTER TABLE ONLY tingleserver."Forgot_password"
    ADD CONSTRAINT key PRIMARY KEY (key);
 E   ALTER TABLE ONLY tingleserver."Forgot_password" DROP CONSTRAINT key;
       tingleserver            postgres    false    248            �           2606    17134 .   Patient_Clinician patient_clinician_unique_key 
   CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT patient_clinician_unique_key UNIQUE (patient_id, clinician_id);
 `   ALTER TABLE ONLY tingleserver."Patient_Clinician" DROP CONSTRAINT patient_clinician_unique_key;
       tingleserver            postgres    false    250    250            �           2606    17136    Symptom symptom_id 
   CONSTRAINT     `   ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT symptom_id PRIMARY KEY (symptom_id);
 D   ALTER TABLE ONLY tingleserver."Symptom" DROP CONSTRAINT symptom_id;
       tingleserver            postgres    false    253            �           1259    17137    fki_id_key_ac_email_fkey    INDEX     `   CREATE INDEX fki_id_key_ac_email_fkey ON tingleserver."Forgot_password" USING btree (ac_email);
 2   DROP INDEX tingleserver.fki_id_key_ac_email_fkey;
       tingleserver            postgres    false    248            �           2606    17138    Admin Admin_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT "Admin_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;
 J   ALTER TABLE ONLY tingleserver."Admin" DROP CONSTRAINT "Admin_ac_id_fkey";
       tingleserver          postgres    false    246    3290    243            �           2606    17143    Clinician Clinician_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;
 R   ALTER TABLE ONLY tingleserver."Clinician" DROP CONSTRAINT "Clinician_ac_id_fkey";
       tingleserver          postgres    false    3290    247    243            �           2606    17148 E   Patient_Receives_Treatment Patient_Receives_Treatment_patient_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey" FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 y   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment" DROP CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey";
       tingleserver          postgres    false    251    3303    249            �           2606    17153 G   Patient_Receives_Treatment Patient_Receives_Treatment_treatment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey" FOREIGN KEY (treatment_id) REFERENCES tingleserver."Treatment"(treatment_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 {   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment" DROP CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey";
       tingleserver          postgres    false    3311    251    255            �           2606    17158    Patient Patient_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED NOT VALID;
 N   ALTER TABLE ONLY tingleserver."Patient" DROP CONSTRAINT "Patient_ac_id_fkey";
       tingleserver          postgres    false    243    249    3290            �           2606    17163     Researcher Researcher_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Researcher"
    ADD CONSTRAINT "Researcher_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id);
 T   ALTER TABLE ONLY tingleserver."Researcher" DROP CONSTRAINT "Researcher_ac_id_fkey";
       tingleserver          postgres    false    3290    252    243            �           2606    17168 !   Patient_Clinician clinician_id_fk    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT clinician_id_fk FOREIGN KEY (clinician_id) REFERENCES tingleserver."Clinician"(ac_id);
 S   ALTER TABLE ONLY tingleserver."Patient_Clinician" DROP CONSTRAINT clinician_id_fk;
       tingleserver          postgres    false    250    247    3298            �           2606    17173 !   Forgot_password key_ac_email_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Forgot_password"
    ADD CONSTRAINT key_ac_email_fkey FOREIGN KEY (ac_email) REFERENCES tingleserver."Account"(ac_email);
 S   ALTER TABLE ONLY tingleserver."Forgot_password" DROP CONSTRAINT key_ac_email_fkey;
       tingleserver          postgres    false    3292    243    248            �           2606    17178    Patient_Clinician patient_id_fk    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT patient_id_fk FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id);
 Q   ALTER TABLE ONLY tingleserver."Patient_Clinician" DROP CONSTRAINT patient_id_fk;
       tingleserver          postgres    false    249    250    3303            �           2606    17183    Symptom username    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT username FOREIGN KEY (patient_username) REFERENCES tingleserver."Account"(ac_email) NOT VALID;
 B   ALTER TABLE ONLY tingleserver."Symptom" DROP CONSTRAINT username;
       tingleserver          postgres    false    253    3292    243            |   r  x���Mk1��w�4�I9%��$�\�R
�����^{[��&io��އwX�Q�Ѧ�n��|S{w,����y����/�����}��*փ��K�E#Y	āU *�(�r�@�rh�7�\<{�b��ܓN��s���ug�$���4GWw�4�Q�+�_�m���諊y�	!ǐZV��-x�$#��E��c�HҠ����a3���w�X \l��iN�dg�S���m��$�?�ݪ�*����<@2�j�W̖8WL)S�e�R{Ch�E�������6�6�-��8��Ӷ�u��3����qյT�BJ�ZYa!Z��!VĜS��4tL`��d�#I As���}��������������N*�S      }      x������ � �            x�33�����       �      x�35����� -      �      x������ � �      �      x�35�L-����� �x      �      x������ � �      �      x������ � �      �      x�3������� 4       �   �   x�eα
1�9}���G{���ࠇ��KN�hS����n"������+x�2�n��6��"���к�-|��,c(أ<2����e�?Ϭd��#��9B9WDW[X5ПQ�N�p�1�1MR2���~�<�      �     x�M��j�0D��W�h�)u���MJ1�)!���J^�@����_ߕM����̮���rk~,�Ɖ$�~�*��WFk�T�@�T��PքyQ֒���t�WynSQ��[��lA�k� 楒oXښF�"9��m*^���+�'C���l�5��{�������~�$�3L���8��@�'v2N��U�o#)=G��"���<�g�oz�Ʒ��(B��d�Շ'B%�ZM�X����'�,#kV��&���)ڰ<u����t��q�� 2��/     