# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Functionality for sending notifications as email"""

from datetime import datetime
import logging
import time
from socket import gaierror
from email.message import EmailMessage
import smtplib
from ..config import get_config


class MaxAttemptsReached(Exception):
    """Raised when the maximum number of attempts has been reached."""


SENDER_EMAIL = "contact@ghga.de"
MAX_ATTEMPTS = 5


def send_email(data: dict):
    """
    Sending email
    """

    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        try:
            msg = EmailMessage()
            msg["Subject"] = data["subject"]
            # Does not work when sent from Gmail
            msg["From"] = SENDER_EMAIL
            msg["To"] = data["recipient_email"]
            msg.set_content(data["message"])
            config = get_config()
            server = smtplib.SMTP(config.smtpserv, config.smtpport)
            server.starttls()
            server.ehlo()
            server.login(config.smtpusername, config.smtppassword)
            server.send_message(msg)
            server.quit()
            logging.info(
                "  [>] %s: Email notification sent.\n",
                datetime.now().isoformat(timespec="milliseconds"),
            )
            break
        except (smtplib.SMTPException, gaierror) as exc:
            logging.warning(
                datetime.now().isoformat(timespec="milliseconds")
                + f": There has been an error sending an e-mail notification on attempt \
                    {attempt}/{MAX_ATTEMPTS}."
            )
            logging.exception(exc)
            attempt += 1
            time.sleep(5)
    else:
        logging.error(
            "%s: Maximum number of attempts reached. Email could not be sent.",
            datetime.now().isoformat(timespec="milliseconds"),
        )
        raise MaxAttemptsReached()
