#!/usr/bin/env bash
echo "Activating environment." > /tmp/magic_init.log
source /home/pi/.virtualenv/magic/bin/activate

echo "Entering app folder." >> /tmp/magic_init.log
cd /home/pi/dev/magic_mirror

echo "Setting display." >> /tmp/magic_init.log
export DISPLAY=:0

echo "Launching magic mirror." >> /tmp/magic_init.log
./main.py -f >> logs.txt
