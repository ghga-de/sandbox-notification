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

"""
This script runs a unit test for the publishing of a message to the notification service.
The message recipient and SMTP server are pre-defined specifically for the unit test.
"""
from email.message import EmailMessage
import smtplib
import unittest
import unittest.mock


class TestNotificationMethods(unittest.TestCase):
    """TestCase unittest class"""

    @staticmethod
    def test_send_email():
        """
        Test case for sending an e-mail through smtplib.
        """
        with unittest.mock.patch("smtplib.SMTP", autospec=True) as mock:
            msg = EmailMessage()
            msg["Subject"] = "Test"
            # Does not work when sent from Gmail
            msg["From"] = "apptest@ghga.de"
            msg["To"] = "apptest@ghga.de"
            msg.set_content("This is a unit test")
            server = smtplib.SMTP("localhost")
            server.send_message(msg)

            mock.return_value.send_message.assert_called_once_with(msg)


if __name__ == "__main__":
    unittest.main()
