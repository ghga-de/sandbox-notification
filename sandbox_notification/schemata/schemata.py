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

"""Get Schemata for Async Messaging"""

import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).parent.resolve()


@lru_cache
def get_schema(message_type: str):
    """Get schema for a specific message_type.
    This function is cached.

    Args:
        message_type (str): Type of message.
    """
    json_schema_path = HERE / f"{message_type}.json"

    with open(json_schema_path, "r", encoding="utf-8") as schema_file:
        schema_dict = json.load(schema_file)

    return schema_dict
