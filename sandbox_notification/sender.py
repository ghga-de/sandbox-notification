"""
app.py This module serves as the entry point for the application.
"""

#!/usr/bin/env python
import pika, sys, json

messageobj = {
  'sender': 'userid',
  'recipient': 'userid',
  'recipient_name': 'Jordy',
  'email': 'jorellanaf@outlook.com',
  'message': 'Hello.'
}

message = json.dumps(messageobj)
print(message)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='notifications', exchange_type='fanout')

channel.basic_publish(exchange='notifications', routing_key='', body=message)
print(' [x] Sent %r' % message)
connection.close()