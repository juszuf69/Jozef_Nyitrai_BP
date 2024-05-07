from time import *
import cv2
import picamera
from picamera.array import PiRGBArray

IMAGE_PATH = 'test_Pictures/Lturn_image.jpg'


def crop_image(image):
    height = image.shape[0]
    roi_start = height // 4
    roi_end = 3 * height // 4
    image = image[roi_start:roi_end, :]
    return image


def convert_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, image_converted = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV)
    return image_converted


def find_centroid(image_converted, image_resized):
    # Find all contours in frame
    contours, hierarchy = cv2.findContours(image_converted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        # Find the largest contour area and image moments
        largest_contour = max(contours, key=cv2.contourArea)
        # display the largest contour on the color image
        cv2.drawContours(image_resized, [largest_contour], -1, (0, 255, 0), 3)
        moments = cv2.moments(largest_contour)
        if moments['m00'] != 0:  # check if the area is not zero to avoid division by zero
            centroid_x = int(moments['m10'] / moments['m00'])
            centroid_y = int(moments['m01'] / moments['m00'])
            cv2.circle(image_resized, (centroid_x, centroid_y), 5, (0, 0, 255), 3)
        return image_resized


def T1():
    # read image file
    image_original = cv2.imread(IMAGE_PATH)
    # Display the original images
    cv2.imshow('Original Image', image_original)
    # Crop the image
    image_cropped = crop_image(image_original)
    # Display the resized image
    cv2.imshow('Cropped Image', image_cropped)
    # Convert the image to use in the contour detection
    image_converted = convert_image(image_cropped)
    # Display the converted image
    cv2.imshow('Converted Image', image_converted)
    # Find the centroid of the image
    image_centroid = find_centroid(image_converted, image_cropped)
    # Display the image with the centroid
    if image_centroid is not None:
        cv2.imshow('Image with Centroid', image_centroid)


def T2():
    camera = picamera.PiCamera()
    camera.resolution = (192, 112)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(192, 112))
    sleep(0.1)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = crop_image(frame.array)
        # Display camera input
        cv2.imshow('Input Original', image)
        # Create key to break for loop
        key = cv2.waitKey(1) & 0xFF
        # convert the image
        image_converted = convert_image(image)
        cv2.imshow('Output Converted', image_converted)
        # Find all contours in frame
        image_centroid = find_centroid(image_converted, image)
        if image_centroid is not None:
            cv2.imshow('Output with Centroid', image_centroid)
        rawCapture.truncate(0)
        if key == ord("q"):
            break


if __name__ == '__main__':
    T1()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    T2()
    cv2.destroyAllWindows()
