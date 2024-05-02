import cv2
import numpy as np
import picamera
import time

# Set up the camera
camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.framerate = camera.MAX_FRAMERATE

# Create a VideoWriter object to write the video frames


# Start the camera preview
camera.start_preview()

# Define the minimum and maximum values for the HSV color space for black
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 46])

while True:
    # Capture a frame from the camera
    camera.capture('frame.jpg')
    frame = cv2.imread('frame.jpg')
    frame_none = cv2.imread('frame.jpg')

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get a binary image of the black line
    mask = cv2.inRange(hsv, lower_black, upper_black)

    # Find contours in the thresholded frame
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    frame_BW = np.zeros_like(frame)
    # Draw the contours on the frame
    cv2.drawContours(frame_BW, contours, -1, (255, 255, 255), -1)
    cv2.drawContours(frame, contours, -1, (255, 255, 255), -1)

    # Write the frame to the video file

    # Show the frame
    cv2.imshow('Camera', frame_none)
    cv2.imshow('Camera + mask',frame)
    cv2.imshow('Frame B/W',frame_BW)

    # Break the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and the VideoWriter objects
camera.stop_preview()
camera.close()

# Close all OpenCV windows
cv2.destroyAllWindows()