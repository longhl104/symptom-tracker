PGDMP         /            
    x           postgres    13.0    13.0 J    '           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            (           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            )           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            *           1262    13707    postgres    DATABASE     S   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'C';
    DROP DATABASE postgres;
                postgres    false            +           0    0    DATABASE postgres    COMMENT     N   COMMENT ON DATABASE postgres IS 'default administrative connection database';
                   postgres    false    3370                        2615    17062    tingleserver    SCHEMA        CREATE SCHEMA tingleserver;
    DROP SCHEMA tingleserver;
                postgres    false            �            1255    24576 �   add_account(character varying, character varying, character varying, date, character varying, character varying, character varying, character varying, character varying)    FUNCTION     f  CREATE FUNCTION tingleserver.add_account(first_name character varying, last_name character varying, gender character varying, dob date, mobile character varying, email character varying, password_hash character varying, user_role character varying, consent character varying) RETURNS smallint
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
   DROP FUNCTION tingleserver.add_account(first_name character varying, last_name character varying, gender character varying, dob date, mobile character varying, email character varying, password_hash character varying, user_role character varying, consent character varying);
       tingleserver          postgres    false    5            �            1259    17064    Account    TABLE     �  CREATE TABLE tingleserver."Account" (
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
 #   DROP TABLE tingleserver."Account";
       tingleserver         heap    postgres    false    5            �            1259    17070    Account_Invitation    TABLE     �   CREATE TABLE tingleserver."Account_Invitation" (
    token character varying(255) NOT NULL,
    ac_email character varying(255) NOT NULL,
    role character varying(20) NOT NULL
);
 .   DROP TABLE tingleserver."Account_Invitation";
       tingleserver         heap    postgres    false    5            �            1259    17076    Account_ac_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Account_ac_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE tingleserver."Account_ac_id_seq";
       tingleserver          postgres    false    201    5            ,           0    0    Account_ac_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE tingleserver."Account_ac_id_seq" OWNED BY tingleserver."Account".ac_id;
          tingleserver          postgres    false    203            �            1259    17078    Admin    TABLE     C   CREATE TABLE tingleserver."Admin" (
    ac_id smallint NOT NULL
);
 !   DROP TABLE tingleserver."Admin";
       tingleserver         heap    postgres    false    5            �            1259    17081 	   Clinician    TABLE     G   CREATE TABLE tingleserver."Clinician" (
    ac_id smallint NOT NULL
);
 %   DROP TABLE tingleserver."Clinician";
       tingleserver         heap    postgres    false    5            �            1259    17084    Forgot_password    TABLE     u   CREATE TABLE tingleserver."Forgot_password" (
    key character(24) NOT NULL,
    ac_email character varying(255)
);
 +   DROP TABLE tingleserver."Forgot_password";
       tingleserver         heap    postgres    false    5            �            1259    17087    Patient    TABLE     g   CREATE TABLE tingleserver."Patient" (
    ac_id smallint NOT NULL,
    consent character varying(3)
);
 #   DROP TABLE tingleserver."Patient";
       tingleserver         heap    postgres    false    5            �            1259    17090    Patient_Clinician    TABLE     x   CREATE TABLE tingleserver."Patient_Clinician" (
    patient_id smallint NOT NULL,
    clinician_id smallint NOT NULL
);
 -   DROP TABLE tingleserver."Patient_Clinician";
       tingleserver         heap    postgres    false    5            �            1259    17222    Patient_Receives_Questionnaire    TABLE     �   CREATE TABLE tingleserver."Patient_Receives_Questionnaire" (
    ac_id smallint NOT NULL,
    questionnaire_id smallint NOT NULL,
    opened boolean DEFAULT false NOT NULL,
    completed boolean DEFAULT false NOT NULL
);
 :   DROP TABLE tingleserver."Patient_Receives_Questionnaire";
       tingleserver         heap    postgres    false    5            �            1259    17093    Patient_Receives_Treatment    TABLE     �   CREATE TABLE tingleserver."Patient_Receives_Treatment" (
    patient_id smallint NOT NULL,
    treatment_id smallint NOT NULL
);
 6   DROP TABLE tingleserver."Patient_Receives_Treatment";
       tingleserver         heap    postgres    false    5            �            1259    17188    Questionnaire    TABLE     �   CREATE TABLE tingleserver."Questionnaire" (
    name character varying(255) NOT NULL,
    link character varying(255) NOT NULL,
    end_date date NOT NULL,
    id integer NOT NULL
);
 )   DROP TABLE tingleserver."Questionnaire";
       tingleserver         heap    postgres    false    5            �            1259    17204    Questionnaire_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Questionnaire_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE tingleserver."Questionnaire_id_seq";
       tingleserver          postgres    false    5    215            -           0    0    Questionnaire_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE tingleserver."Questionnaire_id_seq" OWNED BY tingleserver."Questionnaire".id;
          tingleserver          postgres    false    216            �            1259    17096 
   Researcher    TABLE     ?   CREATE TABLE tingleserver."Researcher" (
    ac_id smallint
);
 &   DROP TABLE tingleserver."Researcher";
       tingleserver         heap    postgres    false    5            �            1259    17099    Symptom    TABLE     Y  CREATE TABLE tingleserver."Symptom" (
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
       tingleserver         heap    postgres    false    5            �            1259    17105    Symptom_symptom_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Symptom_symptom_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE tingleserver."Symptom_symptom_id_seq";
       tingleserver          postgres    false    211    5            .           0    0    Symptom_symptom_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE tingleserver."Symptom_symptom_id_seq" OWNED BY tingleserver."Symptom".symptom_id;
          tingleserver          postgres    false    212            �            1259    17107 	   Treatment    TABLE     �   CREATE TABLE tingleserver."Treatment" (
    treatment_id smallint NOT NULL,
    treatment_name character varying(255) NOT NULL
);
 %   DROP TABLE tingleserver."Treatment";
       tingleserver         heap    postgres    false    5            �            1259    17110    Treatment_treatment_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Treatment_treatment_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE tingleserver."Treatment_treatment_id_seq";
       tingleserver          postgres    false    5    213            /           0    0    Treatment_treatment_id_seq    SEQUENCE OWNED BY     i   ALTER SEQUENCE tingleserver."Treatment_treatment_id_seq" OWNED BY tingleserver."Treatment".treatment_id;
          tingleserver          postgres    false    214            g           2604    17112    Account ac_id    DEFAULT     ~   ALTER TABLE ONLY tingleserver."Account" ALTER COLUMN ac_id SET DEFAULT nextval('tingleserver."Account_ac_id_seq"'::regclass);
 D   ALTER TABLE tingleserver."Account" ALTER COLUMN ac_id DROP DEFAULT;
       tingleserver          postgres    false    203    201            j           2604    17206    Questionnaire id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Questionnaire" ALTER COLUMN id SET DEFAULT nextval('tingleserver."Questionnaire_id_seq"'::regclass);
 G   ALTER TABLE tingleserver."Questionnaire" ALTER COLUMN id DROP DEFAULT;
       tingleserver          postgres    false    216    215            h           2604    17113    Symptom symptom_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Symptom" ALTER COLUMN symptom_id SET DEFAULT nextval('tingleserver."Symptom_symptom_id_seq"'::regclass);
 I   ALTER TABLE tingleserver."Symptom" ALTER COLUMN symptom_id DROP DEFAULT;
       tingleserver          postgres    false    212    211            i           2604    17114    Treatment treatment_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Treatment" ALTER COLUMN treatment_id SET DEFAULT nextval('tingleserver."Treatment_treatment_id_seq"'::regclass);
 M   ALTER TABLE tingleserver."Treatment" ALTER COLUMN treatment_id DROP DEFAULT;
       tingleserver          postgres    false    214    213                      0    17064    Account 
   TABLE DATA           �   COPY tingleserver."Account" (ac_id, ac_email, ac_password, ac_firstname, ac_lastname, ac_gender, ac_phone, ac_type, ac_dob) FROM stdin;
    tingleserver          postgres    false    201   Bc                 0    17070    Account_Invitation 
   TABLE DATA           K   COPY tingleserver."Account_Invitation" (token, ac_email, role) FROM stdin;
    tingleserver          postgres    false    202   �d                 0    17078    Admin 
   TABLE DATA           .   COPY tingleserver."Admin" (ac_id) FROM stdin;
    tingleserver          postgres    false    204   �d                 0    17081 	   Clinician 
   TABLE DATA           2   COPY tingleserver."Clinician" (ac_id) FROM stdin;
    tingleserver          postgres    false    205   �d                 0    17084    Forgot_password 
   TABLE DATA           @   COPY tingleserver."Forgot_password" (key, ac_email) FROM stdin;
    tingleserver          postgres    false    206   e                 0    17087    Patient 
   TABLE DATA           9   COPY tingleserver."Patient" (ac_id, consent) FROM stdin;
    tingleserver          postgres    false    207   <e                 0    17090    Patient_Clinician 
   TABLE DATA           M   COPY tingleserver."Patient_Clinician" (patient_id, clinician_id) FROM stdin;
    tingleserver          postgres    false    208   `e       $          0    17222    Patient_Receives_Questionnaire 
   TABLE DATA           l   COPY tingleserver."Patient_Receives_Questionnaire" (ac_id, questionnaire_id, opened, completed) FROM stdin;
    tingleserver          postgres    false    217   }e                 0    17093    Patient_Receives_Treatment 
   TABLE DATA           V   COPY tingleserver."Patient_Receives_Treatment" (patient_id, treatment_id) FROM stdin;
    tingleserver          postgres    false    209   �e       "          0    17188    Questionnaire 
   TABLE DATA           I   COPY tingleserver."Questionnaire" (name, link, end_date, id) FROM stdin;
    tingleserver          postgres    false    215   �e                 0    17096 
   Researcher 
   TABLE DATA           3   COPY tingleserver."Researcher" (ac_id) FROM stdin;
    tingleserver          postgres    false    210   �e                 0    17099    Symptom 
   TABLE DATA           �   COPY tingleserver."Symptom" (symptom_id, patient_username, severity, recorded_date, symptom_name, notes, location, occurence) FROM stdin;
    tingleserver          postgres    false    211   �e                  0    17107 	   Treatment 
   TABLE DATA           I   COPY tingleserver."Treatment" (treatment_id, treatment_name) FROM stdin;
    tingleserver          postgres    false    213   �f       0           0    0    Account_ac_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('tingleserver."Account_ac_id_seq"', 82, true);
          tingleserver          postgres    false    203            1           0    0    Questionnaire_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('tingleserver."Questionnaire_id_seq"', 62, true);
          tingleserver          postgres    false    216            2           0    0    Symptom_symptom_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('tingleserver."Symptom_symptom_id_seq"', 17, true);
          tingleserver          postgres    false    212            3           0    0    Treatment_treatment_id_seq    SEQUENCE SET     Q   SELECT pg_catalog.setval('tingleserver."Treatment_treatment_id_seq"', 1, false);
          tingleserver          postgres    false    214            r           2606    17116 *   Account_Invitation Account_Invitation_pkey 
   CONSTRAINT     u   ALTER TABLE ONLY tingleserver."Account_Invitation"
    ADD CONSTRAINT "Account_Invitation_pkey" PRIMARY KEY (token);
 ^   ALTER TABLE ONLY tingleserver."Account_Invitation" DROP CONSTRAINT "Account_Invitation_pkey";
       tingleserver            postgres    false    202            n           2606    17118    Account Account_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "Account_pkey" PRIMARY KEY (ac_id);
 H   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT "Account_pkey";
       tingleserver            postgres    false    201            t           2606    17120    Admin Admin_ac_id_key 
   CONSTRAINT     [   ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT "Admin_ac_id_key" UNIQUE (ac_id);
 I   ALTER TABLE ONLY tingleserver."Admin" DROP CONSTRAINT "Admin_ac_id_key";
       tingleserver            postgres    false    204            v           2606    17122    Clinician Clinician_ac_id_key 
   CONSTRAINT     c   ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_key" UNIQUE (ac_id);
 Q   ALTER TABLE ONLY tingleserver."Clinician" DROP CONSTRAINT "Clinician_ac_id_key";
       tingleserver            postgres    false    205            {           2606    17124    Patient Patient_ac_id_key 
   CONSTRAINT     _   ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_key" UNIQUE (ac_id);
 M   ALTER TABLE ONLY tingleserver."Patient" DROP CONSTRAINT "Patient_ac_id_key";
       tingleserver            postgres    false    207                       2606    17126    Researcher Researcher_ac_id_key 
   CONSTRAINT     e   ALTER TABLE ONLY tingleserver."Researcher"
    ADD CONSTRAINT "Researcher_ac_id_key" UNIQUE (ac_id);
 S   ALTER TABLE ONLY tingleserver."Researcher" DROP CONSTRAINT "Researcher_ac_id_key";
       tingleserver            postgres    false    210            �           2606    17128    Treatment Treatment_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY tingleserver."Treatment"
    ADD CONSTRAINT "Treatment_pkey" PRIMARY KEY (treatment_id);
 L   ALTER TABLE ONLY tingleserver."Treatment" DROP CONSTRAINT "Treatment_pkey";
       tingleserver            postgres    false    213            p           2606    17130    Account ac_email 
   CONSTRAINT     W   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT ac_email UNIQUE (ac_email);
 B   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT ac_email;
       tingleserver            postgres    false    201            �           2606    17216    Questionnaire id 
   CONSTRAINT     V   ALTER TABLE ONLY tingleserver."Questionnaire"
    ADD CONSTRAINT id PRIMARY KEY (id);
 B   ALTER TABLE ONLY tingleserver."Questionnaire" DROP CONSTRAINT id;
       tingleserver            postgres    false    215            y           2606    17132    Forgot_password key 
   CONSTRAINT     Z   ALTER TABLE ONLY tingleserver."Forgot_password"
    ADD CONSTRAINT key PRIMARY KEY (key);
 E   ALTER TABLE ONLY tingleserver."Forgot_password" DROP CONSTRAINT key;
       tingleserver            postgres    false    206            }           2606    17134 .   Patient_Clinician patient_clinician_unique_key 
   CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT patient_clinician_unique_key UNIQUE (patient_id, clinician_id);
 `   ALTER TABLE ONLY tingleserver."Patient_Clinician" DROP CONSTRAINT patient_clinician_unique_key;
       tingleserver            postgres    false    208    208            �           2606    17136    Symptom symptom_id 
   CONSTRAINT     `   ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT symptom_id PRIMARY KEY (symptom_id);
 D   ALTER TABLE ONLY tingleserver."Symptom" DROP CONSTRAINT symptom_id;
       tingleserver            postgres    false    211            w           1259    17137    fki_id_key_ac_email_fkey    INDEX     `   CREATE INDEX fki_id_key_ac_email_fkey ON tingleserver."Forgot_password" USING btree (ac_email);
 2   DROP INDEX tingleserver.fki_id_key_ac_email_fkey;
       tingleserver            postgres    false    206            �           2606    17138    Admin Admin_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT "Admin_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;
 J   ALTER TABLE ONLY tingleserver."Admin" DROP CONSTRAINT "Admin_ac_id_fkey";
       tingleserver          postgres    false    3182    204    201            �           2606    17143    Clinician Clinician_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;
 R   ALTER TABLE ONLY tingleserver."Clinician" DROP CONSTRAINT "Clinician_ac_id_fkey";
       tingleserver          postgres    false    201    3182    205            �           2606    17148 E   Patient_Receives_Treatment Patient_Receives_Treatment_patient_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey" FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 y   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment" DROP CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey";
       tingleserver          postgres    false    209    3195    207            �           2606    17153 G   Patient_Receives_Treatment Patient_Receives_Treatment_treatment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey" FOREIGN KEY (treatment_id) REFERENCES tingleserver."Treatment"(treatment_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 {   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment" DROP CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey";
       tingleserver          postgres    false    209    3203    213            �           2606    17158    Patient Patient_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED NOT VALID;
 N   ALTER TABLE ONLY tingleserver."Patient" DROP CONSTRAINT "Patient_ac_id_fkey";
       tingleserver          postgres    false    207    3182    201            �           2606    17163     Researcher Researcher_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Researcher"
    ADD CONSTRAINT "Researcher_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id);
 T   ALTER TABLE ONLY tingleserver."Researcher" DROP CONSTRAINT "Researcher_ac_id_fkey";
       tingleserver          postgres    false    210    201    3182            �           2606    17168 !   Patient_Clinician clinician_id_fk    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT clinician_id_fk FOREIGN KEY (clinician_id) REFERENCES tingleserver."Clinician"(ac_id);
 S   ALTER TABLE ONLY tingleserver."Patient_Clinician" DROP CONSTRAINT clinician_id_fk;
       tingleserver          postgres    false    205    3190    208            �           2606    17173 !   Forgot_password key_ac_email_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Forgot_password"
    ADD CONSTRAINT key_ac_email_fkey FOREIGN KEY (ac_email) REFERENCES tingleserver."Account"(ac_email);
 S   ALTER TABLE ONLY tingleserver."Forgot_password" DROP CONSTRAINT key_ac_email_fkey;
       tingleserver          postgres    false    201    3184    206            �           2606    17225 )   Patient_Receives_Questionnaire patient_fk    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Questionnaire"
    ADD CONSTRAINT patient_fk FOREIGN KEY (ac_id) REFERENCES tingleserver."Patient"(ac_id);
 [   ALTER TABLE ONLY tingleserver."Patient_Receives_Questionnaire" DROP CONSTRAINT patient_fk;
       tingleserver          postgres    false    3195    217    207            �           2606    17178    Patient_Clinician patient_id_fk    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT patient_id_fk FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id);
 Q   ALTER TABLE ONLY tingleserver."Patient_Clinician" DROP CONSTRAINT patient_id_fk;
       tingleserver          postgres    false    208    207    3195            �           2606    17230 /   Patient_Receives_Questionnaire questionnaire_fk    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Questionnaire"
    ADD CONSTRAINT questionnaire_fk FOREIGN KEY (questionnaire_id) REFERENCES tingleserver."Questionnaire"(id);
 a   ALTER TABLE ONLY tingleserver."Patient_Receives_Questionnaire" DROP CONSTRAINT questionnaire_fk;
       tingleserver          postgres    false    217    3205    215            �           2606    17183    Symptom username    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT username FOREIGN KEY (patient_username) REFERENCES tingleserver."Account"(ac_email) NOT VALID;
 B   ALTER TABLE ONLY tingleserver."Symptom" DROP CONSTRAINT username;
       tingleserver          postgres    false    201    3184    211               p  x����j1��{�4�䔀[�@}iK)�2�Fxc{m��B߾r�i{��00�ȜduZ=/w�x0����ݟ���C�}��~=O�ͷ!ks�R��Y���|pA(� ��	���f[8�`)d�j�eR�>���٫��@1])�e�
є�8�e�������O�!�"��ZB��Re��:��S��{�Y:j�؀,z�PK�������h��a�ۜ�Ky�%3�Ye.[�o��_fz���R
���X����&[�5.�{}'����P	B#�,��v��]�%��r����Vf߿�̟��&��mR�EsO$���a�6"sj-Tqh���r��<����7�X��go���R~�\d/w���t�e            x������ � �            x�33�����             x�35����� -            x������ � �            x�35�L-����� �x            x������ � �      $      x������ � �            x�35�4����� �X      "      x������ � �            x�3������� 4          �   x�����@�뽧� �?�$J4P���M��xK�o�ch��6��o�p7��d/�%����ҳ7:�i�A4�!,@i��Ca^�����B��Z�"�T�my�@dKD,2�#d�;�u��ÅB
��1�4�Aky]|4_0T��υ.�R�U)U/            x�M��j�0D��W�h�)u���MJ1�)!���J^�@����_ߕM����̮���rk~,�Ɖ$�~�*��WFk�T�@�T��PքyQ֒���t�WynSQ��[��lA�k� 楒oXښF�"9��m*^���+�'C���l�5��{�������~�$�3L���8��@�'v2N��U�o#)=G��"���<�g�oz�Ʒ��(B��d�Շ'B%�ZM�X����'�,#kV��&���)ڰ<u����t��q�� 2��/     