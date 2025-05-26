from flask import current_app
from flask_mail import Message
from app import mail

def send_email(to, subject, body):
    with current_app.app_context():
        msg = Message(subject=subject, recipients=[to], body=body)
        mail.send(msg)
