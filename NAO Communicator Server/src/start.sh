#!/bin/bash

killall communication_server.py
killall avahi-publish-service
nohup python /home/nao/naocom/communication_server.py > /dev/null 2>&1 &
