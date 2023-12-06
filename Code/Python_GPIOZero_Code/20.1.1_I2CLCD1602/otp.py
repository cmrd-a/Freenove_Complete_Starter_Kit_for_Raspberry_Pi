from datetime import datetime
from time import sleep

import pyotp
from LCD1602 import CharLCD1602

lcd1602 = CharLCD1602()

totp = pyotp.TOTP("")


def get_time_now() -> str:
    return datetime.now().strftime("     %H:%M")


def get_otp_now() -> str:
    otp = totp.now()
    return f"{' '*4}{otp[0:3]} {otp[3:6]}"


def loop() -> None:
    lcd1602.init_lcd()
    while True:
        lcd1602.clear()
        lcd1602.write(0, 1, get_otp_now())
        lcd1602.write(0, 0, get_time_now())
        sleep(15)


def destroy() -> None:
    lcd1602.clear()


if __name__ == "__main__":
    print("Program is starting ... ")
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
