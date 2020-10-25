from flask import *
import database
import configparser
import email_handler
import urllib.parse
import random
import string
import pg8000
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


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        login_return_data = database.get_account(request.form["email"])
        if login_return_data is None:
            flash("Email does not exist, please register a new account", "error")
            return redirect(url_for("login"))

        global user_details
        user_details = login_return_data[0]

        if not check_password_hash(
            user_details["ac_password"], request.form["password"]
        ):
            flash("Incorrect email/password, please try again", "error")
            return redirect(url_for("login"))

        session["logged_in"] = True
        session["name"] = user_details["ac_firstname"]

        if user_details["ac_type"] == "clinician":
            return redirect(url_for("clinician_dashboard"))
        elif user_details["ac_type"] == "researcher":
            return redirect(url_for("researcher_dashboard"))
        elif user_details["ac_type"] == "patient":
            return redirect(url_for("patient_dashboard"))
        else:
            print("Error: Attempted logging in with Unknown")
            raise

    elif request.method == "GET":
        if not session.get("logged_in", None):
            return render_template("index.html", session=session, page=page)
        else:
            return redirect(url_for("patient_dashboard"))


@app.route("/logout", methods=["GET"])
def logout():
    session["logged_in"] = False
    user_details = {}
    page = {}
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        try:
            if request.form["password"] != request.form["confirm-password"]:
                flash("Passwords do not match. Please try again", "error")
                return redirect(url_for("register"))
            age = request.form.get("age", "")
            if age == "":
                age = None
            # gender = request.form.get('gender', "NA")
            # if (gender == "NA"):
            #     gender = None
            mobile = request.form.get("mobile-number", "")
            if mobile == "":
                mobile = None
            add_patient_ret = database.add_patient(
                request.form.get("first-name"),
                request.form.get("last-name"),
                request.form.get("gender", ""),  # gender,
                age,
                mobile,
                request.form.getlist("treatment", []),
                request.form.get("email-address"),
                request.form.get("password"),
                generate_password_hash(request.form.get("password")),
                "patient",
                "yes" if request.form.get("consent") == "on" else "no",
            )
            if add_patient_ret is None:
                # TODO: return error message
                return redirect(url_for("register"))
            else:
                session["logged_in"] = True
                login_return_data = database.get_account(request.form["email-address"])
                global user_details
                user_details = login_return_data[0]
                return redirect(url_for("patient_dashboard"))
        except Exception as e:
            print(e)
            print("Exception occurred. Please try again")
            flash("Something went wrong. Please try again", "error")
            return redirect(url_for("register"))
    elif request.method == "GET":
        if not session.get("logged_in", None):
            treatments = None
            # TODO: try except; should handle somehow if it fails
            treatments = database.get_all_treatments()
            # TODO: probably best to hardcode some treatment types if it fails
            if treatments is None:
                treatments = {}

            return render_template(
                "register.html", session=session, treatments=treatments
            )
        else:
            # TODO: How do we handle redirecting to the correct dashboard?
            return redirect(url_for("patient_dashboard"))


@app.route("/register-extra")
def register_extra():
    return render_template("register-extra.html")


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        result = database.check_key_exists(request.form["email"])
        if not result:
            unique_key = "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(24)
            )
            try:
                database.add_password_key(unique_key, request.form["email"])
            except pg8000.core.IntegrityError:  # if key already exists
                unique_key = "".join(
                    random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(24)
                )
                database.add_password_key(unique_key, request.form["email"])
            except pg8000.core.ProgrammingError:  # email not in database
                flash(
                    "There is no account associated with that email. Please try again.",
                    "error",
                )
                return render_template("forgot-password.html")
        else:
            print(result)
            unique_key = result[0]
        message = email_handler.setup_email(request.form["email"], unique_key)
        email_handler.send_email(message)
        flash(
            "Email sent. If you cannot see the email in your inbox, check your spam folder.",
            "success",
        )
        return render_template("forgot-password.html")
    elif request.method == "GET":
        return render_template("forgot-password.html")


@app.route("/researcher/")
def researcher_dashboard():
    if not session.get("logged_in", None):
        return redirect(url_for("login"))

    if user_details["ac_type"] == "clinician":
        print("Error: Attempted accessing researcher dashboard as Clinician")
        return redirect(url_for("clinician_dashboard"))
    elif user_details["ac_type"] == "patient":
        print("Error: Attempted accessing researcher dashboard as Patient")
        return redirect(url_for("patient_dashboard"))
    elif user_details["ac_type"] != "researcher":
        print("Error: Attempted accessing researcher dashboard as Unknown")
        raise

    print(session)
    return render_template("researcher/dashboard.html", session=session)


@app.route("/clinician/")
def clinician_dashboard():
    if not session.get("logged_in", None):
        return redirect(url_for("login"))

    if user_details["ac_type"] == "researcher":
        print("Error: Attempted accessing clinician dashboard as Researcher")
        return redirect(url_for("researcher_dashboard"))
    elif user_details["ac_type"] == "patient":
        print("Error: Attempted accessing clinician dashboard as Patient")
        return redirect(url_for("patient_dashboard"))
    elif user_details["ac_type"] != "clinician":
        print("Error: Attempted accessing clinician dashboard as Unknown")
        raise

    print(session)
    return render_template("clinician/dashboard.html", session=session)


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
@app.route("/patient/")
def patient_dashboard():
    if not session.get("logged_in", None):
        return redirect(url_for("login"))

    if user_details["ac_type"] == "clinician":
        print("Error: Attempted accessing patient dashboard as Clinician")
        return redirect(url_for("clinician_dashboard"))
    elif user_details["ac_type"] == "researcher":
        print("Error: Attempted accessing patient dashboard as Researcher")
        return redirect(url_for("researcher_dashboard"))
    elif user_details["ac_type"] != "patient":
        print("Error: Attempted accessing patient dashboard as Unknown")
        raise

    print(session)
    return render_template("patient/dashboard.html", session=session)


@app.route("/patient/record-symptom/", methods=["GET", "POST"])
@app.route("/patient/record-symptom/<id>", methods=["DELETE"])
def record_symptom(id=None):
    if not session.get("logged_in", None):
        return redirect(url_for("login"))

    if user_details["ac_type"] == "clinician":
        print("Error: Attempted accessing recording symptom as Clinician")
        return redirect(url_for("clinician_dashboard"))
    elif user_details["ac_type"] == "researcher":
        print("Error: Attempted accessing recording symptom as Researcher")
        return redirect(url_for("researcher_dashboard"))
    elif user_details["ac_type"] != "patient":
        print("Error: Attempted accessing recording symptom as Unknown")
        raise

    if request.method == "POST":
        severity_scale = [
            "Not at all",
            "A little bit",
            "Somewhat",
            "Quite a bit",
            "Very much",
        ]
        form_data = dict(request.form.lists())
        id = form_data.get("id")[0]

        symptom = form_data.get("symptom")[0]
        if symptom == "Other":
            symptom = form_data.get("symptom")[1]

        location = form_data.get("location")[0]
        if location == "Other":
            location = form_data.get("location")[1]

        severity = severity_scale[int(form_data.get("severity")[0])]
        occurence = form_data.get("occurence")[0]
        date = form_data.get("date")[0]
        notes = form_data.get("notes")[0]

        recordSymptom = database.record_symptom(
            id,
            user_details["ac_email"],
            symptom,
            location,
            severity,
            occurence,
            date,
            notes,
        )

        if recordSymptom is None:
            flash("Unable to record symptom, please try again.", "error")
            return redirect(url_for("record_symptom"))
        else:
            return redirect(url_for("symptom_history"))

    if request.method == "DELETE":
        result = database.delete_symptom_record(user_details["ac_email"], id)
    return render_template("patient/record-symptom.html")


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
    graph_data = symptom = location = startDate = endDate = None

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

        data = database.get_graph_data(
            user_details["ac_email"], symptom, location, startDate, endDate
        )
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

            first_row = data[0]["row"][1:-1].split(",")
            last_row = data[-1]["row"][1:-1].split(",")
            start_date = datetime.strptime(first_row[0], "%Y-%m-%d")
            end_date = datetime.strptime(last_row[0], "%Y-%m-%d")

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

            # for single_date in daterange(start_date, end_date + timedelta(1)):
            #     d = single_date.strftime("%Y-%m-%d")
            #     if d in r:
            #         date += [d+" "]
            #         date += [d+""]
            #         date += [d+"\n"]
            #         if len(r[d]) == 3:
            #             severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Morning'}]
            #             severity += [{'value': severity_dict[r[d][1][0]], 'label': 'Daytime'}]
            #             severity += [{'value': severity_dict[r[d][2][0]], 'label': 'Night-time'}]

            #         elif len(r[d]) == 2:
            #             if r[d][0][1] == 'Morning' and r[d][1][1] == 'Daytime':
            #                 severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Morning'}]
            #                 severity += [{'value': severity_dict[r[d][1][0]], 'label': 'Daytime'}]
            #                 severity += [None]
            #             elif r[d][0][1] == 'Morning' and r[d][1][1] == 'Night-time':
            #                 severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Morning'}]
            #                 severity += [None]
            #                 severity += [{'value': severity_dict[r[d][1][0]], 'label': 'Night-time'}]
            #             else:
            #                 severity += [None]
            #                 severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Daytime'}]
            #                 severity += [{'value': severity_dict[r[d][1][0]], 'label': 'Night-time'}]
            #         else:
            #             if r[d][0][1] == 'All the time':
            #                 severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Morning'}]
            #                 severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Daytime'}]
            #                 severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Night-time'}]
            #             elif r[d][0][1] == 'Sporadic':
            #                 severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Sporadic'}] * 3
            #             elif r[d][0][1] == 'Morning':
            #                 severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Morning'}]
            #                 severity += [None]
            #                 severity += [None]
            #             elif r[d][0][1] == 'Daytime':
            #                 severity += [None]
            #                 severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Daytime'}]
            #                 severity += [None]
            #             else:
            #                 severity += [None]
            #                 severity += [None]
            #                 severity += [{'value': severity_dict[r[d][0][0]], 'label': 'Night-time'}]

            custom_style = Style(
                background="#FFFFFF",
                plot_background="#FFFFFF",
                transition="400ms ease-in",
                font_family="googlefont:Oxygen",
            )

            no_days = (end_date - start_date).days + 1
            i = 0
            while no_days / (7 * pow(3, i)) > 1:
                i += 1
            freq = pow(3, i)

            # no_days = len(date) / 3
            # i = 0
            # while no_days / (7 * pow(3,i)) > 1:
            #     i += 1
            # freq = pow(3, i)

            graph = pygal.Line(style = custom_style, height = 400, x_label_rotation=60, x_title='Date',
                y_title='Severity', fill=False, range=(0, 4), show_legend=False, stroke_style={'width': 3},
                show_minor_x_labels=False, x_labels_major_every=freq, truncate_label=11)
            graph.title = symptom + ' in my ' + location

            graph.x_labels = date
            graph.y_labels = list(severity_dict.keys())
            graph.add('Severity', severity, allow_interruptions=True)

            

            # Additional Sporadic Label https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute
            # Change size, colour, opacity etc of specific shapes
            # Change shapes seems to be possible but a lot more work
            # Change stroke between sporadic points, each set of sporadic points would be disconnected from graph
            # graph = pygal.Line(style=custom_style)
            # graph.add(
            #     "Serie",
            #     [
            #         1,
            #         {
            #             "value": 2,
            #             "node": {
            #                 "fill": "black",
            #                 "fill-opacity": "100%",
            #                 "stroke": "black",
            #                 "stroke-opacity": "100%",
            #             },
            #         },
            #         3,
            #     ],
            # )
            # graph.add(
            #     "Serie",
            #     [
            #         None,
            #         None,
            #         None,
            #         1,
            #         {
            #             "value": 2,
            #             "node": {
            #                 "fill": "black",
            #                 "fill-opacity": "100%",
            #                 "stroke": "black",
            #                 "stroke-opacity": "100%",
            #             },
            #         },
            #         3,
            #     ],
            #     stroke_style={
            #         "width": 5,
            #         "dasharray": "3, 6",
            #         "linecap": "round",
            #         "linejoin": "round",
            #     },
            # )

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

        graph_data = graph.render_data_uri()

    return render_template(
        "patient/reports.html",
        graph_data=graph_data,
        symptom=symptom,
        location=location,
        startDate=startDate,
        endDate=endDate,
    )


@app.route("/patient/reports/download", methods=["POST"])
def download_file():
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


@app.route("/patient/account")
def patient_account():
    return render_template("patient/account.html")


# PWA-related routes

# PWA-related routes
@app.route("/service-worker.js")
def service_worker():
    return app.send_static_file("service-worker.js")
