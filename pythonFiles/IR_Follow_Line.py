from time import *
from smbus import SMBus
import RPi.GPIO as GPIO
import cv2

SENSOR_L = 15
SENSOR_H = 0
SENSOR_M = (SENSOR_H + SENSOR_L) / 2

#       MOTORS      SMBus regs      addr=20
#   LF  45  44  RF
#   LB  40  41  RB
#                   GPIO.OUT pins
#   LF  23  24  RF
#   LB  13  20  RB
#
#   Input values
SPEED_0 = 0
SPEED_10 = 37634
SPEED_20 = 52994
SPEED_30 = 2819
SPEED_40 = 18179
SPEED_50 = 33539
SPEED_60 = 48899
SPEED_70 = 64259
SPEED_80 = 14084
SPEED_90 = 29444


#   GrayScale   SMBus regs      addr=20
#   18  17  16
#   L   M   R

class Motor:
    def __init__(self, reg, pin):
        self.reg = reg
        self.pin = pin
        self.direction = 1
        GPIO.setup(self.pin, GPIO.OUT)

    def set_power(self, power):
        bus = SMBus(1)
        GPIO.output(self.pin, self.direction)
        bus.write_word_data(20, self.reg, power)

    def stop(self):
        bus = SMBus(1)
        bus.write_word_data(20, self.reg, 0)

    def set_backwards(self):
        self.direction = 0

    def set_forwards(self):
        self.direction = 1


class Tracker:
    def __init__(self):
        self.left = 0
        self.middle = 0
        self.right = 0
        self.left_reg = 18
        self.middle_reg = 17
        self.right_reg = 16
        GPIO.setup(21, GPIO.IN)

    def read(self):
        bus = SMBus(1)
        bus.write_word_data(20, self.left_reg, 0)
        self.left = bus.read_byte(20)
        bus.read_byte(20)
        bus.write_word_data(20, self.middle_reg, 0)
        self.middle = bus.read_byte(20)
        bus.read_byte(20)
        bus.write_word_data(20, self.right_reg, 0)
        self.right = bus.read_byte(20)
        bus.read_byte(20)
        return self.left, self.middle, self.right


def forward(power):
    left_front.set_forwards()
    left_back.set_forwards()
    right_front.set_forwards()
    right_back.set_forwards()
    left_front.set_power(power)
    left_back.set_power(power)
    right_front.set_power(power)
    right_back.set_power(power)


def backward(power):
    left_front.set_backwards()
    left_back.set_backwards()
    right_front.set_backwards()
    right_back.set_backwards()
    left_front.set_power(power)
    left_back.set_power(power)
    right_front.set_power(power)
    right_back.set_power(power)


def turn_left(power):
    left_front.set_backwards()
    left_back.set_backwards()
    right_front.set_forwards()
    right_back.set_forwards()
    left_front.set_power(power)
    left_back.set_power(power)
    right_front.set_power(power)
    right_back.set_power(power)


def turn_right(power):
    left_front.set_forwards()
    left_back.set_forwards()
    right_front.set_backwards()
    right_back.set_backwards()
    left_front.set_power(power)
    left_back.set_power(power)
    right_front.set_power(power)
    right_back.set_power(power)


def stop():
    left_front.set_power(0)
    left_back.set_power(0)
    right_front.set_power(0)
    right_back.set_power(0)


def initBus():
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(21, 0)
    sleep(0.01)
    GPIO.output(21, 1)
    sleep(0.01)
    bus = SMBus(1)
    sleep(1)
    bus.write_word_data(20, 67, 44804)
    bus.write_word_data(20, 71, 44804)
    bus.write_word_data(20, 67, 44804)
    bus.write_word_data(20, 71, 44804)
    bus.write_word_data(20, 66, 44804)
    bus.write_word_data(20, 70, 44804)
    bus.write_word_data(20, 66, 44804)
    bus.write_word_data(20, 70, 44804)
    bus.write_word_data(20, 64, 44804)
    bus.write_word_data(20, 68, 44804)
    bus.write_word_data(20, 68, 65039)
    bus.write_word_data(20, 64, 24065)
    bus.write_word_data(20, 64, 44804)
    bus.write_word_data(20, 68, 44804)
    bus.write_word_data(20, 68, 65039)
    bus.write_word_data(20, 64, 24065)


def followLine(speed):
    key = cv2.waitKey(1) & 0xFF
    while True:
        tracker.read()
        if tracker.left > SENSOR_M and tracker.right > SENSOR_M:
            forward(speed)
        elif tracker.left < SENSOR_M < tracker.right:
            turn_left(speed)
        elif tracker.right < SENSOR_M < tracker.left:
            turn_right(speed)
        elif tracker.left < SENSOR_M and tracker.middle < SENSOR_M and tracker.right < SENSOR_M:
            stop()
        if key == ord("q"):
            stop()
            break


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    #initBus()

    left_front = Motor(45, 23)
    left_back = Motor(40, 13)
    right_front = Motor(44, 24)
    right_back = Motor(41, 20)

    tracker = Tracker()

    followLine(SPEED_20)