import cv2
import numpy as np
import picamera
import time

file_name = 'paint/right'
file_format = '.jpg'

path = file_name + file_format


# Define the minimum and maximum values for the HSV color space for black
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 46])


# Capture a frame from the camera
frame = cv2.imread(path)

# Convert the frame to HSV color space
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Threshold the HSV image to get a binary image of the black line
mask = cv2.inRange(hsv, lower_black, upper_black)

# Find contours in the thresholded frame
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

frame_BW = np.zeros_like(frame)
# Draw the contours on the frame
cv2.drawContours(frame_BW, contours, -1, (255, 255, 255), -1)

out_path = file_name + '_out' + file_format

cv2.imwrite(out_path,frame_BW)

# Close all OpenCV windows
cv2.destroyAllWindows()
