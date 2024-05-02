from time import *
import RPi.GPIO as GPIO
import cv2
import picamera
from picamera.array import PiRGBArray
from smbus import SMBus

"""
# constants

#       MOTORS      SMBus regs      addr=20
#   LF  45  44  RF
#   LB  40  41  RB
#                   GPIO.OUT pins
#   LF  23  24  RF
#   LB  13  20  RB
#
"""
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

SPEED = SPEED_30


# classes
# Motor class
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


# Car class
class Car:
    def __init__(self, left_front, left_back, right_front, right_back):
        self.left_front = left_front
        self.left_back = left_back
        self.right_front = right_front
        self.right_back = right_back

    def forward(self, power):
        self.left_front.set_forwards()
        self.left_back.set_forwards()
        self.right_front.set_forwards()
        self.right_back.set_forwards()
        self.left_front.set_power(power)
        self.left_back.set_power(power)
        self.right_front.set_power(power)
        self.right_back.set_power(power)

    def backward(self, power):
        self.left_front.set_backwards()
        self.left_back.set_backwards()
        self.right_front.set_backwards()
        self.right_back.set_backwards()
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


# Functions to control the movement of the robot
def forward(car, power):
    car.forward(power)


def backward(car, power):
    car.backward(power)


def turn_left(car, power):
    car.turn_left(power)


def turn_right(car, power):
    car.turn_right(power)


def stop(car):
    car.stop()


# Function to initialize the I2C bus
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


# main
def __main__():
    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Initialize I2C bus
    initBus()
    # Initialize motors
    left_front = Motor(45, 23)
    left_back = Motor(40, 13)
    right_front = Motor(44, 24)
    right_back = Motor(41, 20)
    # initialize car
    car = Car(left_front, left_back, right_front, right_back)
    # Initialize camera
    camera = picamera.PiCamera()
    camera.resolution = (192, 112)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(192, 112))
    sleep(0.1)
    followLine(camera, rawCapture, car)
    GPIO.cleanup()


def followLine(camera, rawCapture, car):
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        # Display camera input
        image = frame.array

        height, width = image.shape[:2]
        roi_start = height // 4
        roi_end = 3 * height // 4
        image = image[roi_start:roi_end, :]

        cv2.imshow('img', image)

        # Create key to break for loop
        key = cv2.waitKey(1) & 0xFF

        # convert to grayscale, gaussian blur, and threshold
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh1 = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

        # Erode to eliminate noise, Dilate to restore eroded parts of image
        mask = cv2.erode(thresh1, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cv2.imshow('mask', mask)

        # Find all contours in frame
        contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

        # Find x-axis centroid of largest contour and cut power to appropriate motor
        # to recenter camera on centroid.
        if len(contours) > 0:
            # Find largest contour area and image moments
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            # Find x-axis centroid using image moments
            cx = int(M['m10'] / M['m00'])

            if cx >= 130:
                turn_right(car, SPEED)

            if cx < 130 and cx > 60:
                forward(car, SPEED)

            if cx <= 60:
                turn_left(car, SPEED)

        if key == ord("q"):
            stop(car)
            break

        rawCapture.truncate(0)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    __main__()
