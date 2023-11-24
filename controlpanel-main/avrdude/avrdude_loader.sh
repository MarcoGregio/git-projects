#! /bin/bash
avrdude -v -patmega2560 -cwiring -P/dev/ttyACM0 -b115200 -D -Uflash:w:/home/pi/HMI/avrdude/hexacode.ino.mega.hex:i
