from flask import *
import database
import configparser
import email_handler
import urllib.parse
from datetime import datetime

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
        login_return_data = database.check_login(
            request.form['email'],
            request.form['password']
        )

        if login_return_data is None:
            flash('Incorrect email/password, please try again', 'error')
            return redirect(url_for('login'))

        session['logged_in'] = True
        

        global user_details
        user_details = login_return_data[0]
        session['name'] = user_details['ac_firstname']

        return redirect(url_for('patient_dashboard'))

    elif request.method == 'GET':
        if not session.get('logged_in', None):
            return(render_template('index.html', session=session, page=page))
        else:
            # TODO: How do we handle redirecting to the correct dashboard?
            return redirect(url_for('patient_dashboard'))

@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    return(render_template('index.html', session=session, page=page))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            if request.form['password'] != request.form['confirm-password']:
                flash('Passwords do not match. Please try again', 'error')
                return redirect(url_for('register'))
            add_patient_ret = database.add_patient(
                request.form['first-name'],
                request.form['last-name'],
                request.form.get('gender', ''),
                request.form.get('age', ''),
                request.form.get('mobile-number', ''),
                request.form.getlist('treatment', ['A']),
                request.form['email-address'],
                request.form['password'],
                request.form.get('consent', 'no')
            )
            if add_patient_ret is None:
                # TODO: return error message
                return redirect(url_for('register'))
            else:
                return redirect(url_for('patient_dashboard'))
        except:
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
        #TODO fix check if email account exists
        # email = database.check_email(request.form['email'])
        # if email is None:
        #     flash('There is no account associated with that email, please try again', "error")
        #     return render_template('forgot-password.html')
        # else:
        message = email_handler.setup_email(request.form['email'])
        email_handler.send_email(message)
        flash('Email sent. If you cannot see the email in your inbox, check your spam folder',  "success")
        return render_template('forgot-password.html')
    elif request.method == 'GET':
        return render_template('forgot-password.html')

@app.route('/reset-password/', methods=['GET', 'POST'])
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token=None):
    if request.method == 'POST':
        #TODO: work out how to get email address
        # email = None
        # # email = database.check_email(request.form['email'])
        # if email is None:
        #     flash('An error occurred. Please try again.', "error")
        #     return render_template('reset-password.html')
        # TODO: check if password is of sufficient complexity
        password = request.form['pw']
        password_confirm = request.form['pw_confirm']

        # flash('Password successfully reset.',  "success")
        # TODO: fix password reset logic / database
        # if password != password_confirm:
        #     flash('The passwords do not match.', "error")
        # else:
        #     database.update_password(password)
        #     flash('Password reset',  "success")
        return "Password successfully reset.", 200
    else:
        return render_template('/reset-password.html', token=token)

@app.route('/patient/')
def patient_dashboard():
    # if not session.get('logged_in', None):
    #     return redirect(url_for('login'))
    
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
    return render_template('patient/symptom-history.html', symptoms = symptoms)    
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