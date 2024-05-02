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

# Functions to control the movement of the robot
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

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#
initBus()

left_front = Motor(45, 23)
left_back = Motor(40, 13)
right_front = Motor(44, 24)
right_back = Motor(41, 20)

# Initialize camera
camera = picamera.PiCamera()
camera.resolution = (192, 112)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(192, 112))
sleep(0.1)

# Loop over all frames captured by camera indefinitely
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
    
    cv2.imshow('mask',mask)

    # Find all contours in frame
    contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find x-axis centroid of largest contour and cut power to appropriate motor
    # to recenter camera on centroid.
    # This control algorithm was written referencing guide:
    # Author: Einsteinium Studios
    # Availability: http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html
    if len(contours) > 0:
        # Find largest contour area and image moments
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        # Find x-axis centroid using image moments
        cx = int(M['m10'] / M['m00'])

        if cx >= 130:
            turn_right(SPEED_30)
            
        if cx < 130 and cx > 60:
            forward(SPEED_30)

        if cx <= 60:
            turn_left(SPEED_30)

    if key == ord("q"):
        break

    rawCapture.truncate(0)

stop()

GPIO.cleanup()

