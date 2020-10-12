from flask import *
import database
import configparser
import urllib.parse
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

        return redirect(url_for('patient_dashboard'))

    elif request.method == 'GET':
        if not session.get('logged_in', None):
            return(render_template('index.html', session=session, page=page))
        else:
            # TODO: How do we handle redirecting to the correct dashboard?
            return redirect(url_for('patient_dashboard'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            add_patient_ret = database.add_patient(
                request.form['first-name'],
                request.form['last-name'],
                request.form['gender'],
                request.form.get('age', ''),
                request.form.get('mobile-number', ''),
                request.form.getlist('treatment', ['A']),
                request.form['email-address'],
                request.form['password'],
                generate_password_hash(request.form['password']),
                request.form.get('consent', 'no')
            )
            if add_patient_ret is None:
                # TODO: return error message
                return redirect(url_for('register'))
            else:
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


@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')

# Patient-related routes


@app.route('/patient/')
def patient_dashboard():
    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    print(session)
    return render_template('patient/dashboard.html', session=session)


@app.route('/patient/record-symptom', methods=['GET', 'POST'])
def record_symptom():
    if not session.get('logged_in', None):
        return redirect(url_for('login'))
    if request.method == 'POST':
        form_data = dict(request.form.lists())
        print(form_data)
        symptom = form_data.get('symptom')[0]
        if symptom == 'Other':
            symptom = form_data.get('symptom')[1]
        print(symptom)
        activity = form_data.get('activity')[0]
        if activity == 'Other':
            activity = form_data.get('activity')[1]
        print(activity)
        severity = form_data.get('severity')[0]
        date = form_data.get('date')[0]
        time = form_data.get('time')[0]
        notes = form_data.get('notes')[0]

        recordSymptom = database.record_symptom(
            user_details['ac_email'],
            symptom,
            severity,
            date,
            time,
            activity,
            notes
        )

        if recordSymptom is None:
            flash('Unable to record symptom, please try again.', 'error')
            return redirect(url_for('record_symptom'))
        else:
            return redirect(url_for('patient_dashboard'))
    return render_template('patient/record-symptom.html')


@app.route('/patient/symptom-history')
def symptom_history():
    if user_details.get('ac_email') is None:
        return redirect(url_for('login'))
    symptoms = None
    symptoms = database.get_all_symptoms(user_details['ac_email'])
    symptoms = [symptom['row'].split(",") for symptom in symptoms]
    return render_template('patient/symptom-history.html', symptoms=symptoms)


@app.route('/patient/reports')
def patient_reports():
    return render_template('patient/reports.html')


@app.route('/patient/account')
def patient_account():
    return render_template('patient/account.html')

# PWA-related routes

# PWA-related routes
@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')
