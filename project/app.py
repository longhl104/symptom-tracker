from flask import *
from modules import *
from . import database

user_details = {}  # User details kept for us
session = {}  # Session information (logged in state)
page = {}  # Determines the page information


app = Flask(__name__)
app.secret_key = """U29tZWJvZHkgb25jZSB0b2xkIG1lIFRoZSB3b3JsZCBpcyBnb25uYSBy
b2xsIG1lIEkgYWluJ3QgdGhlIHNoYXJwZXN0IHRvb2wgaW4gdGhlIHNoZWQgU2hlIHdhcyBsb29r
aW5nIGtpbmRhIGR1bWIgV2l0aCBoZXIgZmluZ2VyIGFuZCBoZXIgdGh1bWIK"""


@app.route('/')
def index():
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    return render_template('index.html', session=session, page=page, user=user_details)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        login_return_data = database.check_login(
            request.form['email'],
            request.form['password']
        )

        if login_return_data is None:
            page['bar'] = False
            flash("Incorrect username/password, please try again")
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


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')
