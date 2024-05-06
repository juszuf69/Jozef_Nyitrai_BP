from time import *
import cv2
import picamera
from picamera.array import PiRGBArray

IMAGE_PATH = 'test_Pictures/Lturn_image.jpg'


def resize_image(image):
    # Resize the image
    height, width = image.shape[:2]
    roi_start = height // 4
    roi_end = 3 * height // 4
    image = image[roi_start:roi_end, :]
    return image


def convert_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh1 = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)
    return thresh1


def find_centroid(image_converted, image_resized):
    # Find all contours in frame
    contours, hierarchy = cv2.findContours(image_converted.copy(), 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        # Find the largest contour area and image moments
        c = max(contours, key=cv2.contourArea)
        # display the largest contour
        cv2.drawContours(image_resized, [c], -1, (0, 255, 0), 2)
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(image_resized, (cx, cy), 5, (0, 0, 255), -1)
        return image_resized


def T1():
    # read image file
    image_original = cv2.imread(IMAGE_PATH)
    # Display and save the original images
    cv2.imshow('Original Left Turn Image', image_original)
    # Resize the images
    image_resized = resize_image(image_original)
    # Display the resized images
    cv2.imshow('Resized Left Turn Image', image_resized)
    # Convert the images to use in the contour detection
    image_converted = convert_image(image_resized)
    # Display the converted images
    cv2.imshow('Converted Left Turn Image', image_converted)
    # Find the centroid of the images
    image_centroid = find_centroid(image_converted, image_resized)
    # Display the images with the centroid
    cv2.imshow('Left Turn Image with Centroid', image_centroid)
    # Wait for user to press a key


def T2():
    camera = picamera.PiCamera()
    camera.resolution = (192, 112)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(192, 112))
    sleep(0.1)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = resize_image(frame.array)
        # Display camera input
        cv2.imshow('Input Original', image)
        # Create key to break for loop
        key = cv2.waitKey(1) & 0xFF
        # convert the image
        image_converted = convert_image(image)
        cv2.imshow('Output Converted', image_converted)
        # Find all contours in frame
        image_centroid = find_centroid(image_converted, image)
        cv2.imshow('Output with Centroid', image_centroid)
        rawCapture.truncate(0)
        if key == ord("q"):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    T1()
    cv2.waitKey(0)
    T2()
    cv2.destroyAllWindows()
