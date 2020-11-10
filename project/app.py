from flask import *
from project import database, email_handler
import configparser
import urllib.parse
import random
import string
import pg8000
import traceback
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


user_details = {}  # User details kept for us
session = {}  # Session information (logged in state)
page = {}  # Determines the page information

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('sample-config.ini')

app.secret_key = config['DATABASE']['secret_key']

# General routes


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_return_data = database.get_account(request.form['email'])
        if login_return_data is None:
            flash('Email does not exist, please register a new account', 'error')
            return redirect(url_for('login'))

        global user_details
        user_details = login_return_data[0]
        if not check_password_hash(user_details['ac_password'], request.form['password']):
            flash('Incorrect email/password, please try again', 'error')
            return redirect(url_for('login'))

        session['logged_in'] = True
        session['name'] = user_details['ac_firstname']

        if user_details['ac_type'] in ['clinician', 'researcher', 'patient', 'admin']:
            return redirect(url_for(str(user_details['ac_type']) + '_dashboard'))
        else:
            raise Exception('Error: Attempted logging in with an unknown role')

    elif request.method == 'GET':
        if not session.get('logged_in', None):
            return render_template('index.html', session=session, page=page)
        else:
            return redirect(url_for('patient_dashboard'))

@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    user_details = {}
    page = {}
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
@app.route('/register/<token>', methods=['GET', 'POST'])
def register(token=None):
    if not token and request.method == 'POST':
        firstName = request.form.get('first-name')
        lastName = request.form.get('last-name')
        gender = request.form.get('gender', "")
        age = request.form.get('age', "NA")
        mobile = request.form.get('mobile',"")
        treatment = request.form.getlist('treatment', [])
        emailAddress = request.form.get('email-address')
        password = request.form.get('password')

        try:
            print(request.form)
            if request.form['password'] != request.form['confirm-password']:
                flash('Passwords do not match. Please try again', 'error')
                return redirect(url_for('register'))
            if (age == ""):
                age = None
            if (gender == "NA"):
                gender = None
            if (mobile == ""):
                mobile = None
            add_patient_ret = database.add_patient(
                firstName,
                lastName,
                gender,
                age,
                mobile,
                treatment,
                emailAddress,
                password,
                generate_password_hash(password),
                'patient',
                'yes' if request.form.get('consent') == 'on' else 'no'
            )
            if add_patient_ret is None:
                # TODO: return error message
                return redirect(url_for('register'))
            else:
                session['logged_in'] = True
                login_return_data = database.get_account(request.form['email-address'])
                global user_details
                user_details = login_return_data[0]
                session['logged_in'] = True
                session['name'] = user_details['ac_firstname']
                return redirect(url_for('patient_dashboard'))
        except:
            traceback.print_exc(file=sys.stdout)
            print('Exception occurred. Please try again')
            flash('Email address already in use. Please try again', 'error')
            # return redirect(url_for('register'))
            return render_template('register.html', session=session, firstName=firstName, lastName=lastName, emailAddress=emailAddress, gender=gender, age=age, mobile=mobile)
    elif not token and request.method == 'GET':
        if not session.get('logged_in', None):
            treatments = None
            # TODO: try except; should handle somehow if it fails
            treatments = database.get_all_treatments()
            # TODO: probably best to hardcode some treatment types if it fails
            if treatments is None:
                treatments = {}

            return render_template('register.html', session=session, treatments=treatments)
        else:
            # TODO: How do we handle redirecting to the correct dashboard?
            return redirect(url_for('patient_dashboard'))
    elif token:
        token_valid = database.check_invitation_token_validity(token)
        if request.method == 'POST':
            try:
                if request.form['email-address'] != token_valid[0].get("ac_email"):
                    flash('This invitation is not valid for the email address entered. Please request a new invitation.', 'error')
                    return render_template('register-extra.html', token=token)
                if request.form['password'] != request.form['confirm-password']:
                    flash('Passwords do not match. Please try again', 'error')
                    return render_template('register-extra.html', token=token)
                age = None
                # gender = request.form.get('gender', "NA")
                # if (gender == "NA"):
                #     gender = None
                mobile = request.form.get('mobile-number', "")
                mobile = None if mobile == "" else mobile
                add_account_ret = database.add_patient(
                    request.form.get('first-name'),
                    request.form.get('last-name'),
                    request.form.get('gender', ""), # gender,
                    age,
                    mobile,
                    request.form.getlist('treatment', []),
                    request.form.get('email-address'),
                    request.form.get('password'),
                    generate_password_hash(request.form.get('password')),
                    token_valid[0].get('role'),
                    'yes' if request.form.get('consent') == 'on' else 'no'
                )
                if add_account_ret is None:
                    # TODO: return error message
                    return render_template('register-extra.html', token=token)
                else:
                    delete_token = database.delete_account_invitation(token, request.form['email-address'])
                    session['logged_in'] = True
                    login_return_data = database.get_account(request.form['email-address'])
                    user_details = login_return_data[0]
                    session['name'] = user_details['ac_firstname']
                    return redirect(url_for(str(token_valid[0].get('role', 'patient')).lower()+'_dashboard'))
            except Exception as e:
                print(e)
                print('Exception occurred. Please try again')
                flash('Something went wrong. Please try again', 'error')
            return render_template('register-extra.html', token=token)
        elif request.method == 'GET':
            if token_valid:
                return render_template('register-extra.html', token=token)
            else:
                return redirect(url_for('login'))


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        result = database.check_key_exists(request.form['email'])
        if (not result):
            unique_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24))
            try:
                database.add_password_key(unique_key, request.form['email'])
            except pg8000.core.IntegrityError: # if key already exists
                unique_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24))
                database.add_password_key(unique_key, request.form['email'])
            except pg8000.core.ProgrammingError: # email not in database
                flash('There is no account associated with that email. Please try again.', "error")
                return render_template('forgot-password.html')
        else:
            # print(result)
            unique_key = result[0]
        message = email_handler.setup_email(request.form['email'], unique_key)
        email_handler.send_email(message)
        flash('Email sent. If you cannot see the email in your inbox, check your spam folder.',  "success")
        return render_template('forgot-password.html')
    elif request.method == 'GET':
        return render_template('forgot-password.html')

@app.route('/researcher/')
def researcher_dashboard():
    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    if user_details['ac_type'] in ['clinician', 'patient', 'admin']:
        print('Error: Attempted accessing researcher dashboard as', str(user_details['ac_type']))
        return redirect(url_for(str(user_details['ac_type']) + '_dashboard'))

    print(session)
    return render_template('researcher/dashboard.html', session=session)

@app.route('/clinician/')
def clinician_dashboard():
    print(session)
    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    if user_details['ac_type'] in ['researcher', 'patient', 'admin']:
        print('Error: Attempted accessing researcher dashboard as', str(user_details['ac_type']))
        return redirect(url_for(str(user_details['ac_type']) + '_dashboard'))

    print(session)
    return render_template('clinician/dashboard.html', session=session)

@app.route('/clinician/create_survey/')
def create_survey():
    if not session.get('logged_in', None):
        return redirect(url_for('login'))
    if user_details['ac_type'] != 'clinician':
        raise Exception('Error: Attempted accessing clinician dashboard as Unknown')
    return render_template('clinician/dashboard.html', session=session)

@app.route('/clinician/view_patients/')
def view_patients():
    if not session.get('logged_in', None):
        return redirect(url_for('login'))
    if user_details['ac_type'] != 'clinician':
        raise Exception('Error: Attempted accessing clinician dashboard as Unknown')
    patients = None
    patients = database.get_all_patients(user_details['ac_id'])
    print(patients)
    list_of_patients = []
    patient_col_order = ["ac_id","ac_email", "ac_firstname", "ac_lastname", "ac_age", "ac_gender"]
    for patient in patients:
        patient = patient['row'][1:-1]
        patient_dict = {}
        for i, col in enumerate(patient.split(",")):
            patient_dict[patient_col_order[i]] = col.strip('"')
        list_of_patients.append(patient_dict)
    print(list_of_patients)

    return render_template('clinician/view-patients.html', patients=list_of_patients)

@app.route('/clinician/view_patients/<id>', methods=['GET'])
def view_patients_history(id = None):
    if not session.get('logged_in', None):
        return redirect(url_for('login'))
    if user_details['ac_type'] != 'clinician':
        raise Exception('Error: Attempted accessing clinician dashboard as Unknown')

    check_link = None
    check_link = database.check_clinician_link(user_details['ac_id'],id)
    if len(check_link) == 0:
        return(redirect(url_for('clinician_dashboard')))
    print('id = {}'.format(id))
    if id != None:
        symptoms = None
        symptoms = database.get_all_symptoms(id)
        list_of_symptoms = []
        symptom_col_order = ["symptom_id", "recorded_date", "symptom_name", "location", "severity", "occurence", "notes"]
        for symptom in symptoms:
            symptom = symptom["row"][1:-1]
            symptom_dict = {}
            for i, col in enumerate(symptom.split(",")):
                if i == 1 and col[-3:] == ":00":
                    col = col[:-3]
                if i == 6 and (col == '""' or len(col) == 0):
                    col = "None"
                symptom_dict[symptom_col_order[i]] = col.strip('"')
            list_of_symptoms.append(symptom_dict)
        return render_template('clinician/symptom-history.html', symptoms=list_of_symptoms)
    return(redirect(url_for('clinician_dashboard')))

@app.route('/reset-password/<url_key>', methods=['GET', 'POST'])
def reset_password(url_key):
    if request.method == 'POST':
        password = request.form['pw']
        password_confirm = request.form['pw_confirm']
        if password != password_confirm:
            flash('The passwords do not match.', "error")
        elif (len(password) < 8) or (len(password) > 20):
            flash('Password length must be between 8 and 20 characters.', "error")
        else:

            result = database.update_password(generate_password_hash(password), url_key)
            if not result:
                flash('The reset password key is invalid. Please request a new token.', "error")
            else:
                database.delete_token(url_key)
                flash('Password successfully reset. You may now login.',  "success")
        return redirect(url_for('reset_password', url_key=url_key))

    else:
        return render_template('/reset-password.html', url_key=url_key)

# Patient-related routes
@app.route('/patient/')
def patient_dashboard():
    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    if user_details['ac_type'] in ['clinician', 'researcher', 'admin']:
        print('Error: Attempted accessing researcher dashboard as', str(user_details['ac_type']))
        return redirect(url_for(str(user_details['ac_type']) + '_dashboard'))
    all_questionnaires = database.get_patient_questionnaires(user_details['ac_id'])
    return render_template('patient/dashboard.html', session=session, questionnaires=all_questionnaires)

@app.route('/patient/record-symptom/', methods=['GET', 'POST'])
@app.route('/patient/record-symptom/<id>', methods=['DELETE'])
def record_symptom(id=None):
    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    if user_details['ac_type'] == 'clinician':
        print('Error: Attempted accessing recording symptom as Clinician')
        return redirect(url_for('clinician_dashboard'))
    elif user_details['ac_type'] == 'researcher':
        print('Error: Attempted accessing recording symptom as Researcher')
        return redirect(url_for('researcher_dashboard'))
    elif user_details['ac_type'] != 'patient':
        raise Exception('Error: Attempted accessing recording symptom as Unknown')

    if request.method == 'POST':
        severity_scale = ["Not at all", "A little bit", "Somewhat", "Quite a bit", "Very much"]
        form_data = dict(request.form.lists())
        id = form_data.get('id')[0]

        symptom = form_data.get('symptom')[0]
        if symptom == 'Other':
            symptom = form_data.get('symptom')[1]

        location = form_data.get('location')[0]
        if location == 'Other':
            location = form_data.get('location')[1]

        severity = severity_scale[int(form_data.get('severity')[0])]
        occurence = form_data.get('occurence')[0]
        date = form_data.get('date')[0]
        notes = form_data.get('notes')[0]

        recordSymptom = database.record_symptom(
            id,
            user_details['ac_email'],
            symptom,
            location,
            severity,
            occurence,
            date,
            notes
        )

        if recordSymptom is None:
            flash('Unable to record symptom, please try again.', 'error')
            return redirect(url_for('record_symptom'))
        else:
            return redirect(url_for('symptom_history'))

    if request.method == 'DELETE':
        result = database.delete_symptom_record(user_details['ac_email'], id)
    return render_template('patient/record-symptom.html')


@app.route('/patient/symptom-history')
def symptom_history():
    if user_details.get('ac_email') is None:
        return redirect(url_for('login'))
    symptoms = None
    symptoms = database.get_all_symptoms(user_details['ac_email'])
    list_of_symptoms = []
    symptom_col_order = ["symptom_id", "recorded_date", "symptom_name", "location", "severity", "occurence", "notes"]
    for symptom in symptoms:
        symptom = symptom["row"][1:-1]
        symptom_dict = {}
        for i, col in enumerate(symptom.split(",")):
            if i == 1 and col[-3:] == ":00":
                col = col[:-3]
            if i == 6 and (col == '""' or len(col) == 0):
                col = "None"
            symptom_dict[symptom_col_order[i]] = col.strip('"').replace("'", "").replace('"', '')
        list_of_symptoms.append(symptom_dict)
    return render_template('patient/symptom-history.html', symptoms=list_of_symptoms)

@app.route('/patient/reports')
def patient_reports():
    return render_template('patient/reports.html')

@app.route('/patient/account/', methods=['GET', 'POST'])
@app.route('/patient/account/<clinician_email>', methods=['DELETE'])
def patient_account(clinician_email=None):
    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    if user_details['ac_type'] == 'clinician':
        print('Error: Attempted accessing patient account as Clinician')
        return redirect(url_for('clinician_dashboard'))
    elif user_details['ac_type'] == 'researcher':
        print('Error: Attempted accessing patient account as Researcher')
        return redirect(url_for('researcher_dashboard'))
    elif user_details['ac_type'] != 'patient':
        raise Exception('Error: Attempted accessing patient account as Unknown')

    if request.method == 'POST':
        form_data = dict(request.form.lists())
        clinician_email = form_data.get('clinician_email', [''])[0]
        if clinician_email == '':
            flash('Please enter a clinician email address.', 'error')

        acc = database.get_account(clinician_email.lower())
        if (acc == None or len(acc) == 0 or acc[0]['ac_type'] != "clinician"):
            flash('This email address is not associated with a clinician account.', 'error')
            return redirect(url_for('patient_account'))

        clinician_id = acc[0]['ac_id']

        try:
            link = database.add_patient_clinician_link(
                user_details['ac_id'],
                clinician_id
            )
        except pg8000.IntegrityError:
            flash('This clinician account is already linked to your account.', 'error')
            return redirect(url_for('patient_account'))

        if link is None:
            flash('Unable to link clinician account, please try again.', 'error')
            return redirect(url_for('patient_account'))
        else:
            flash('Clinician successfully linked to your account.', 'success')
            return redirect(url_for('patient_account'))

    if request.method == 'DELETE':
        acc = database.get_account(clinician_email)
        if (acc == None or len(acc) == 0 or acc[0]['ac_type'] != "clinician"):
            print('Error: Attempted to delete clinician-patient link for non-existent clinician account')
            return redirect(url_for('patient_account'))
        result = database.delete_patient_clinician_link(
            user_details['ac_id'],
            acc[0]['ac_id']
        )
        if result is None:
            flash('Clinician account link could not be deleted.', 'error')
            return redirect(url_for('patient_account'))

    clinicians_raw = database.get_linked_clinicians(user_details['ac_id'])
    clinicians = []
    if clinicians_raw is None:
        flash('Error retrieving clinicians list.', 'error')
        clinicians = []
    else:
        for clinician in clinicians_raw:
            acc = database.get_account_by_id(clinician['clinician_id'])
            if (acc != None and len(acc) != 0 and acc[0]['ac_type'] == "clinician"):
                clinicians.append(acc[0]['ac_email'])
    return render_template('patient/account.html', clinicians=clinicians)

@app.route('/patient/questionnaire/<id>', methods=['GET'])
def patient_questionnaire(id=None):
    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    if user_details['ac_type'] in ['clinician', 'researcher', 'admin']:
        print('Error: Attempted accessing researcher dashboard as', str(user_details['ac_type']))
        return redirect(url_for(str(user_details['ac_type']) + '_dashboard'))

    if id and request.method == 'GET':
        questionnaire = database.get_questionnaire(None, id)
        if questionnaire:
            questionnaire = questionnaire[0]
            questionnaire['link'] = questionnaire['link'].replace('EMAILADDRESS', user_details['ac_email'])
            return render_template('patient/questionnaire.html', questionnaire=questionnaire)
        return redirect(url_for('patient_dashboard'))

@app.route('/admin/')
def admin_dashboard():
    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    if user_details['ac_type'] in ['clinician', 'researcher', 'patient']:
        print('Error: Attempted accessing admin dashboard as a', str(user_details['ac_type']))
        return redirect(url_for(str(user_details['ac_type']) + '_dashboard'))

    all_questionnaires = database.get_all_questionnaires()
    return render_template('admin/dashboard.html', session=session, questionnaires=all_questionnaires)

@app.route('/admin/invite/', methods=['POST'])
def invite_user():
    if request.method == 'POST':
        form_data = dict(request.form.lists())
        email = form_data.get('email-address')[0]
        role = form_data.get('role')[0]
        existing_account = database.get_account(email)
        if existing_account:
            flash('An account with that email address already exists', 'error')
            return redirect(url_for('admin_dashboard'))
        already_invited = database.check_email_in_account_invitation(email)
        token = None
        if already_invited:
            token = already_invited[0].get('token')
            if already_invited[0].get('role') != role:
                result = database.update_role_in_account_invitation(email, role)
                token = result[0].get('token')
                role = result[0].get('role')
        else:
            token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24))
            try:
                database.add_account_invitation(token, email, role)
            except pg8000.core.IntegrityError: # if token already exists
                token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24))
                database.add_account_invitation(token, email, role)
        message = email_handler.setup_invitation(role, email, token)
        email_handler.send_email(message)
        flash('Email sent. If you cannot see the email in your inbox, check your spam folder.',  'success')
        return redirect(url_for('admin_dashboard'))

def validate_recipients(recipients):
    if len(recipients) == 0:
        return None, None
    recipients = recipients.split(',')
    valid_recipients = []
    invalid_recipients = []
    for email in recipients:
        email = email.strip()
        result = database.get_patient_by_email(email)
        if result:
            valid_recipients.append((result[0].get('ac_id'), email))
        else:
            invalid_recipients.append((None, email))
    return valid_recipients, invalid_recipients

def validate_form_link(link):
    return 'docs.google.com/forms/' in link

@app.route('/admin/create-questionnaire/', methods=['POST'])
def create_questionnaire():
    if request.method == 'POST':
        form_data = dict(request.form.lists())
        name = form_data.get('questionnaire-name')[0].strip()
        link = form_data.get('survey-link')[0].strip()
        if not validate_form_link(link):
            flash('Invalid Survey link. Please enter a Google forms link.', 'error')
            return redirect(url_for('admin_dashboard'))
        end_date = form_data.get('end-date')[0]
        recipients = form_data.get('recipients')[0]
        valid_recipients, invalid_recipients = validate_recipients(recipients)
        if (valid_recipients == None and invalid_recipients == None) or len(valid_recipients) == 0:
            flash('Invalid recipient(s) format. Please enter a comma separated list with no spaces.', 'error')
            return redirect(url_for('admin_dashboard'))
        existing_questionnaire = database.get_questionnaire(link)
        if existing_questionnaire:
            flash('A questionnaire with that link already exists.', 'error')
            return redirect(url_for('admin_dashboard'))
        result = database.add_questionnaire(name, link, end_date)
        if result:
            questionnaire_id = result[0].get('id')
            successful_records = database.link_questionnaire_to_patient(questionnaire_id, valid_recipients)
            if len(successful_records) == 0:
                flash('Something went wrong linking questionnaire to patients. Please try again.', 'error')
                return redirect(url_for('admin_dashboard'))
            # TODO: add email handler here
            flash('Created questionnaire successfully and sent notification to {}/{} patients'.format(len(valid_recipients), len(valid_recipients) + len(invalid_recipients)),  'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Failed to create questionnaire',  'error')
            return redirect(url_for('admin_dashboard'))

@app.route('/admin/questionnaire/<id>', methods=['GET', 'DELETE'])
def modify_questionnaire(id=None):
    if id and request.method == 'GET':
        questionnaire = database.get_questionnaire(None, id)
        if questionnaire:
            return jsonify(questionnaire=questionnaire), 200
        else:
            return jsonify(questionnaire=[]), 404
    if id and request.method == 'DELETE':
        result = database.delete_questionnaire(id)
        if result:
            return '', 200
        else:
            return '', 404
    if id and request.method == 'POST':
        form_data = dict(request.form.lists())
        name = form_data.get('questionnaire-name')[0].strip()
        link = form_data.get('survey-link')[0].strip()
        if not validate_form_link(link):
            flash('Invalid Survey link. Please enter a Google forms link.', 'error')
            return redirect(url_for('admin_dashboard'))
        end_date = form_data.get('end-date')[0]
        existing_questionnaire = database.get_questionnaire(None, id)
        if existing_questionnaire:
            result = database.update_questionnaire(id, name, link, end_date)
            if result:
                flash('Modified questionnaire successfully',  'success')
                return redirect(url_for('admin_dashboard'))
        flash('Failed to modify questionnaire',  'error')
        return redirect(url_for('admin_dashboard'))

# PWA-related routes
@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')
