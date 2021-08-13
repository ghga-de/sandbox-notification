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

"""Consuming or subscribing to channels"""

from datetime import datetime
import json
import logging
from pathlib import Path
import pika
import jsonschema
from .core.send import send_email, MaxAttemptsReached

HERE = Path(__file__).parent.resolve()
NOTIFICATION_SCHEMA = HERE / "schemata" / "notification.json"


def callback(
    channel: pika.channel.Channel,
    method: pika.spec.Basic.Deliver,
    _: pika.spec.BasicProperties,
    body: str,
):
    """Executed once a message is received"""

    messageobj = json.loads(body)
    logging.info(
        " [x] %s: Message received", datetime.now().isoformat(timespec="milliseconds")
    )

    with open(NOTIFICATION_SCHEMA) as schema:
        try:
            jsonschema.validate(instance=messageobj, schema=json.load(schema))
        except jsonschema.exceptions.ValidationError as exc:
            logging.error(
                "%s: Message package does not comform to JSON schema.",
                datetime.now().isoformat(timespec="milliseconds"),
            )
            logging.exception(exc)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    try:
        send_email(messageobj)
    except (MaxAttemptsReached, ValueError):
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    else:
        channel.basic_ack(delivery_tag=method.delivery_tag)


def subscribe(topic_str: str):
    """Subscribe this consumer to a topic or set of topics based on a
    topic string as defined in the AMQP 0.9.1 specification."""

    Path(Path(__file__).parent / "logs/").mkdir(exist_ok=True)
    logging.basicConfig(
        filename=(
            str(Path(__file__).parent.resolve())
            + "/logs/"
            + datetime.now().isoformat(timespec="milliseconds")
            + "_consumer.log"
        ),
        level=logging.INFO,
    )

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.exchange_declare(exchange="notifications", exchange_type="topic")

    result = channel.queue_declare(queue="notifications", durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange="notifications", queue="notifications", routing_key=topic_str
    )

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    logging.info(
        " [*] %s: Waiting for notification.",
        datetime.now().isoformat(timespec="milliseconds"),
    )
    channel.start_consuming()
