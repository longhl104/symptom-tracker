from flask import *
import database, email_handler
import configparser
import urllib.parse
import random
import string
import pg8000
import traceback
import sys
import pygal
import io
import csv
from pygal.style import Style
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

user_details = {}  # User details kept for us
session = {}  # Session information (logged in state)
page = {}  # Determines the page information

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("config.ini")

app.secret_key = config["DATABASE"]["secret_key"]

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


@app.route("/logout", methods=["GET"])
def logout():
    session["logged_in"] = False
    user_details = {}
    page = {}
    return redirect(url_for("login"))


@app.route('/register', methods=['GET', 'POST'])
@app.route('/register/<token>', methods=['GET', 'POST'])
def register(token=None):
    if not token and request.method == 'POST':
        firstName = request.form.get('first-name')
        lastName = request.form.get('last-name')
        gender = request.form.get('gender', "")
        age = request.form.get('age', "")
        mobile = request.form.get('mobile',"")
        treatment = request.form.getlist('treatment', [])
        emailAddress = request.form.get('email-address')
        password = request.form.get('password')

        try:
            print(request.form)
            if request.form['password'] != request.form['confirm-password']:
                flash('Passwords do not match. Please try again', 'error')
                return redirect(url_for('register'))
            age = request.form.get('age', "")
            if (age == ""):
                age = None
            gender = request.form.get('gender', "NA")
            if (gender == "NA"):
                gender = None
            mobile = request.form.get('mobile-number', "")
            if (mobile == ""):
                mobile = None
            print(request.form.get('treatment'))
            add_patient_ret = database.add_patient(
                firstName,
                lastName,
                gender,
                age,
                mobile,
                request.form.get('treatment'),
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

@app.route("/reset-password/<url_key>", methods=["GET", "POST"])
def reset_password(url_key):
    if request.method == "POST":
        password = request.form["pw"]
        password_confirm = request.form["pw_confirm"]
        if password != password_confirm:
            flash("The passwords do not match.", "error")
        elif (len(password) < 8) or (len(password) > 20):
            flash("Password length must be between 8 and 20 characters.", "error")
        else:

            result = database.update_password(generate_password_hash(password), url_key)
            if not result:
                flash(
                    "The reset password key is invalid. Please request a new token.",
                    "error",
                )
            else:
                database.delete_token(url_key)
                flash("Password successfully reset. You may now login.", "success")
        return redirect(url_for("reset_password", url_key=url_key))

    else:
        return render_template("/reset-password.html", url_key=url_key)


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


@app.route("/patient/symptom-history")
def symptom_history():
    if user_details.get("ac_email") is None:
        return redirect(url_for("login"))
    symptoms = None
    symptoms = database.get_all_symptoms(user_details["ac_email"])
    list_of_symptoms = []
    symptom_col_order = [
        "symptom_id",
        "recorded_date",
        "symptom_name",
        "location",
        "severity",
        "occurence",
        "notes",
    ]
    for symptom in symptoms:
        symptom = symptom["row"][1:-1]
        symptom_dict = {}
        for i, col in enumerate(symptom.split(",")):
            if i == 1 and col[-3:] == ":00":
                col = col[:-3]
            symptom_dict[symptom_col_order[i]] = col.strip('"')
        list_of_symptoms.append(symptom_dict)
    return render_template("patient/symptom-history.html", symptoms=list_of_symptoms)




@app.route("/patient/reports", methods=["GET", "POST"])
def patient_reports():
    if user_details.get("ac_email") is None:
        return redirect(url_for("login"))

    graph = graph_data = symptom = location = startDate = endDate = None

    if request.method == "POST":
        form_data = dict(request.form.lists())

        symptom = form_data.get("symptom")[0]

        if symptom == "Other":
            symptom = form_data.get("symptom")[1]

        location = form_data.get("location")[0]

        if location == "Other":
            location = form_data.get("location")[1]

        startDate = form_data.get("startDate")[0]
        endDate = form_data.get("endDate")[0]

        data = [1]
        # data = database.get_graph_data(
        #     user_details["ac_email"], symptom, location, startDate, endDate
        # )
        graph = None

        if len(data) == 0:
            graph = pygal.Line()

        else:
            date = []
            severity = []
            severity_dict = {
                "Not at all": 0,
                "A little bit": 1,
                "Somewhat": 2,
                "Quite a bit": 3,
                "Very much": 4,
            }

            # for row in data:
            #     row = row["row"][1:-1].split(",")
            #     date += [row[0]]
            #     severity += [severity_dict[row[1].strip('"')]]

            def daterange(
                start_date, end_date
            ):  # https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
                for n in range(int((end_date - start_date).days)):
                    yield start_date + timedelta(n)

            def clean_data(start_date, end_date, data):
                date = []
                severity = []
                severity_dict = {
                    "Not at all": 0,
                    "A little bit": 1,
                    "Somewhat": 2,
                    "Quite a bit": 3,
                    "Very much": 4,
                }
                r = {}
                for row in data:
                    row = row["row"][1:-1].split(",")
                    if row[0] in r:
                        r[row[0]] += [[row[1].strip('"'), row[2].strip('"')]]
                    else:
                        r[row[0]] = [[row[1].strip('"'), row[2].strip('"')]]

                for single_date in daterange(start_date, end_date + timedelta(1)):

                    d = single_date.strftime("%Y-%m-%d")
                    date += [d + " "]
                    date += [d + ""]
                    date += [d + "\n"]
                    if d in r:
                        if len(r[d]) == 3:
                            severity += [
                                {"value": severity_dict[r[d][0][0]], "label": "Morning"}
                            ]
                            severity += [
                                {"value": severity_dict[r[d][1][0]], "label": "Daytime"}
                            ]
                            severity += [
                                {"value": severity_dict[r[d][2][0]], "label": "Night-time"}
                            ]

                        elif len(r[d]) == 2:
                            if r[d][0][1] == "Morning" and r[d][1][1] == "Daytime":
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Morning"}
                                ]
                                severity += [
                                    {"value": severity_dict[r[d][1][0]], "label": "Daytime"}
                                ]
                                severity += [None]
                            elif r[d][0][1] == "Morning" and r[d][1][1] == "Night-time":
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Morning"}
                                ]
                                severity += [None]
                                severity += [
                                    {
                                        "value": severity_dict[r[d][1][0]],
                                        "label": "Night-time",
                                    }
                                ]
                            else:
                                severity += [None]
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Daytime"}
                                ]
                                severity += [
                                    {
                                        "value": severity_dict[r[d][1][0]],
                                        "label": "Night-time",
                                    }
                                ]
                        else:
                            if r[d][0][1] == "All the time":
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Morning"}
                                ]
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Daytime"}
                                ]
                                severity += [
                                    {
                                        "value": severity_dict[r[d][0][0]],
                                        "label": "Night-time",
                                    }
                                ]
                            elif r[d][0][1] == "Sporadic":
                                severity += [
                                    {
                                        "value": severity_dict[r[d][0][0]],
                                        "label": "Sporadic",
                                    }
                                ] * 3
                            elif r[d][0][1] == "Morning":
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Morning"}
                                ]
                                severity += [None]
                                severity += [None]
                            elif r[d][0][1] == "Daytime":
                                severity += [None]
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Daytime"}
                                ]
                                severity += [None]
                            else:
                                severity += [None]
                                severity += [None]
                                severity += [
                                    {
                                        "value": severity_dict[r[d][0][0]],
                                        "label": "Night-time",
                                    }
                                ]

                    else:
                        severity += [None] * 3

                return date, severity

            def clean_data_no_space(start_date, end_date, data):
                date = []
                severity = []
                severity_dict = {
                    "Not at all": 0,
                    "A little bit": 1,
                    "Somewhat": 2,
                    "Quite a bit": 3,
                    "Very much": 4,
                }
                r = {}
                for row in data:
                    row = row["row"][1:-1].split(",")
                    if row[0] in r:
                        r[row[0]] += [[row[1].strip('"'), row[2].strip('"')]]
                    else:
                        r[row[0]] = [[row[1].strip('"'), row[2].strip('"')]]

                for single_date in daterange(start_date, end_date + timedelta(1)):
                    d = single_date.strftime("%Y-%m-%d")
                    if d in r:
                        date += [d+" "]
                        date += [d+""]
                        date += [d+"\n"]
                        if len(r[d]) == 3:
                            severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Morning'}]
                            severity += [{'value': severity_dict[r[d][1][0]], 'label': 'Daytime'}]
                            severity += [{'value': severity_dict[r[d][2][0]], 'label': 'Night-time'}]

                        elif len(r[d]) == 2:
                            if r[d][0][1] == 'Morning' and r[d][1][1] == 'Daytime':
                                severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Morning'}]
                                severity += [{'value': severity_dict[r[d][1][0]], 'label': 'Daytime'}]
                                severity += [None]
                            elif r[d][0][1] == 'Morning' and r[d][1][1] == 'Night-time':
                                severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Morning'}]
                                severity += [None]
                                severity += [{'value': severity_dict[r[d][1][0]], 'label': 'Night-time'}]
                            else:
                                severity += [None]
                                severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Daytime'}]
                                severity += [{'value': severity_dict[r[d][1][0]], 'label': 'Night-time'}]
                        else:
                            if r[d][0][1] == 'All the time':
                                severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Morning'}]
                                severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Daytime'}]
                                severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Night-time'}]
                            elif r[d][0][1] == 'Sporadic':
                                severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Sporadic'}] * 3
                                # severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Sporadic',
                                #                 "node": {
                                #                     "r": 4,
                                #                     "fill": "black",
                                #                     "fill-opacity": "100%",
                                #                     "stroke": "black",
                                #                     "stroke-opacity": "100%",
                                #                 },
                                #             }] * 3
                            elif r[d][0][1] == 'Morning':
                                severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Morning'}]
                                severity += [None]
                                severity += [None]
                            elif r[d][0][1] == 'Daytime':
                                severity += [None]
                                severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Daytime'}]
                                severity += [None]
                            else:
                                severity += [None]
                                severity += [None]
                                severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Night-time'}]

                return date, severity

            # first_row = data[0]["row"][1:-1].split(",")
            # last_row = data[-1]["row"][1:-1].split(",")
            # start_date = datetime.strptime(first_row[0], "%Y-%m-%d")
            # end_date = datetime.strptime(last_row[0], "%Y-%m-%d")

            # date, severity = clean_data_no_space(start_date, end_date, data)

            custom_style = Style(
                background="#FFFFFF",
                plot_background="#FFFFFF",
                transition="400ms ease-in",
                font_family="googlefont:Oxygen",
            )

            # #labels space
            # no_days = (end_date - start_date).days + 1
            # i = 0
            # while no_days / (7 * pow(3, i)) > 1:
            #     i += 1
            # freq = pow(3, i)

            # labels no space
            # no_days = len(date) / 3
            # i = 0
            # while no_days / (7 * pow(3,i)) > 1:
            #     i += 1
            # freq = pow(3, i)

            # graph = pygal.Line(style = custom_style, height = 400, x_label_rotation=60, x_title='Date',
            #     y_title='Severity', fill=False, range=(0, 4), show_legend=False, stroke_style={'width': 3},
            #     show_minor_x_labels=False, x_labels_major_every=freq, truncate_label=11)
            # graph.title = symptom + ' in my ' + location

            # graph.x_labels = date
            # graph.y_labels = list(severity_dict.keys())
            # graph.add('Severity', severity, allow_interruptions=True)

            # Additional Sporadic Label https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute
            # Change size, colour, opacity etc of specific shapes
            # Change shapes seems to be possible but a lot more work
            # Change stroke between sporadic points, each set of sporadic points would be disconnected from graph
            # custom_style = Style(
            #     background="transparent",
            #     plot_background="transparent",
            #     foreground="#53E89B",
            #     foreground_strong="#53A0E8",
            #     foreground_subtle="#630C0D",
            #     opacity=".6",
            #     opacity_hover=".9",
            #     transition="400ms ease-in",
            #     colors=("#E853A0", "#E853A0"),
            # )

            # stroke_style={
            #         "width": 5,
            #         "dasharray": "3, 6",
            #         "linecap": "round",
            #         "linejoin": "round",
            #     },

            # graph = pygal.Line(style = custom_style, height = 400, x_label_rotation=60, x_title='Date',
            #     y_title='Severity', fill=False, range=(0, 4), stroke_style={'width': 3})
            # graph.title = 'Symptoms in my Hands (C)'
            # graph.y_labels = list(severity_dict.keys())
            # graph.x_labels = ['2020-10-27 Morning', '2020-10-27  Daytime', '2020-10-27 Night-time', '2020-10-28 Morning',
            #  '2020-10-28 Daytime', '2020-10-28 Night-time', '2020-10-29 Morning', '2020-10-29 Daytime', 
            #  '2020-10-29 Night-time']            
            # graph.add("Cramping", [2, 4, 3, 0, 0, 3, 4, 0, 0])
            # graph.add("Discomfort", [2, 3, 2, 4, 3, 3, 0, 1, 2])
            # graph.add("Numbness",[0, 2, 3, 1, 2, 4, 2, 3, 0])
            # graph.add("Pain", [1, 3, 4, 1, 2, 0, 3, 2, 1])
            # graph.add("Tingling", [3, 2, 2, 4, 1, 3, 0, 3, 2])
            # graph.add("Weakness", [1, 2, 4, 0, 0, 3, 4,2 , 3])
            # graph.x_labels = ['Morning','2020-10-27','','Daytime','2020-10-27','','Night-time','2020-10-27','','Morning',
            #  '2020-10-28','', 'Daytime', '2020-10-28','', 'Night-time', '2020-10-28','','Morning', '2020-10-29','', 'Daytime', 
            #  '2020-10-29','', 'Night-time','2020-10-29']
            # graph.add("Cramping", [2, None, None, 4, None, None,3, None, None, 0, None, None,0, None, None,
            #     3, None, None, 4, None, None, 0, None, None, 0])
            # graph.add("Discomfort", [2, None, None, 3, None, None, 2, None, None, 4, None, None, 3, None, None, 
            #     3, None, None, 0, None, None, 1, None, None, 2])
            # graph.add("Numbness",[0, None, None, 2, None, None, 3, None, None, 1, None, None, 2, None, None, 
            #     4, None, None, 2, None, None, 3, None, None, 0])
            # graph.add("Pain", [1, None, None, 3, None, None, 4, None, None, 1, None, None, 2, None, None, 0, 
            #     3, None, None, 2, None, None, 1])
            # graph.add("Tingling", [3, None, None, 2, None, None, 2, None, None, 4, None, None, 1, None, None, 
            #     3, None, None, 0, None, None, 3, None, None, 2])
            # graph.add("Weakness", [1, None, None, 2, None, None, 4, None, None, 0, None, None, 0, None, None, 3, 
            #     4, None, None, 2, None, None, 3])
            # graph.x_labels = ['2020-10-27', '2020-10-27', '2020-10-27', '2020-10-28',
            #  '2020-10-28', '2020-10-28', '2020-10-29', '2020-10-29', 
            #  '2020-10-29']
            # graph.add("Cramping", [{'value': 2, 'label': 'Morning'}, {'value': 4, 'label': 'Daytime'}, 
            #     {'value': 3, 'label': 'Night-time'}, {'value': 0, 'label': 'Morning'}, {'value': 0, 'label': 'Daytime'},
            #     {'value': 3, 'label': 'Night-time'}, {'value': 4, 'label': 'Morning'}, {'value': 0, 'label': 'Daytime'},
            #     {'value': 0, 'label': 'Night-time'}])
            # graph.add("Discomfort", [{'value': 2, 'label': 'Morning'}, {'value': 3, 'label': 'Daytime'}, 
            #     {'value': 2, 'label': 'Night-time'}, {'value': 4, 'label': 'Morning'}, {'value': 3, 'label': 'Daytime'},
            #     {'value': 3, 'label': 'Night-time'}, {'value': 0, 'label': 'Morning'}, {'value': 1, 'label': 'Daytime'},
            #     {'value': 2, 'label': 'Night-time'}])
            # graph.add("Numbness", [{'value': 0, 'label': 'Morning'}, {'value': 2, 'label': 'Daytime'}, 
            #     {'value': 3, 'label': 'Night-time'}, {'value': 1, 'label': 'Morning'}, {'value': 2, 'label': 'Daytime'},
            #     {'value': 4, 'label': 'Night-time'}, {'value': 2, 'label': 'Morning'}, {'value': 3, 'label': 'Daytime'},
            #     {'value': 0, 'label': 'Night-time'}])
            # graph.add("Pain", [{'value': 1, 'label': 'Morning'}, {'value': 3, 'label': 'Daytime'}, 
            #     {'value': 4, 'label': 'Night-time'}, {'value': 1, 'label': 'Morning'}, {'value': 2, 'label': 'Daytime'},
            #     {'value': 0, 'label': 'Night-time'}, {'value': 3, 'label': 'Morning'}, {'value': 2, 'label': 'Daytime'},
            #     {'value': 1, 'label': 'Night-time'}])
            # graph.add("Weakness", [{'value': 3, 'label': 'Morning'}, {'value': 2, 'label': 'Daytime'}, 
            #     {'value': 2, 'label': 'Night-time'}, {'value': 4, 'label': 'Morning'}, {'value': 1, 'label': 'Daytime'},
            #     {'value': 3, 'label': 'Night-time'}, {'value': 0, 'label': 'Morning'}, {'value': 3, 'label': 'Daytime'},
            #     {'value': 2, 'label': 'Night-time'}])
            custom_style = Style(
                background="#FFFFFF",
                plot_background="#FFFFFF",
                transition="400ms ease-in",
                font_family="googlefont:Oxygen",
                colors=("#E853A0", "#E853A0", "#E853A0")
            )
            # graph = pygal.Line(style = custom_style, height = 400, x_label_rotation=60, x_title='Date',
            #     y_title='Severity', fill=False, range=(0, 4), stroke_style={'width': 3}, show_legend=False)
            # graph.y_labels = list(severity_dict.keys())
            # graph.x_labels = ['2020-10-27', '2020-10-27', '2020-10-27', '2020-10-28',
            #  '2020-10-28', '2020-10-28', '2020-10-29', '2020-10-29']  
            # graph.title = 'Cramping in my Hands (A)'
            # graph.add("Cramping", [{'value': 2, 'label': 'Morning'}, {'value': 4, 'label': 'Daytime'}, 
            #     {'value': 3, 'label': 'Night-time'}, None, {'value': 0, 'label': 'Daytime'},
            #     {'value': 3, 'label': 'Night-time'}, {'value': 4, 'label': 'Morning'}, None,
            #     {'value': 0, 'label': 'Night-time'}], allow_interruptions=True)
            # graph.title = 'Cramping in my Hands (C)'
            # graph.x_labels = ['2020-10-27', '2020-10-27', '2020-10-27',
            #  '2020-10-28', '2020-10-28', '2020-10-29', '2020-10-29']  
            # graph.add("Cramping", [{'value': 2, 'label': 'Morning'}, {'value': 4, 'label': 'Daytime'}, 
            #     {'value': 3, 'label': 'Night-time'}, None, None, None,
            #     {'value': 0, 'label': 'Night-time'}], allow_interruptions=True)
            # graph.add("Cramping", [None, None, None, {'value': 0, 'label': 'Daytime'},
            #     {'value': 3, 'label': 'Night-time'}, {'value': 4, 'label': 'Morning'},
            #     None], allow_interruptions=True)
            # graph.add("Cramping", [None, None, 
            #     {'value': 3, 'label': 'Night-time'}, {'value': 0, 'label': 'Daytime'},
            #     None, {'value': 4, 'label': 'Morning'},
            #     {'value': 0, 'label': 'Night-time'}], allow_interruptions=True, stroke_style={"width": 5,
            #         "dasharray": "3, 6"})
            # graph.title = 'Sporadic Cramping in my Hands (A)'
            # graph.x_labels = ['2020-10-27', '2020-10-27', '2020-10-27',
            #  '2020-10-28', '2020-10-28','2020-10-28', '2020-10-29', '2020-10-29', '2020-10-29']
            # graph.add("Cramping", [{'value': 2, 'label': 'Morning'}, {'value': 4, 'label': 'Daytime'}, 
            #     {'value': 2, 'label': 'Night-time'}, {'value': 3, 'label': 'Sporadic'}, {'value': 3, 'label': 'Sporadic'},
            #     {'value': 3, 'label': 'Sporadic'}, {'value': 4, 'label': 'Morning'}, {'value': 0, 'label': 'Daytime'},
            #     {'value': 0, 'label': 'Night-time'}])
            # graph.title = 'Sporadic Cramping in my Hands (B)'
            # graph.x_labels = ['2020-10-27', '2020-10-27', '2020-10-27',
            #  '2020-10-28', '2020-10-28','2020-10-28', '2020-10-29', '2020-10-29', '2020-10-29']
            # graph.add("Cramping", [{'value': 2, 'label': 'Morning'}, {'value': 4, 'label': 'Daytime'}, 
            #     {'value': 2, 'label': 'Night-time'}, {'value': 3, 'label': 'Sporadic'}, None,
            #     {'value': 3, 'label': 'Sporadic'}, {'value': 4, 'label': 'Morning'}, {'value': 0, 'label': 'Daytime'},
            #     {'value': 0, 'label': 'Night-time'}], allow_interruptions=True)
            # graph.add("Cramping", [None, None, 
            #     None, {'value': 3, 'label': 'Sporadic', "node": {
            #                                         "r": 4,
            #                                         "fill": "black",
            #                                         "fill-opacity": "100%",
            #                                         "stroke": "black",
            #                                         "stroke-opacity": "100%",
            #                                     },}, {'value': 3, 'label': 'Sporadic', "node": {
            #                                         "r": 4,
            #                                         "fill": "black",
            #                                         "fill-opacity": "100%",
            #                                         "stroke": "black",
            #                                         "stroke-opacity": "100%",
            #                                     }},
            #     {'value': 3, 'label': 'Sporadic', "node": {
            #                                         "r": 4,
            #                                         "fill": "black",
            #                                         "fill-opacity": "100%",
            #                                         "stroke": "black",
            #                                         "stroke-opacity": "100%",
            #                                     }}, None, None,
            #     None], allow_interruptions=True, stroke_style={"width": 5,"dasharray": "3, 6"})
            graph = pygal.DateLine(x_label_rotation=35,
                x_value_formatter=lambda dt: dt.strftime('%d, %b %Y'), range=(0,4))
            graph.y_labels = [
                'Not at all',
                'A little bit',
                'Somewhat',
                'Quite a bit',
                'Very much'
            ]
            graph.add("Serie1", [
                (datetime(2013, 1, 2), 3),
                (datetime(2013, 1, 2), 0),
                (datetime(2013, 8, 2), 1),
                (datetime(2014, 12, 7), 1),
                (datetime(2015, 3, 21), 2)
            ])
            graph.add("Serie2", [
                {'value': (datetime(2013, 1, 2), 3), 'label': 'test'},
                (datetime(2014, 8, 2), 1),
                (datetime(2014, 12, 7), 1),
                (datetime(2015, 3, 1), 0)
            ])

        graph_data = graph.render_data_uri()

    return render_template(
        "patient/reports.html",
        graph_data=graph_data,
        symptom=symptom,
        location=location,
        startDate=startDate,
        endDate=endDate,
    )

@app.route("/patient/reports/download-file", methods=["POST"])
def download_file():
    if user_details.get("ac_email") is None:
        return redirect(url_for("login"))

    string_input = io.StringIO()
    csv_writer = csv.writer(string_input)
    form_data = dict(request.form.lists())

    symptom = form_data.get("symptom")[0]

    if symptom == "Other":
        symptom = form_data.get("symptom")[1]

    location = form_data.get("location")[0]

    if location == "Other":
        location = form_data.get("location")[1]

    start_date = form_data.get("startDate")[0]
    end_date = form_data.get("endDate")[0]

    data = database.get_export_data(
        user_details["ac_email"], symptom, location, start_date, end_date
    )
    row_data = []

    for row in data:
        row = row["row"][1:-1].split(",")
        print(row[3], flush=True)
        if row[3] == '""':
            row_data += [(row[0], row[1].strip('"'), row[2].strip('"'), 'N/A')]
        else:   
            row_data += [(row[0], row[1].strip('"'), row[2].strip('"'), row[3].strip('"'))]

    head = ("Date", "Severity", "Time of Day", "Notes")
    csv_writer.writerow(("Date", "Severity", "Time of Day", "Notes"))
    csv_writer.writerows(row_data)

    output = make_response(string_input.getvalue())
    output.headers["Content-Disposition"] = (
        "attachment; filename=" + symptom.lower() + "_" + location.lower() + ".csv"
    )
    output.headers["Content-type"] = "text/csv"

    return output


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

# PWA-related routes

# PWA-related routes
@app.route("/service-worker.js")
def service_worker():
    return app.send_static_file("service-worker.js")
