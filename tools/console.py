#!/usr/bin/env python3
import serial
import time


PORT = "/dev/ttyUSB0" # or /dev/ttyDUT0 from udev rule
BAUD = 115200
TIMEOUT = 1


with serial.Serial(PORT, BAUD, timeout=TIMEOUT) as ser:
    ser.reset_input_buffer()
    t0 = time.time()
    while time.time() - t0 < 5:
        line = ser.readline().decode(errors="ignore").rstrip()
        if line:
            print(line)