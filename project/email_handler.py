import smtplib, ssl
import configparser
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config = configparser.ConfigParser()
config.read('config.ini')

class EmailHandler():
    def __init__(self, emails=[]):
        self.emails = emails

    def set_emails(self, emails):
        self.emails = emails

    def send_emails(self):
        for email in self.emails:
            self.send(self.setup_email(email.get('recipient'), email.get('subject'), email.get('message')))

    @staticmethod
    def setup_email(recipient, subject, text):
        sender = str(config['EMAIL']['email'])
        message = MIMEText(text, "plain")
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = recipient
        return message

    @staticmethod
    def send(message):
        port = 465  # For SSL
        password = str(config['EMAIL']['email_password'])

        # Create a secure SSL context
        context = ssl.create_default_context()
        smtp_server = "smtp.gmail.com"

        # Log into sender
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(message["From"], password)

        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(message["From"], password)
            server.sendmail(message["From"], message["To"], message.as_string())

    @staticmethod
    def forgot_password_email_text(key):
        base_url = config['EMAIL']['base_url']
        text = """

        You are receiving this email because you requested a password reset for the Brain and Mind Centre's Symptom Tracker.

        Click (or copy-paste) the link below into your browser to create a new password:

        {base_url}/reset-password/{key}

        This link will expire in 24 hours.

        If you did not request a password reset, you may disregard this message.

        Thank you,

        The Brain and Mind Centre at the University of Sydney""".format(base_url=base_url, key=key)
        return text

    @staticmethod
    def invitation_email_text(role, key):
        base_url = config['EMAIL']['base_url']
        role = 'an ' + role.title() if role.lower() == 'admin' else 'a ' + role.title()
        text = """

        You are receiving this email because you have been invited to join Brain and Mind Centre's Symptom Tracker as {role}.

        Click (or copy-paste) the link below into your browser to create a new account:

        {base_url}/register/{key}

        This link will expire in 24 hours.

        If you did not request an invitation, you may disregard this message.

        Thank you,

        The Brain and Mind Centre at the University of Sydney""".format(base_url=base_url, key=key, role=role)
        return text

    @staticmethod
    def weekly_survey_email_text(id, questionnaire_name, end_date):
        base_url = config['EMAIL']['base_url']
        date_time_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        text = """

        You are receiving this email because you are a registered patient on Symptom Tracker and have been assigned a new questionnaire - {questionnaire_name}.

        Click (or copy-paste) the link below into your browser to complete the questionnaire:

        {base_url}/patient/questionnaire/{id}

        The questionnaire is due on {end_date}.

        Thank you,

        The Brain and Mind Centre at the University of Sydney""".format(questionnaire_name=questionnaire_name, base_url=base_url, id=id, end_date=date_time_obj.strftime('%B %d %Y'))
        return text

    @staticmethod
    def summary_weekly_survey_email_text(questionnaire_id, name, end_date, valid_recipients, invalid_recipients):
        date_time_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        text = """

        You are receiving this email because you are a registered admin on Symptom Tracker.
        
        Here is a summary report for the recently created survey - {questionnaire_name}:

        Questionnaire ID: {id}
        Due date: {end_date}
        Total recipient(s): {total}
        Successful recipient(s): {successful}
        Invalid recipient(s): {invalid}


        Below are email address(es) that didn't receive the survey:
        {invalid_emails}

        Thank you,

        The Brain and Mind Centre at the University of Sydney""".format(
            questionnaire_name=name,
            id=questionnaire_id,
            end_date=date_time_obj.strftime('%B %d %Y'),
            total=len(valid_recipients) + len(invalid_recipients),
            successful=len(valid_recipients),
            invalid=len(invalid_recipients),
            invalid_emails=", ".join([email[1] for email in invalid_recipients])
        )
        return text