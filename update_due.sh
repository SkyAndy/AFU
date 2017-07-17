#!/bin/bash
# uploading firmware on Arduino DUE from raspi console
# compile firmware on external PC an copy it via ssh to /tmp/update.bin
# aptitude install bossa-cli
stty -F /dev/ttyACM0 speed 1200 cs8 -cstopb -parenb > /dev/null 2>&1
killall -9 MMDVMHost
sleep 3
/usr/bin/bossac --port=ttyACM0 --force_usb_port=false --erase --write --verify --boot=1 --reset /tmp/update.bin
sleep 3
stty -F /dev/ttyACM0 speed 115200 cs8 -cstopb -parenb > /dev/null 2>&1
sleep 3
echo "ready... please start your MMDVMHost service"
