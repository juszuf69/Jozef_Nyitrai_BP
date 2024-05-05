import RPi.GPIO as GPIO
from smbus2 import SMBus
from time import sleep

#       MOTORS      SMBus regs      addr=20
#   LF  45  44  RF
#   LB  40  41  RB
#                   GPIO.OUT pins
#   LF  23  24  RF
#   LB  13  20  RB

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

HAT_ADDR = 20


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


def T1(motor, motorName):
    print(motorName + " Starting")
    sleep(1)
    print(motorName + " Forwards")
    motor.set_forwards()
    motor.set_power(SPEED_20)
    sleep(1)
    print(motorName + " Stop")
    motor.stop()
    sleep(1)
    print(motorName + " Backwards")
    motor.set_backwards()
    motor.set_power(SPEED_20)
    sleep(1)
    print(motorName + " Stop")
    motor.stop()
    print(motorName + " Finished")


def T2(speed):
    print("All Motors Starting with speed " + str(speed))
    sleep(1)
    print("All Motors Forwards")
    left_front.set_forwards()
    left_back.set_forwards()
    right_front.set_forwards()
    right_back.set_forwards()
    left_front.set_power(speed)
    left_back.set_power(speed)
    right_front.set_power(speed)
    right_back.set_power(speed)
    sleep(1)
    print("All Motors Stop")
    left_front.stop()
    left_back.stop()
    right_front.stop()
    right_back.stop()
    print("All Motors Finished with speed " + str(speed))


def T3(speed):
    print("All Motors Starting with speed " + str(speed))
    sleep(1)
    print("All Motors Different Directions")
    left_front.set_forwards()
    left_back.set_backwards()
    right_front.set_forwards()
    right_back.set_backwards()
    left_front.set_power(speed)
    left_back.set_power(speed)
    right_front.set_power(speed)
    right_back.set_power(speed)
    sleep(1)
    print("All Motors Stop")
    left_front.stop()
    left_back.stop()
    right_front.stop()
    right_back.stop()
    print("All Motors Finished with speed " + str(speed))


if __name__ == '__main__':
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Initialize the bus to avoid errors
    bus = SMBus(1)
    sleep(1)
    initBus(bus)

    left_front = Motor(45, 23, bus)
    left_back = Motor(40, 13, bus)
    right_front = Motor(44, 24, bus)
    right_back = Motor(41, 20, bus)

    # Test all motors individually
    T1(left_front, "Left Front")
    T1(left_back, "Left Back")
    T1(right_front, "Right Front")
    T1(right_back, "Right Back")

    # Test motor speeds
    T2(SPEED_40)
    T2(SPEED_80)

    # Test motors in different directions
    T3(SPEED_40)

    print("All Tests Finished")
