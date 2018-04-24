#!/usr/bin/env bash
cd /home/pi/dev/magic_mirror
source /home/pi/.virtualenv/magic/bin/activate
export DISPLAY=:0
./main.py -f
