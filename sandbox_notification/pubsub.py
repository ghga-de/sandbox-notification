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

"""Consuming or Subscribing to Async Messaging Topics"""

import pika
from ghga_service_chassis_lib.pubsub import AmqpTopic
from .config import get_config
from .core.send import send_email
from .schemata.schemata import get_schema


def get_connection_params():
    """Return a configuration object for pika"""
    config = get_config()

    return pika.ConnectionParameters(
        host=config.rabbitmq_host, port=config.rabbitmq_port
    )


def subscribe():
    """Subscribes to the `send_notifications` topic."""

    config = get_config()

    topic = AmqpTopic(
        connection_params=get_connection_params(),
        topic_name=config.topic_name,
        service_name="sandbox_notification",
        json_schema=get_schema(config.topic_name),
    )

    topic.subscribe_for_ever(exec_on_message=send_email)
