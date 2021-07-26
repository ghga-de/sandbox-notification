"""Functionality for sending notifications as email"""

from email.message import EmailMessage
import smtplib

SENDER_EMAIL = 'contact@ghga.de'
EMAIL_SUBJECT = 'GHGA Sandbox Notification'
MAX_ATTEMPTS = 5

def send_email(data):
    """
    send email
    """
    msg = EmailMessage()
    msg['Subject'] = EMAIL_SUBJECT
    # Does not work when sent from Gmail
    msg['From'] = SENDER_EMAIL
    msg['To'] = data['recipient_email']
    msg.set_content(data['message'])
    server = smtplib.SMTP(data['smtp_server'], int(data['smtp_port']))
    server.starttls()
    server.ehlo()
    server.login( data['smtp_username'],  data['smtp_password'])
    server.send_message(msg)
    server.quit()
