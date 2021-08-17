#!/bin/bash

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

cd /workspace/.devcontainer
mkdir -p ./logs

(sandbox-notification > logs/svc_1.log 2>&1) &
pid[0]=$!
sleep 0.1
(sandbox-notification > logs/svc_2.log 2>&1) &
pid[1]=$!

trap "kill ${pid[0]}; kill ${pid[1]}; exit" INT EXIT TERM

while true
do
    echo
    echo "---"
    echo "Send notification (check /sandbox_notification/logs/ for consumer processes logs)."
    echo "Recipient name:"
    read RNAME
    echo "Recipient email:"
    read REMAIL
    echo "Message:"
    read MESSAGE
    echo "Subject:"
    read SUBJECT

    ./example_publisher.py "$RNAME" "$REMAIL" "$MESSAGE" "$SUBJECT" > logs/pub.log
done
