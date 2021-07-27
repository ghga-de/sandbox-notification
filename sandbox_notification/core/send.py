"""Functionality for sending notifications as email"""

from datetime import datetime
import logging
import time
from email.message import EmailMessage
import smtplib

class MaxAttemptsReached(Exception):
    """Raised when the maximum number of attempts has been reached."""

SENDER_EMAIL = 'contact@ghga.de'
EMAIL_SUBJECT = 'GHGA Sandbox Notification'
MAX_ATTEMPTS = 5

def send_email(data):
    """
    Sending email
    """

    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        try:
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
            logging.info("  [>] %s: Email notification sent.\n",
                    datetime.now().isoformat(timespec='milliseconds'))
            break
        except smtplib.SMTPException:
            logging.warning(datetime.now().isoformat(timespec='milliseconds') +
                    f": There has been an error sending an e-mail notification on attempt \
                    {attempt}/{MAX_ATTEMPTS}.")
            logging.exception('')
            attempt += 1
            time.sleep(5)
    else:
        logging.error('%s: Maximum number of attempts reached. Email could not be sent.',
                datetime.now().isoformat(timespec='milliseconds'))
        raise MaxAttemptsReached()
