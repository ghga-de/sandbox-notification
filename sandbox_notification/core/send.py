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
from email.message import EmailMessage
from socket import gaierror
import smtplib
from ..config import get_config


class MaxAttemptsReached(Exception):
    """Raised when the maximum number of attempts has been reached."""


def send_email(data: dict):
    """
    Sending email
    """

    config = get_config()

    for attempt in range(0, config.max_attempts):
        try:
            msg = EmailMessage()
            msg["Subject"] = data["subject"]
            # Does not work when sent from Gmail
            msg["From"] = config.sender_email
            msg["To"] = data["recipient_email"]
            msg.set_content(data["message"])

            server = smtplib.SMTP(config.smtp_server, config.smtp_port)

            server.starttls()

            server.ehlo()

            server.login(config.smtp_username, config.smtp_password)
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
                    {attempt+1}/{config.max_attempts}."
            )
            logging.exception(exc)
            time.sleep(5)

    logging.error(
        "%s: Maximum number of attempts reached. Email could not be sent.",
        datetime.now().isoformat(timespec="milliseconds"),
    )
    raise MaxAttemptsReached()
