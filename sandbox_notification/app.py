"""
app.py This module serves as the entry point for the application.
"""

import uvicorn

from fastapi import FastAPI
from service import send_mail
from config import config

app = FastAPI()
CONFIG_YAML = "example_config.yaml"
HOST = 'host'
PORT = 'port'
config_data = config.get_config(CONFIG_YAML)


@app.get("/")
async def send_email():
    """
    send mail
    :return:
    """
    sender = "example@gmail.com"
    receiver = ["receiver@example.com"]
    subject = "hey"
    message = "hello world"
    send_mail.send_email(sender, receiver, subject, message)
    return "Mail sent"


if __name__ == "__main__":
    uvicorn.run("app:app",
                host=config_data[HOST],
                port=config_data[PORT],
                log_level="info")
