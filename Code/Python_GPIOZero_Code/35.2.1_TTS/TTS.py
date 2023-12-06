#!/usr/bin/env python3
#############################################################################
# Filename    : TTS.py
# Description : Make TTS alerts using the speaker amplifier module PAM8403.
# Author      : www.freenove.com
# modification: 2023/05/15
########################################################################
import os
import time

from sensor import InfraredSensor

sensorPin = 18  # define sensorPin
sensor = InfraredSensor(sensorPin, pull_up=True)


def SensorEvent():  # The sensor is blocked
    print("Hello, please  stay away")
    os.system("espeak 'Hello, please  stay away'")


def loop():
    sensor.when_reflect = SensorEvent
    while True:
        time.sleep(1)


def destroy():
    sensor.close()


if __name__ == "__main__":  # Program entrance
    print("Program is starting...")
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
        print("Ending program")
