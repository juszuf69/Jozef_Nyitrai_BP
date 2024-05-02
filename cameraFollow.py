"""
import cv2
import numpy as np
import picamera
from time import *
import RPI.GPIO as GPIO
from smbus import SMBus

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
"""
# functions
# Function to get the leftmost and rightmost points of the biggest contour in picture
def get_left_right_points(contour):
    # Initialize leftmost and rightmost points with extreme values
    leftmost = tuple(contour[0][0])
    rightmost = tuple(contour[0][0])

    # Iterate through all points in the contour to find leftmost and rightmost
    for point in contour:
        point = tuple(point[0])  # Convert to tuple for easier comparison

        # Update leftmost point if current point is more left
        if point[0] < leftmost[0]:
            leftmost = point

        # Update rightmost point if current point is more right
        if point[0] > rightmost[0]:
            rightmost = point

    return leftmost, rightmost
"""

from time import *

import RPi.GPIO as GPIO
import cv2
import picamera
from picamera.array import PiRGBArray
from smbus import SMBus


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
"""
# Function to follow the black line
def followLine(speed):
    # Set up the camera
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = camera.MAX_FRAMERATE

    # Start the camera preview
    camera.start_preview()
    time.sleep(0.5)

    # Define the minimum and maximum values for the HSV color space for black
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 46])

    while True:
        # Capture a frame from the camera
        camera.capture('frame.jpg')
        frame = cv2.imread('frame.jpg')

        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get a binary image of the black line
        mask = cv2.inRange(hsv, lower_black, upper_black)

        # Find contours in the thresholded frame
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        frame_BW = np.zeros_like(frame)
        # Draw the contours on the frame
        cv2.drawContours(frame_BW, contours, -1, (255, 255, 255), -1)
        cv2.imwrite('frame2.jpg', frame_BW)
        frame_BW = cv2.imread('frame2.jpg', cv2.IMREAD_GRAYSCALE)

        height, width = frame_BW.shape[:2]
        roi_start = height // 4
        roi_end = 3 * height // 4
        roi_pic = frame_BW[roi_start:roi_end, :]

        # Preprocessing
        _, thresh = cv2.threshold(roi_pic, 127, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            left_most_p, right_most_p = get_left_right_points(largest_contour)

            # Example decision making based on points in countour
            if left_most_p[0] < 200:
                turn_left(speed)
            elif right_most_p[0] > 440:
                turn_right(speed)
            else:
                forward(speed)
        else:
            stop()

        # Break the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Release the camera
    camera.stop_preview()
    camera.close()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

# main

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    initBus()

    left_front = Motor(45, 23)
    left_back = Motor(40, 13)
    right_front = Motor(44, 24)
    right_back = Motor(41, 20)

    followLine(SPEED_20)
"""

# Gregory Mueth
# 2635999
# EEL 4660 Robotics Systems
# Fall 2017

# line-follower.py

# A line following robot for Robotics Systems final project
# Coded using Python 2.7.13 and OpenCV 3.3 for a Raspberry Pi 3B running Raspbian
# Uses Raspberry Pi camera module v2

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
