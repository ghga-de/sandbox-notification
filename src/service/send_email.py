"""
Send email
"""

import smtplib
from email.message import EmailMessage


def send_email(sender, receiver, subject, message):
    """
    send email
    :return:
    """
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(message)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(sender, "")
    server.send_message(msg)
    server.quit()
