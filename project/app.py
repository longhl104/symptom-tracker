from flask import *
import database
import configparser
import email_handler

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
            page['bar'] = False
            flash('Incorrect email/password, please try again')
            return redirect(url_for('login'))

        page['bar'] = True
        flash('You have been logged in successfully')
        session['logged_in'] = True

        global user_details
        user_details = login_return_data[0]

        return redirect(url_for('patient_index'))

    elif request.method == 'GET':
        return(render_template('index.html', session=session, page=page))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        add_patient_ret = database.add_patient(
            request.form['firstname'],
            request.form['lastname'],
            request.form['gender'],
            request.form['age'],
            request.form['mobile'],
            request.form.getlist('treatment'),
            request.form['email'],
            request.form['password'],
            request.form['consent']
        )
        if add_patient_ret is None:
            # TODO: return error message
            return redirect(url_for('register'))
        else:
            return redirect(url_for('patient_index'))
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


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = database.check_email(request.form['email'])
        if email is None:
            flash('There is no account associated with that email, please try again', "error")
            return render_template('forgot-password.html')
        else:
            message = email_handler.setup_email(email)
            email_handler.send_email(message)
            flash('Email sent. If you cannot see the email in your inbox, check your spam folder',  "success")
            return render_template('forgot-password.html')
    elif request.method == 'GET':
        return render_template('forgot-password.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        #TODO: work out how to get email address
        email = None
        # email = database.check_email(request.form['email'])
        if email is None:
            flash('An error occurred. Please try again.', "error")
            return render_template('reset-password.html')
        # TODO: check if password is of sufficient complexity
        password = request.form['pw']
        password_confirm = request.form['pw_confirm']
        if password != password_confirm:
            flash('The passwords do not match.', "error")
        else:
            database.update_password(password)
            flash('Password reset',  "success")
    elif request.method == 'GET':
        return render_template('/reset-password.html')

# Patient-related routes
@app.route('/patient/')
def patient_dashboard():
    # TODO: extract out into a decorator so less repeated code
    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    page['title'] = 'Dashboard'
    return render_template('patient/dashboard.html', session=session, page=page)

@app.route('/patient/record-symptom')
def record_symptom():
    return render_template('patient/record-symptom.html')

# PWA-related routes

@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')
