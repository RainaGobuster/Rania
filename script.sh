#!/bin/bash
exec > /root/script.log 2>&1

screen -dmS check
screen -S check -X stuff "cd /root/setup\n"
sleep 10
screen -S check -X stuff "python3 check.py\n"

screen -dmS setup_bot
screen -S setup_bot -X stuff "cd /root/setup\n"
sleep 10
screen -S setup_bot -X stuff "python3 main.py\n"

