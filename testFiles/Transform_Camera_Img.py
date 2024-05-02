import cv2
import numpy as np
import picamera
import time

LEFT_TURN = 'test_Pictures/Lturn_image.jpg'
RIGHT_TURN = 'test_Pictures/Rturn_image.jpg'
STRAIGHT = 'test_Pictures/straight_line_image.jpg'
STOP = 'test_Pictures/stop_line_image.jpg'

file_name = LEFT_TURN

# Capture a frame from the camera
frame = cv2.imread(file_name)

# Display the original image
cv2.imshow('Original Image', frame)

height, width = frame.shape[:2]
roi_start = height // 4
roi_end = 3 * height // 4
frame = frame[roi_start:roi_end, :]

# Display the original image with Roi
cv2.imshow('Original Image Resized', frame)

# Convert to grayscale, gaussian blur, and threshold
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
ret, thresh1 = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

# Erode to eliminate noise, Dilate to restore eroded parts of image
mask = cv2.erode(thresh1, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)

# Display the processed image
cv2.imshow('Processed Image', mask)

# Find all contours in frame
contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

# Find largest contour and display the centroid
if len(contours) > 0:
    # Find largest contour area and image moments
    c = max(contours, key=cv2.contourArea)
    M = cv2.moments(c)

    # Find x-axis centroid using image moments
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    # Display the centroid
    cv2.imshow('Centroid', frame)

cv2.waitKey(0)
cv2.destroyAllWindows()