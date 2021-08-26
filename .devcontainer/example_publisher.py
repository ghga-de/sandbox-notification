#!/usr/bin/env python3

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
This script simulates a service that is sending
a notification request to the notification service.

Usage:
    Please first start the sandbox-notification service,
    which acts as a subscriber, by running:
    ```
    ./dev_launcher
    ```

    Then open a new terminal and execute this script using:
    ```
    ./example_publisher.py "$RNAME" "$REMAIL" "$MESSAGE" "$SUBJECT"
    ```
"""

import os
import argparse
import logging
from pathlib import Path
from datetime import datetime
from ghga_service_chassis_lib.pubsub import AmqpTopic
from sandbox_notification.pubsub import get_connection_params
from sandbox_notification.schemata.schemata import get_schema
from sandbox_notification.config import get_config

HERE = Path(__file__).parent.resolve()


def main(recipient_name: str, recipient_email: str, message_text: str, subject: str):
    """Run a test for publishing a notification."""

    # change into directory of this script so that the
    # config yaml is read
    os.chdir(HERE)

    config = get_config()

    message = {
        "recipient_name": recipient_name,
        "recipient_email": recipient_email,
        "message": message_text,
        "subject": subject,
    }

    topic = AmqpTopic(
        connection_params=get_connection_params(),
        topic_name=config.topic_name,
        service_name="publisher",
        json_schema=get_schema(config.topic_name),
    )

    topic.publish(message)

    logging.info(
        " [x] %s: Sent notification.", datetime.now().isoformat(timespec="milliseconds")
    )


def run():
    """Run the publisher testing script."""

    parser = argparse.ArgumentParser(
        description="Send a notification message to another script that send a notification email."
    )

    parser.add_argument("recipient_name", type=str)
    parser.add_argument("recipient_email", type=str)
    parser.add_argument("message_text", type=str)
    parser.add_argument("subject", type=str)
    args = parser.parse_args()

    main(
        recipient_name=str(args.recipient_name),
        recipient_email=str(args.recipient_email),
        message_text=str(args.message_text),
        subject=str(args.subject),
    )


if __name__ == "__main__":
    run()
