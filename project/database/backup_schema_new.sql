PGDMP         8            
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
                   postgres    false    3471                        2615    16507    tingleserver    SCHEMA        CREATE SCHEMA tingleserver;
    DROP SCHEMA tingleserver;
                postgres    false                       1255    16607 �   add_account(character varying, character varying, character varying, smallint, character varying, character varying, character varying, character varying, character varying)    FUNCTION     �  CREATE FUNCTION tingleserver.add_account(first_name character varying, last_name character varying, gender character varying, age smallint, mobile character varying, email character varying, password_hash character varying, user_role character varying, consent character varying) RETURNS smallint
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
       tingleserver          postgres    false    8            �            1259    16509    Account    TABLE     �  CREATE TABLE tingleserver."Account" (
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
       tingleserver         heap    postgres    false    8            �            1259    16642    Account_Invitation    TABLE     �   CREATE TABLE tingleserver."Account_Invitation" (
    token character varying(255) NOT NULL,
    ac_email character varying(255) NOT NULL,
    role character varying(20) NOT NULL
);
 .   DROP TABLE tingleserver."Account_Invitation";
       tingleserver         heap    postgres    false    8            �            1259    16515    Account_ac_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Account_ac_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE tingleserver."Account_ac_id_seq";
       tingleserver          postgres    false    8    203            �           0    0    Account_ac_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE tingleserver."Account_ac_id_seq" OWNED BY tingleserver."Account".ac_id;
          tingleserver          postgres    false    204            �            1259    16517    Admin    TABLE     C   CREATE TABLE tingleserver."Admin" (
    ac_id smallint NOT NULL
);
 !   DROP TABLE tingleserver."Admin";
       tingleserver         heap    postgres    false    8            �            1259    16520 	   Clinician    TABLE     G   CREATE TABLE tingleserver."Clinician" (
    ac_id smallint NOT NULL
);
 %   DROP TABLE tingleserver."Clinician";
       tingleserver         heap    postgres    false    8            �            1259    16523    Forgot_password    TABLE     u   CREATE TABLE tingleserver."Forgot_password" (
    key character(24) NOT NULL,
    ac_email character varying(255)
);
 +   DROP TABLE tingleserver."Forgot_password";
       tingleserver         heap    postgres    false    8            �            1259    16526    Patient    TABLE     g   CREATE TABLE tingleserver."Patient" (
    ac_id smallint NOT NULL,
    consent character varying(3)
);
 #   DROP TABLE tingleserver."Patient";
       tingleserver         heap    postgres    false    8            �            1259    16627    Patient_Clinician    TABLE     x   CREATE TABLE tingleserver."Patient_Clinician" (
    patient_id smallint NOT NULL,
    clinician_id smallint NOT NULL
);
 -   DROP TABLE tingleserver."Patient_Clinician";
       tingleserver         heap    postgres    false    8            �            1259    16529    Patient_Receives_Treatment    TABLE     �   CREATE TABLE tingleserver."Patient_Receives_Treatment" (
    patient_id smallint NOT NULL,
    treatment_id smallint NOT NULL
);
 6   DROP TABLE tingleserver."Patient_Receives_Treatment";
       tingleserver         heap    postgres    false    8            �            1259    16608 
   Researcher    TABLE     ?   CREATE TABLE tingleserver."Researcher" (
    ac_id smallint
);
 &   DROP TABLE tingleserver."Researcher";
       tingleserver         heap    postgres    false    8            �            1259    16532    Symptom    TABLE     Y  CREATE TABLE tingleserver."Symptom" (
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
       tingleserver         heap    postgres    false    8            �            1259    16538    Symptom_symptom_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Symptom_symptom_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE tingleserver."Symptom_symptom_id_seq";
       tingleserver          postgres    false    210    8            �           0    0    Symptom_symptom_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE tingleserver."Symptom_symptom_id_seq" OWNED BY tingleserver."Symptom".symptom_id;
          tingleserver          postgres    false    211            �            1259    16540 	   Treatment    TABLE     �   CREATE TABLE tingleserver."Treatment" (
    treatment_id smallint NOT NULL,
    treatment_name character varying(255) NOT NULL
);
 %   DROP TABLE tingleserver."Treatment";
       tingleserver         heap    postgres    false    8            �            1259    16543    Treatment_treatment_id_seq    SEQUENCE     �   CREATE SEQUENCE tingleserver."Treatment_treatment_id_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE tingleserver."Treatment_treatment_id_seq";
       tingleserver          postgres    false    8    212            �           0    0    Treatment_treatment_id_seq    SEQUENCE OWNED BY     i   ALTER SEQUENCE tingleserver."Treatment_treatment_id_seq" OWNED BY tingleserver."Treatment".treatment_id;
          tingleserver          postgres    false    213            �           2604    16545    Account ac_id    DEFAULT     ~   ALTER TABLE ONLY tingleserver."Account" ALTER COLUMN ac_id SET DEFAULT nextval('tingleserver."Account_ac_id_seq"'::regclass);
 D   ALTER TABLE tingleserver."Account" ALTER COLUMN ac_id DROP DEFAULT;
       tingleserver          postgres    false    204    203            �           2604    16546    Symptom symptom_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Symptom" ALTER COLUMN symptom_id SET DEFAULT nextval('tingleserver."Symptom_symptom_id_seq"'::regclass);
 I   ALTER TABLE tingleserver."Symptom" ALTER COLUMN symptom_id DROP DEFAULT;
       tingleserver          postgres    false    211    210            �           2604    16547    Treatment treatment_id    DEFAULT     �   ALTER TABLE ONLY tingleserver."Treatment" ALTER COLUMN treatment_id SET DEFAULT nextval('tingleserver."Treatment_treatment_id_seq"'::regclass);
 M   ALTER TABLE tingleserver."Treatment" ALTER COLUMN treatment_id DROP DEFAULT;
       tingleserver          postgres    false    213    212            |          0    16509    Account 
   TABLE DATA           �   COPY tingleserver."Account" (ac_id, ac_email, ac_password, ac_firstname, ac_lastname, ac_age, ac_gender, ac_phone, ac_type) FROM stdin;
    tingleserver          postgres    false    203   �T       �          0    16642    Account_Invitation 
   TABLE DATA           K   COPY tingleserver."Account_Invitation" (token, ac_email, role) FROM stdin;
    tingleserver          postgres    false    216   �W       ~          0    16517    Admin 
   TABLE DATA           .   COPY tingleserver."Admin" (ac_id) FROM stdin;
    tingleserver          postgres    false    205   �W                 0    16520 	   Clinician 
   TABLE DATA           2   COPY tingleserver."Clinician" (ac_id) FROM stdin;
    tingleserver          postgres    false    206   X       �          0    16523    Forgot_password 
   TABLE DATA           @   COPY tingleserver."Forgot_password" (key, ac_email) FROM stdin;
    tingleserver          postgres    false    207   ?X       �          0    16526    Patient 
   TABLE DATA           9   COPY tingleserver."Patient" (ac_id, consent) FROM stdin;
    tingleserver          postgres    false    208   \X       �          0    16627    Patient_Clinician 
   TABLE DATA           M   COPY tingleserver."Patient_Clinician" (patient_id, clinician_id) FROM stdin;
    tingleserver          postgres    false    215   �X       �          0    16529    Patient_Receives_Treatment 
   TABLE DATA           V   COPY tingleserver."Patient_Receives_Treatment" (patient_id, treatment_id) FROM stdin;
    tingleserver          postgres    false    209   �X       �          0    16608 
   Researcher 
   TABLE DATA           3   COPY tingleserver."Researcher" (ac_id) FROM stdin;
    tingleserver          postgres    false    214   �X       �          0    16532    Symptom 
   TABLE DATA           �   COPY tingleserver."Symptom" (symptom_id, patient_username, severity, recorded_date, symptom_name, notes, location, occurence) FROM stdin;
    tingleserver          postgres    false    210   �X       �          0    16540 	   Treatment 
   TABLE DATA           I   COPY tingleserver."Treatment" (treatment_id, treatment_name) FROM stdin;
    tingleserver          postgres    false    212   �Y       �           0    0    Account_ac_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('tingleserver."Account_ac_id_seq"', 72, true);
          tingleserver          postgres    false    204            �           0    0    Symptom_symptom_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('tingleserver."Symptom_symptom_id_seq"', 22, true);
          tingleserver          postgres    false    211            �           0    0    Treatment_treatment_id_seq    SEQUENCE SET     Q   SELECT pg_catalog.setval('tingleserver."Treatment_treatment_id_seq"', 1, false);
          tingleserver          postgres    false    213            �           2606    16649 *   Account_Invitation Account_Invitation_pkey 
   CONSTRAINT     u   ALTER TABLE ONLY tingleserver."Account_Invitation"
    ADD CONSTRAINT "Account_Invitation_pkey" PRIMARY KEY (token);
 ^   ALTER TABLE ONLY tingleserver."Account_Invitation" DROP CONSTRAINT "Account_Invitation_pkey";
       tingleserver            postgres    false    216            �           2606    16551    Account Account_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT "Account_pkey" PRIMARY KEY (ac_id);
 H   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT "Account_pkey";
       tingleserver            postgres    false    203            �           2606    16624    Admin Admin_ac_id_key 
   CONSTRAINT     [   ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT "Admin_ac_id_key" UNIQUE (ac_id);
 I   ALTER TABLE ONLY tingleserver."Admin" DROP CONSTRAINT "Admin_ac_id_key";
       tingleserver            postgres    false    205            �           2606    16622    Clinician Clinician_ac_id_key 
   CONSTRAINT     c   ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_key" UNIQUE (ac_id);
 Q   ALTER TABLE ONLY tingleserver."Clinician" DROP CONSTRAINT "Clinician_ac_id_key";
       tingleserver            postgres    false    206            �           2606    16553    Patient Patient_ac_id_key 
   CONSTRAINT     _   ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_key" UNIQUE (ac_id);
 M   ALTER TABLE ONLY tingleserver."Patient" DROP CONSTRAINT "Patient_ac_id_key";
       tingleserver            postgres    false    208            �           2606    16626    Researcher Researcher_ac_id_key 
   CONSTRAINT     e   ALTER TABLE ONLY tingleserver."Researcher"
    ADD CONSTRAINT "Researcher_ac_id_key" UNIQUE (ac_id);
 S   ALTER TABLE ONLY tingleserver."Researcher" DROP CONSTRAINT "Researcher_ac_id_key";
       tingleserver            postgres    false    214            �           2606    16555    Treatment Treatment_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY tingleserver."Treatment"
    ADD CONSTRAINT "Treatment_pkey" PRIMARY KEY (treatment_id);
 L   ALTER TABLE ONLY tingleserver."Treatment" DROP CONSTRAINT "Treatment_pkey";
       tingleserver            postgres    false    212            �           2606    16557    Account ac_email 
   CONSTRAINT     W   ALTER TABLE ONLY tingleserver."Account"
    ADD CONSTRAINT ac_email UNIQUE (ac_email);
 B   ALTER TABLE ONLY tingleserver."Account" DROP CONSTRAINT ac_email;
       tingleserver            postgres    false    203            �           2606    16559    Forgot_password key 
   CONSTRAINT     Z   ALTER TABLE ONLY tingleserver."Forgot_password"
    ADD CONSTRAINT key PRIMARY KEY (key);
 E   ALTER TABLE ONLY tingleserver."Forgot_password" DROP CONSTRAINT key;
       tingleserver            postgres    false    207            �           2606    16631 .   Patient_Clinician patient_clinician_unique_key 
   CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT patient_clinician_unique_key UNIQUE (patient_id, clinician_id);
 `   ALTER TABLE ONLY tingleserver."Patient_Clinician" DROP CONSTRAINT patient_clinician_unique_key;
       tingleserver            postgres    false    215    215            �           2606    16561    Symptom symptom_id 
   CONSTRAINT     `   ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT symptom_id PRIMARY KEY (symptom_id);
 D   ALTER TABLE ONLY tingleserver."Symptom" DROP CONSTRAINT symptom_id;
       tingleserver            postgres    false    210            �           1259    16562    fki_id_key_ac_email_fkey    INDEX     `   CREATE INDEX fki_id_key_ac_email_fkey ON tingleserver."Forgot_password" USING btree (ac_email);
 2   DROP INDEX tingleserver.fki_id_key_ac_email_fkey;
       tingleserver            postgres    false    207            �           2606    16563    Admin Admin_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Admin"
    ADD CONSTRAINT "Admin_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;
 J   ALTER TABLE ONLY tingleserver."Admin" DROP CONSTRAINT "Admin_ac_id_fkey";
       tingleserver          postgres    false    205    203    3290            �           2606    16568    Clinician Clinician_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Clinician"
    ADD CONSTRAINT "Clinician_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) NOT VALID;
 R   ALTER TABLE ONLY tingleserver."Clinician" DROP CONSTRAINT "Clinician_ac_id_fkey";
       tingleserver          postgres    false    3290    203    206            �           2606    16573 E   Patient_Receives_Treatment Patient_Receives_Treatment_patient_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey" FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 y   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment" DROP CONSTRAINT "Patient_Receives_Treatment_patient_id_fkey";
       tingleserver          postgres    false    3301    209    208            �           2606    16578 G   Patient_Receives_Treatment Patient_Receives_Treatment_treatment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment"
    ADD CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey" FOREIGN KEY (treatment_id) REFERENCES tingleserver."Treatment"(treatment_id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;
 {   ALTER TABLE ONLY tingleserver."Patient_Receives_Treatment" DROP CONSTRAINT "Patient_Receives_Treatment_treatment_id_fkey";
       tingleserver          postgres    false    3305    212    209            �           2606    16583    Patient Patient_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient"
    ADD CONSTRAINT "Patient_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED NOT VALID;
 N   ALTER TABLE ONLY tingleserver."Patient" DROP CONSTRAINT "Patient_ac_id_fkey";
       tingleserver          postgres    false    3290    203    208            �           2606    16611     Researcher Researcher_ac_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Researcher"
    ADD CONSTRAINT "Researcher_ac_id_fkey" FOREIGN KEY (ac_id) REFERENCES tingleserver."Account"(ac_id);
 T   ALTER TABLE ONLY tingleserver."Researcher" DROP CONSTRAINT "Researcher_ac_id_fkey";
       tingleserver          postgres    false    214    203    3290            �           2606    16632 !   Patient_Clinician clinician_id_fk    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT clinician_id_fk FOREIGN KEY (clinician_id) REFERENCES tingleserver."Clinician"(ac_id);
 S   ALTER TABLE ONLY tingleserver."Patient_Clinician" DROP CONSTRAINT clinician_id_fk;
       tingleserver          postgres    false    206    215    3296            �           2606    16588 !   Forgot_password key_ac_email_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Forgot_password"
    ADD CONSTRAINT key_ac_email_fkey FOREIGN KEY (ac_email) REFERENCES tingleserver."Account"(ac_email);
 S   ALTER TABLE ONLY tingleserver."Forgot_password" DROP CONSTRAINT key_ac_email_fkey;
       tingleserver          postgres    false    3292    203    207            �           2606    16637    Patient_Clinician patient_id_fk    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Patient_Clinician"
    ADD CONSTRAINT patient_id_fk FOREIGN KEY (patient_id) REFERENCES tingleserver."Patient"(ac_id);
 Q   ALTER TABLE ONLY tingleserver."Patient_Clinician" DROP CONSTRAINT patient_id_fk;
       tingleserver          postgres    false    215    3301    208            �           2606    16593    Symptom username    FK CONSTRAINT     �   ALTER TABLE ONLY tingleserver."Symptom"
    ADD CONSTRAINT username FOREIGN KEY (patient_username) REFERENCES tingleserver."Account"(ac_email) NOT VALID;
 B   ALTER TABLE ONLY tingleserver."Symptom" DROP CONSTRAINT username;
       tingleserver          postgres    false    3292    203    210            |   �  x���Oo7���O�ÜQ�H)��p�&@�6qb�ȅ�({����u�|�h׎�(v �f ��=>&rw���z�zo��˺Y�;]�^�n%$zɏg��_w��ŧI��k)*MCL!	e@$��� �Qh�AQ�<%5A5�^���7�br��J��|��1�4�Į.��y���ڷ��߾���W!��3B�[�H�-�X"%��0�8h�p��A��	�����-y��X l!>��Rv[ۙl�mO����׿�˩�J T��<@��Ų�X,�R1�K�dQko� ul�Ðm� �'6�-��pfN�j~J��d�_�M]���r�j:I�h�R�=pE,%������#j�#�Hh�͡�{S��~�w�<�aiy �Qv�`B����b3�_Ve��*����D9�Ә�q/��!�69C���NV���=j��d��4hT��P�ϭܿ�Y�|��pv�J�wS��#7�dU��P�b)J+�T���e����=v_���(� �Xg���kٙ�ܗ�3݃d쏒�	���˛���)Q�8�F�� 5$��LMcbI �> A#d�Z�Ň6ҫ��6��A��u ��$���;���M5��rA�R����T0q�8&�w��[O�- �<�X��Xt�dt���x�M�x���We���لL�E��H	k�Fu�E���i � �Ʋj�bc�2H���=�����ף����l6�e�<      �      x������ � �      ~      x�33�2��27�27����� @v            x�35�27����� 
��      �      x������ � �      �      x�35�L-�2� S1z\\\ /�J      �      x�35�45����� 
��      �      x������ � �      �      x�3������� 4       �   
  x���MK�0���_17O.m�z����ʊ�i/I;n���t��o�U˶�Br�yޏl	�59�bjxQz��Ҿ�"�iO/��L� ��U�e��R�����Z̈́��<�V9j�"�#
4���#jm�v ��k��%�%�k�ˋ��M�J*��[�KBh;d��e��1�5�����>+G�c�;ƽlP�j7D<a�&�W
ڶ�G�rl�8���Id:Y�ڻ�@���0yb凰����-�����|��5:�lI�|*��3      �     x�M��j�0D��W�h�)u���MJ1�)!���J^�@����_ߕM����̮���rk~,�Ɖ$�~�*��WFk�T�@�T��PքyQ֒���t�WynSQ��[��lA�k� 楒oXښF�"9��m*^���+�'C���l�5��{�������~�$�3L���8��@�'v2N��U�o#)=G��"���<�g�oz�Ʒ��(B��d�Շ'B%�ZM�X����'�,#kV��&���)ڰ<u����t��q�� 2��/     