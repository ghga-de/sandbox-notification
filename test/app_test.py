"""
This script runs a unit test for the publishing of a message to the notification service.
The message recipient and SMTP server are pre-defined specifically for the unit test.
"""
import argparse
from pathlib import Path
import subprocess
import time
import unittest
import unittest.mock
from test_publisher import test_publisher

class TestNotificationMethods(unittest.TestCase):
    """TestCase unittest class"""

    def test_app(self):
        """
        Test case for sending a RMQ message to the e-mail notification service.
        """
        with unittest.mock.patch('smtplib.SMTP', autospec=True) as mock:
            with subprocess.Popen('sandbox-notification' + ' "#.notifications.#"',
                    cwd=str(Path(__file__).parent.parent.resolve() / 'sandbox_notification'),
                    start_new_session=True, shell=True) as proc:
                args = argparse.Namespace(recipient_name='Test Recipient',
                        recipient_email='test@ghga.com', smtp_server='localhost',
                        smtp_port='80', smtp_username='', smtp_password='')
                test_publisher.main(args)
                time.sleep(10)
                proc.terminate()

if __name__=="__main__":
    unittest.main()
