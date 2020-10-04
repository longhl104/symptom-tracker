import smtplib, ssl
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config = configparser.ConfigParser()
config.read('config.ini')

def setup_email(to):

    sender = "brainandmindcentre.usyd@gmail.com" # config['DATABASE']['email']
    recipient = to

    text = """\

    You are receiving this email because you requested a password reset for the Brain and Mind Centre's Symptom Tracker. 

    Copy and paste the link below into your browser to create a new password:

    http://127.0.0.1:5000/reset-password/Gr6BCpNIN

    This link will expire in 24 hours.

    If you did not request a password reset, you may disregard this message.

    Thank you,

    The Brain and Mind Centre at the University of Sydney"""

    message = MIMEText(text, "plain")
    message["Subject"] = "Reset your password"
    message["From"] = sender
    message["To"] = recipient

    return message

def send_email(message):

    port = 465  # For SSL
    password = "w4wtcitb9newaf" #config['DATABASE']['email_password']
    
    # Create a secure SSL context
    context = ssl.create_default_context()
    smtp_server = "smtp.gmail.com"

    # Log into sender
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(message["From"], password)

    # Send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login( message["From"], password)
        server.sendmail( message["From"], message["To"], message.as_string()),