from flask import *
import database
import configparser
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
            flash('Incorrect email/password, please try again', "error")
            return redirect(url_for('login'))

        session['logged_in'] = True

        global user_details
        user_details = login_return_data[0]

        return redirect(url_for('patient_dashboard'))

    elif request.method == 'GET':
        return(render_template('index.html', session=session, page=page))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            add_patient_ret = database.add_patient(
                request.form['first-name'],
                request.form['last-name'],
                request.form['gender'],
                request.form.get('age', 'no'),
                request.form.get('mobile-number', 'no'),
                request.form.getlist('treatment'),
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
            print("Exception occurred. Please try again")
            return redirect(url_for('register'))
    elif request.method == 'GET':
        treatments = None
        # TODO: try except; should handle somehow if it fails
        treatments = database.get_all_treatments()
        # TODO: probably best to hardcode some treatment types if it fails
        if treatments is None:
            treatments = {}

        return render_template('register.html', session=session, page=page, treatments=treatments)

@app.route('/register-extra')
def register_extra():
    return render_template('register-extra.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')

# Patient-related routes


@app.route('/patient/')
def patient_dashboard():
    # TODO: extract out into a decorator so less repeated code
    # if not session.get('logged_in', None):
    #     return redirect(url_for('login'))

    page['title'] = 'Dashboard'
    return render_template('patient/dashboard.html', session=session, page=page)

@app.route('/patient/record-symptom', methods=['GET', 'POST'])
def record_symptom():
    if not session.get('logged_in', None):
        return redirect(url_for('login'))
    if request.method == 'POST':
        #try:
        print(user_details)
        time = request.form.get('time', 'no')
        time = time.replace("%3A",":")
        datestring = request.form.get('date', 'no')
        date = datetime.strptime(datestring,'%Y-%m-%d').date()
        time = datetime.strptime(time,'%H:%M').time().strftime('%H:%M')
        

        recordSymptom = database.record_symptom(
            user_details['ac_email'],
            request.form['symptom'],
            request.form['severity'],
            date,
            time


        )

        
        if recordSymptom is None:
            # TODO: return error message
            return redirect(url_for('record_symptom'))
        else:
            return redirect(url_for('patient_dashboard'))
        #except:
            #print("Exception occurred. Please try again")
            #return redirect(url_for('record_symptom'))
    return render_template('patient/record-symptom.html')

@app.route('/patient/reports')
def patient_reports():
    return render_template('patient/reports.html')

@app.route('/patient/account')
def patient_account():
    return render_template('patient/account.html')

# PWA-related routes

@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')