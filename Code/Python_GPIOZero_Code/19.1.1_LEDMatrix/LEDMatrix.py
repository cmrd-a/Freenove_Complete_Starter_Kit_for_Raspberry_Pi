#!/usr/bin/env python3
#############################################################################
# Filename    : LEDMatrix.py
# Description : Control LEDMatrix with 74HC595
# auther      : www.freenove.com
# modification: 2023/05/15
########################################################################
import time

from gpiozero import OutputDevice

LSB_FIRST = 1
MSB_FIRST = 2
# define the pins connect to 74HC595
data_pin = OutputDevice(17)  # DS Pin of 74HC595(Pin14)
latch_pin = OutputDevice(27)  # ST_CP Pin of 74HC595(Pin12)
clock_pin = OutputDevice(22)  # CH_CP Pin of 74HC595(Pin11)
pic = [0x1C, 0x22, 0x51, 0x45, 0x45, 0x51, 0x22, 0x1C]  # data of smiling face
data = [  # data of "0-F"
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,  # " "
    0x00,
    0x00,
    0x3E,
    0x41,
    0x41,
    0x3E,
    0x00,
    0x00,  # "0"
    0x00,
    0x00,
    0x21,
    0x7F,
    0x01,
    0x00,
    0x00,
    0x00,  # "1"
    0x00,
    0x00,
    0x23,
    0x45,
    0x49,
    0x31,
    0x00,
    0x00,  # "2"
    0x00,
    0x00,
    0x22,
    0x49,
    0x49,
    0x36,
    0x00,
    0x00,  # "3"
    0x00,
    0x00,
    0x0E,
    0x32,
    0x7F,
    0x02,
    0x00,
    0x00,  # "4"
    0x00,
    0x00,
    0x79,
    0x49,
    0x49,
    0x46,
    0x00,
    0x00,  # "5"
    0x00,
    0x00,
    0x3E,
    0x49,
    0x49,
    0x26,
    0x00,
    0x00,  # "6"
    0x00,
    0x00,
    0x60,
    0x47,
    0x48,
    0x70,
    0x00,
    0x00,  # "7"
    0x00,
    0x00,
    0x36,
    0x49,
    0x49,
    0x36,
    0x00,
    0x00,  # "8"
    0x00,
    0x00,
    0x32,
    0x49,
    0x49,
    0x3E,
    0x00,
    0x00,  # "9"
    0x00,
    0x00,
    0x3F,
    0x44,
    0x44,
    0x3F,
    0x00,
    0x00,  # "A"
    0x00,
    0x00,
    0x7F,
    0x49,
    0x49,
    0x36,
    0x00,
    0x00,  # "B"
    0x00,
    0x00,
    0x3E,
    0x41,
    0x41,
    0x22,
    0x00,
    0x00,  # "C"
    0x00,
    0x00,
    0x7F,
    0x41,
    0x41,
    0x3E,
    0x00,
    0x00,  # "D"
    0x00,
    0x00,
    0x7F,
    0x49,
    0x49,
    0x41,
    0x00,
    0x00,  # "E"
    0x00,
    0x00,
    0x7F,
    0x48,
    0x48,
    0x40,
    0x00,
    0x00,  # "F"
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,  # " "
]


def shift_out(order, val):
    for i in range(0, 8):
        clock_pin.off()
        if order == LSB_FIRST:
            data_pin.on() if (0x01 & (val >> i) == 0x01) else data_pin.off()
        elif order == MSB_FIRST:
            data_pin.on() if (0x80 & (val << i) == 0x80) else data_pin.off()
        clock_pin.on()


def loop():
    while True:
        for j in range(0, 500):  # Repeat enough times to display the smiling face a period of time
            x = 0x80
            for i in range(0, 8):
                latch_pin.off()
                shift_out(MSB_FIRST, pic[i])  # first shift data of line information to first stage 74HC959

                shift_out(MSB_FIRST, ~x)  # then shift data of column information to second stage 74HC959
                latch_pin.on()  # Output data of two stage 74HC595 at the same time
                time.sleep(0.001)  # display the next column
                x >>= 1
        for k in range(0, len(data) - 8):  # len(data) total number of "0-F" columns
            for j in range(
                0, 20
            ):  # times of repeated displaying LEDMatrix in every frame, the bigger the "j", the longer the display time.
                x = 0x80  # Set the column information to start from the first column
                for i in range(k, k + 8):
                    latch_pin.off()
                    shift_out(MSB_FIRST, data[i])
                    shift_out(MSB_FIRST, ~x)
                    latch_pin.on()
                    time.sleep(0.001)
                    x >>= 1


def destroy():
    data_pin.close()
    latch_pin.close()
    clock_pin.close()


if __name__ == "__main__":  # Program entrance
    print("Program is starting...")
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
        print("Ending program")
