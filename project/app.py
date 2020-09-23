from flask import *
import database
import configparser

user_details = {}  # User details kept for us
session = {}  # Session information (logged in state)
page = {}  # Determines the page information


app = Flask(__name__)

config = configparser.ConfigParser()
config.read('sample-config.ini')

app.secret_key = config['DATABASE']['secret_key']


@app.route('/')
def index():
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    return render_template('index.html', session=session, page=page)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        login_return_data = database.check_login(
            request.form['email'],
            request.form['password']
        )

        if login_return_data is None:
            page['bar'] = False
            flash("Incorrect email/password, please try again")
            return redirect(url_for('login'))

        page['bar'] = True
        flash('You have been logged in successfully')
        session['logged_in'] = True

        global user_details
        user_details = login_return_data[0]

        return redirect(url_for('patient_index'))

    elif request.method == 'GET':
        return(render_template('login.html', session=session, page=page))


@app.route('/patient/index')
def patient_index():
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Patient API'
    return render_template('patient/index.html', session=session, page=page)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        add_patient_ret = database.add_patient(
            request.form['firstname'],
            request.form['lastname'],
            request.form['gender'],
            request.form['age'],
            request.form['mobile'],
            request.form['treatment'],
            request.form['email'],
            request.form['password'],
            request.form['consent']
        )
        if add_patient_ret is None:
            return redirect(url_for('register'))
        else:
            return redirect(url_for('patient_index'))
    elif request.method == 'GET':
        treatments = None
        treatments = database.get_all_treatments()

        if treatments is None:
            treatments = {}

        return render_template('register.html', session=session, page=page, treatments=treatments)


@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')
