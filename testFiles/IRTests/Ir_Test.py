from time import *
import RPi.GPIO as GPIO
from smbus import SMBus

SENSOR_L = 15
SENSOR_H = 0
SENSOR_M = (SENSOR_H + SENSOR_L) / 2


#   GrayScale   SMBus regs      addr=20
#   18  17  16
#   L   M   R

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


def followLine():
    try:
        while True:
            print(tracker.read())
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    initBus()

    tracker = Tracker()

    followLine()
