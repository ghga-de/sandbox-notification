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
  python sender.py "$RNAME" "$REMAIL" "$MESSAGE" "$SUBJECT"
"""

import argparse
from datetime import datetime
import json
import logging
from pathlib import Path
import pika


def main(notification: argparse.Namespace):
    """Run a test for publishing a notification."""
    Path(Path(__file__).parent / "logs/").mkdir(exist_ok=True)
    logging.basicConfig(
        filename=(
            str(Path(__file__).parent.resolve())
            + "/logs/"
            + datetime.now().isoformat(timespec="milliseconds")
            + "_publisher.log"
        ),
        level=logging.INFO,
    )

    messageobj = {
        "recipient_name": str(notification.recipient_name),
        "recipient_email": str(notification.recipient_email),
        "message": str(notification.message),
        "subject": str(notification.subject),
    }

    msgjson = json.dumps(messageobj)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.exchange_declare(exchange="notifications", exchange_type="topic")

    routing_key = "test.sandbox.notifications"

    channel.basic_publish(
        exchange="notifications",
        routing_key=routing_key,
        body=msgjson,
        properties=pika.BasicProperties(delivery_mode=2),
    )
    logging.info(
        " [x] %s: Sent notification.", datetime.now().isoformat(timespec="milliseconds")
    )
    connection.close()


def run():
    """Run the publisher testing script."""
    parser = argparse.ArgumentParser(
        description="Send a notification message to another script that send a notification email."
    )
    parser.add_argument("recipient_name", type=str)
    parser.add_argument("recipient_email", type=str)
    parser.add_argument("message", type=str)
    parser.add_argument("subject", type=str)
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    run()
