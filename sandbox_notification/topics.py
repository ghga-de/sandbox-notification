"""Consuming or subscribing to channels"""

from datetime import datetime
import json
import logging
from pathlib import Path
import time
import pika
from .core.send import send_email

MAX_ATTEMPTS = 5


def callback(channel, method, _, body):
    """Executed once a message was received"""
    messageobj = json.loads(body)
    logging.info(" [x] %s: Message received",
                    datetime.now().isoformat(timespec='milliseconds'))

    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        try:
            send_email(messageobj)
            logging.info("  [>] %s: Email notification sent.\n",
                    datetime.now().isoformat(timespec='milliseconds'))
            break
        except Exception:
            logging.warning(datetime.now().isoformat(timespec='milliseconds') + f": There has been an error sending an e-mail notification on attempt {attempt}/{MAX_ATTEMPTS}.")
            attempt += 1
            time.sleep(5)
    else:
        logging.error('%s: Maximum number of attempts reached. Email could not be sent.',
                datetime.now().isoformat(timespec='milliseconds'))
    channel.basic_ack(delivery_tag = method.delivery_tag)


def subscribe(topic_str):
    """Subscribe this consumer to a topic or set of topics based on a
    topic string as defined in the AMQP 0.9.1 specification."""
    Path('logs/').mkdir(exist_ok=True)
    logging.basicConfig(filename='logs/' +
            datetime.now().isoformat(timespec='milliseconds') + '_consumer.log',
            encoding='utf-8', level=logging.INFO)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.exchange_declare(exchange='notifications', exchange_type='topic')

    result = channel.queue_declare(queue='notifications', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='notifications', queue='notifications', routing_key=topic_str)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback
    )
    
    logging.info(" [*] %s: Waiting for notification.",
            datetime.now().isoformat(timespec='milliseconds'))
    channel.start_consuming()
