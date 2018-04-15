#!/usr/bin/env bash
source /home/pi/.virtualenv/magic/bin/activate
cd /home/pi/dev/magic_mirror
export DISPLAY=:0
./main.py -f >> logs.txt
