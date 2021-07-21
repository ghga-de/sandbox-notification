#!/usr/bin/env python
import pika, json, smtplib, sys, time
from email.message import EmailMessage

SENDER_EMAIL = 'contact@ghga.de'
EMAIL_SUBJECT = 'GHGA Sandbox Notification'
MAX_ATTEMPTS = 5

def send_email(recipient_email, message, smtp_server, smtp_port, smtp_username, smtp_password):
    """
    send email
    :return:
    """
    msg = EmailMessage()
    msg['Subject'] = EMAIL_SUBJECT
    # Does not work when sent from Gmail
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg.set_content(message)
    server = smtplib.SMTP(smtp_server, int(smtp_port))
    server.starttls()
    server.ehlo()
    server.login(smtp_username, smtp_password)
    server.send_message(msg)
    server.quit()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='notifications', exchange_type='topic')

result = channel.queue_declare(queue='notifications', durable=True)
queue_name = result.method.queue

channel.queue_bind(exchange='notifications', queue='notifications', routing_key='#.notifications.#')

print(' [*] Waiting for notification. To exit press CTRL+C')

def callback(ch, method, properties, body):
    messageobj = json.loads(body)
    print(" [x] Message received")

    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        try:
            send_email(messageobj['recipient_email'], messageobj['message'], messageobj['smtp_server'], messageobj['smtp_port'], messageobj['smtp_username'], messageobj['smtp_password'])
            time.sleep(5)
            print('  [>] Email notification sent.\n')
            break
        except Exception:
            print(f"There has been an error sending an e-mail notification on attempt {attempt}/{MAX_ATTEMPTS}.")
            attempt += 1
            time.sleep(5)
    else:
        print ('Error: Maximum number of attempts reached. Email could not be sent.')
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print(' [*] Waiting for notification. To exit press CTRL+C')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=queue_name, on_message_callback=callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print()
    sys.exit(0)