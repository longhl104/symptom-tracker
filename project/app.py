from flask import *
import database
import configparser
import email_handler
import urllib.parse
import random
import string
import pg8000
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


user_details = {}  # User details kept for us
session = {}  # Session information (logged in state)
page = {}  # Determines the page information

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

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
            print('Error: Attempted logging in with an unknown role')
            raise

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
def register():
    if request.method == 'POST':
        
        try:
            if request.form['password'] != request.form['confirm-password']:
                flash('Passwords do not match. Please try again', 'error')
                return redirect(url_for('register'))
            age = request.form.get('age', "")
            if (age == ""):
                age = None
            # gender = request.form.get('gender', "NA")
            # if (gender == "NA"):
            #     gender = None
            mobile = request.form.get('mobile-number', "")
            if (mobile == ""):
                mobile = None
            add_patient_ret = database.add_patient(
                request.form.get('first-name'),
                request.form.get('last-name'),
                request.form.get('gender', ""), # gender,
                age,
                mobile, 
                request.form.getlist('treatment', []),
                request.form.get('email-address'),
                request.form.get('password'),
                generate_password_hash(request.form.get('password')),
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
                return redirect(url_for('patient_dashboard'))
        except Exception as e:
            print(e)
            print('Exception occurred. Please try again')
            flash('Something went wrong. Please try again', 'error')
            return redirect(url_for('register'))
    elif request.method == 'GET':
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


@app.route('/register-extra')
def register_extra():
    return render_template('register-extra.html')

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
            print(result)
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
    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    if user_details['ac_type'] in ['researcher', 'patient', 'admin']:
        print('Error: Attempted accessing researcher dashboard as', str(user_details['ac_type']))
        return redirect(url_for(str(user_details['ac_type']) + '_dashboard'))

    print(session)
    return render_template('clinician/dashboard.html', session=session)

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

    print(session)
    return render_template('patient/dashboard.html', session=session)

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
        print('Error: Attempted accessing recording symptom as Unknown')
        raise

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
            symptom_dict[symptom_col_order[i]] = col.strip('"')
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
        print('Error: Attempted accessing patient account as Unknown')
        raise

    if request.method == 'POST':
        form_data = dict(request.form.lists())
        clinician_email = form_data.get('clinician_email', [''])[0]
        if clinician_email == '':
            flash('Please enter a clinician email address.', 'error')

        acc = database.get_account(clinician_email)
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
        clinicians = ''
    else:
        for clinician in clinicians_raw:
            acc = database.get_account_by_id(clinician['clinician_id'])
            if (acc != None and len(acc) != 0 and acc[0]['ac_type'] == "clinician"):
                clinicians.append(acc[0]['ac_email'])
        clinicians = ",".join(clinicians)
    return render_template('patient/account.html', clinicians=clinicians)

@app.route('/admin/')
def admin_dashboard():
    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    if user_details['ac_type'] in ['clinician', 'researcher', 'patient']:
        print('Error: Attempted accessing admin dashboard as a', str(user_details['ac_type']))
        return redirect(url_for(str(user_details['ac_type']) + '_dashboard'))

    return render_template('admin/dashboard.html', session=session)

# PWA-related routes
@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')
