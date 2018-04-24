#!/usr/bin/env bash
echo "Activating environment." > /var/log/magic_init.log
source /home/pi/.virtualenv/magic/bin/activate

echo "Entering app folder." >> /var/log/magic_init.log
cd /home/pi/dev/magic_mirror

echo "Setting display." >> /var/log/magic_init.log
export DISPLAY=:0

echo "Launching magic mirror." >> /var/log/magic_init.log
./main.py -f
