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

"""Config Parameter Modeling and Parsing"""

from typing import Literal
from functools import lru_cache
from ghga_service_chassis_lib.config import config_from_yaml
from pydantic import BaseSettings

# type alias for log level parameter
LogLevel = Literal["critical", "error", "warning", "info", "debug", "trace"]


@config_from_yaml(prefix="sandbox_notification")
class Config(BaseSettings):
    """Config parameters and their defaults."""

    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    sender_email: str

    rabbitmq_host: str
    rabbitmq_port: int
    topic_name: str = "notifications"

    max_attempts: int = 5

    log_level: LogLevel = "info"


@lru_cache
def get_config():
    """Get runtime configuration."""
    return Config()
