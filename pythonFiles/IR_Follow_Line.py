from time import *
from smbus import SMBus
import RPi.GPIO as GPIO

SENSOR_LOW_VALUE = 15
SENSOR_HIGH_VALUE = 0
SENSOR_MIDDLE_VALUE = (SENSOR_LOW_VALUE + SENSOR_HIGH_VALUE) / 2
HAT_ADDR = 20

#       MOTORS      SMBus regs      addr=20
#   LF  45  44  RF
#   LB  40  41  RB
#                   GPIO.OUT pins
#   LF  23  24  RF
#   LB  13  20  RB

#   Speed Input values
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
    def __init__(self, reg, pin, bus):
        self.reg = reg
        self.pin = pin
        self.bus = bus
        self.direction = 1
        GPIO.setup(self.pin, GPIO.OUT)

    def set_power(self, power):
        GPIO.output(self.pin, self.direction)
        self.bus.write_word_data(HAT_ADDR, self.reg, power)

    def stop(self):
        self.bus.write_word_data(HAT_ADDR, self.reg, 0)

    def set_backwards(self):
        self.direction = 0

    def set_forwards(self):
        self.direction = 1


class Tracker:
    def __init__(self, bus):
        self.left = 0
        self.center = 0
        self.right = 0
        self.left_reg = 18
        self.center_reg = 17
        self.right_reg = 16
        self.bus = bus

    def read(self):
        self.bus.write_word_data(HAT_ADDR, self.left_reg, 0)
        self.left = self.bus.read_byte(HAT_ADDR)
        self.bus.read_byte(HAT_ADDR)
        self.bus.write_word_data(HAT_ADDR, self.center_reg, 0)
        self.center = self.bus.read_byte(HAT_ADDR)
        self.bus.read_byte(HAT_ADDR)
        self.bus.write_word_data(HAT_ADDR, self.right_reg, 0)
        self.right = self.bus.read_byte(HAT_ADDR)
        self.bus.read_byte(HAT_ADDR)
        return self.left, self.center, self.right


class Car:
    def __init__(self, left_front, left_back, right_front, right_back, tracker):
        self.left_front = left_front
        self.left_back = left_back
        self.right_front = right_front
        self.right_back = right_back
        self.tracker = tracker

    def forward(self, power):
        self.left_front.set_forwards()
        self.left_back.set_forwards()
        self.right_front.set_forwards()
        self.right_back.set_forwards()
        self.left_front.set_power(power)
        self.left_back.set_power(power)
        self.right_front.set_power(power)
        self.right_back.set_power(power)

    def turn_left(self, power):
        self.left_front.set_backwards()
        self.left_back.set_backwards()
        self.right_front.set_forwards()
        self.right_back.set_forwards()
        self.left_front.set_power(power)
        self.left_back.set_power(power)
        self.right_front.set_power(power)
        self.right_back.set_power(power)

    def turn_right(self, power):
        self.left_front.set_forwards()
        self.left_back.set_forwards()
        self.right_front.set_backwards()
        self.right_back.set_backwards()
        self.left_front.set_power(power)
        self.left_back.set_power(power)
        self.right_front.set_power(power)
        self.right_back.set_power(power)

    def stop(self):
        self.left_front.stop()
        self.left_back.stop()
        self.right_front.stop()
        self.right_back.stop()

    def read(self):
        self.tracker.read()

    def getTrackerLeft(self):
        return self.tracker.left

    def getTrackerCenter(self):
        return self.tracker.center

    def getTrackerRight(self):
        return self.tracker.right


def initBus(bus):
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(21, 0)
    sleep(0.01)
    GPIO.output(21, 1)
    sleep(0.01)
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


def followLine(car, speed):
    lost_read_count = 0
    try:
        while True:
            car.read()
            if car.getTrackerLeft() > SENSOR_MIDDLE_VALUE and car.getTrackerRight() > SENSOR_MIDDLE_VALUE:
                car.forward(speed)
            elif car.getTrackerLeft() < SENSOR_MIDDLE_VALUE < car.getTrackerRight():
                car.turn_left(speed)
            elif car.getTrackerRight() < SENSOR_MIDDLE_VALUE < car.getTrackerLeft():
                car.turn_right(speed)
            elif car.getTrackerLeft() < SENSOR_MIDDLE_VALUE and car.getTrackerCenter() < SENSOR_MIDDLE_VALUE and car.getTrackerRight() < SENSOR_MIDDLE_VALUE:
                car.stop()
            else:
                lost_read_count += 1
                if lost_read_count == 1:
                    start_time = time()
                if lost_read_count > 10:
                    car.stop()
                    print(time() - start_time)
                    break
    except KeyboardInterrupt:
        car.stop()


if __name__ == '__main__':
    # Initialize the GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Initialize the I2C bus
    bus = SMBus(1)
    sleep(1)
    initBus(bus)
    # Initialize the motors
    left_front = Motor(45, 23, bus)
    left_back = Motor(40, 13, bus)
    right_front = Motor(44, 24, bus)
    right_back = Motor(41, 20, bus)
    # Initialize the tracker
    tracker = Tracker(bus)
    # Initialize the car
    car = Car(left_front, left_back, right_front, right_back, tracker)
    # Follow the line
    followLine(car, SPEED_20)
