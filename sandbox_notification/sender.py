"""
app.py This module serves as the entry point for the application.
"""

#!/usr/bin/env python
import pika, sys, json, argparse

def main(args):
  messageobj = {
    'sender': 'userid',
    'recipient': 'userid',
    'recipient_name': args.recipient_name,
    'recipient_email': args.recipient_email,
    'message': 'Dear ' + args.recipient_name + '.\nThis is a notification from the GHGA sandbox notification service.',
    'smtp_server': args.smtp_server,
    'smtp_port': args.smtp_port,
    'smtp_username': args.smtp_username,
    'smtp_password': args.smtp_password,
  }

  message = json.dumps(messageobj)

  connection = pika.BlockingConnection(
      pika.ConnectionParameters(host='rabbitmq'))
  channel = connection.channel()

  channel.exchange_declare(exchange='notifications', exchange_type='fanout')

  channel.basic_publish(exchange='notifications', routing_key='', body=message)
  print(' [x] Sent notification.')
  connection.close()

if __name__=="__main__":
  parser = argparse.ArgumentParser(description = 'Send a notification message to another script that send a notification email.')
  parser.add_argument('recipient_name', type=str)
  parser.add_argument('recipient_email', type=str)
  parser.add_argument('smtp_server', type=str)
  parser.add_argument('smtp_port', type=str)
  parser.add_argument('smtp_username', type=str)
  parser.add_argument('smtp_password', type=str)
  args = parser.parse_args()
  main(args)