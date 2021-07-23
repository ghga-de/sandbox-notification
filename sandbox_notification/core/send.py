"""Functionality for sending notifications as email"""

import pika, json, smtplib, sys, time
from email.message import EmailMessage

SENDER_EMAIL = 'contact@ghga.de'
EMAIL_SUBJECT = 'GHGA Sandbox Notification'
MAX_ATTEMPTS = 5

def send_email(
    recipient_email:str, 
    message:str, 
    smtp_server:str, 
    smtp_port:str, 
    smtp_username:str, 
    smtp_password:str
):
    """
    send email
    """
    msg = EmailMessage()
    msg['Subject'] = EMAIL_SUBJECT
    # Does not work when sent from Gmail
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg.set_content(message)
    server = smtplib.SMTP(smtp_server, int(smtp_port))
    server.starttls()
    server.ehlo()
    server.login(smtp_username, smtp_password)
    server.send_message(msg)
    server.quit()
