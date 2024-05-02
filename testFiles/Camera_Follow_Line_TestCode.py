from time import *
import RPi.GPIO as GPIO
import cv2
import picamera
from picamera.array import PiRGBArray
from smbus import SMBus


def followLine(camera, rawCapture):
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
                print("turn right")

            if 130 > cx > 60:
                print("forward")

            if cx <= 60:
                print("turn left")

        if key == ord("q"):
            print("Stopping")
            break

        rawCapture.truncate(0)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Initialize camera
    camera = picamera.PiCamera()
    camera.resolution = (192, 112)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(192, 112))
    sleep(0.1)
    followLine(camera, rawCapture)
    GPIO.cleanup()
