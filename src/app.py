from flask import Flask
from service import send_email

server = Flask(__name__)


@server.route("/")
def hello():
    """
    hello world
    :return:
    """
    sender = "mani.ghga@gmail.com"
    receiver = "manikandan.ravichandran@dkfz-heidelberg.de"
    subject = "hey"
    message = "hello world 3"
    send_email.send_email(sender, receiver, subject, message)
    return "Hello World!"


if __name__ == "__main__":
    server.run(host='0.0.0.0')
