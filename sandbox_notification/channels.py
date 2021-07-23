"""Consuming or subscribing to channels"""

import pika, json, time
from .core.send import send_email

MAX_ATTEMPTS = 5


def callback(ch, method, properties, body):
    """Executed once a message was received"""
    messageobj = json.loads(body)
    print(" [x] Message received")

    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        try:
            send_email(messageobj['recipient_email'], messageobj['message'], messageobj['smtp_server'], messageobj['smtp_port'], messageobj['smtp_username'], messageobj['smtp_password'])
            print('  [>] Email notification sent.\n')
            break
        except Exception:
            print(f"There has been an error sending an e-mail notification on attempt {attempt}/{MAX_ATTEMPTS}.")
            attempt += 1
            time.sleep(5)
    else:
        print ('Error: Maximum number of attempts reached. Email could not be sent.')
    ch.basic_ack(delivery_tag = method.delivery_tag)


def subscribe():
    """Subscribe to "notifications" topic"""

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.exchange_declare(exchange='notifications', exchange_type='topic')

    result = channel.queue_declare(queue='notifications', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='notifications', queue='notifications', routing_key='#.notifications.#')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue_name, 
        on_message_callback=callback
    )
    
    print(' [*] Waiting for notification.')
    channel.start_consuming()

