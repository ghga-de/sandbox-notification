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
