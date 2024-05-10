from time import *
import RPi.GPIO as GPIO
import cv2
import picamera
from picamera.array import PiRGBArray
from smbus import SMBus

# Constants
HAT_ADDR = 20

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


# Function to initialize the I2C bus
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


def find_centroid(image_converted):
    contours, hierarchy = cv2.findContours(image_converted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        leftmost = tuple(largest_contour[largest_contour[:, :, 0].argmin()][0])
        rightmost = tuple(largest_contour[largest_contour[:, :, 0].argmax()][0])
        moments = cv2.moments(largest_contour)
        if moments['m00'] != 0:  # check if the area is not zero to avoid division by zero
            centroid_x = int(moments['m10'] / moments['m00'])
            return leftmost[0], rightmost[0], centroid_x
        return leftmost[0], rightmost[0], None
    return 0, 191, None


def followLine(car, speed):
    first_contour = True
    camera = picamera.PiCamera()
    camera.resolution = (192, 112)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(192, 112))
    sleep(0.1)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = crop_image(frame.array)
        key = cv2.waitKey(1) & 0xFF
        image = convert_image(image)
        # cv2.imshow("image", image)        # Uncomment this line to see the processed image
        leftmost, rightmost, centroid_x = find_centroid(image)
        if leftmost == 0 and rightmost == 191 and not first_contour:
            car.stop()
            break
        first_contour = False
        if centroid_x is not None:
            if centroid_x <= 80:
                car.turn_left(speed)
            if centroid_x >= 110:
                car.turn_right(speed)
            else:
                car.forward(speed)
        if key == ord("q"):
            car.stop()
            break
        rawCapture.truncate(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Initialize I2C bus
    bus = SMBus(1)
    sleep(1)
    initBus(bus)
    # Initialize motors
    left_front = Motor(45, 23, bus)
    left_back = Motor(40, 13, bus)
    right_front = Motor(44, 24, bus)
    right_back = Motor(41, 20, bus)
    # initialize car
    car = Car(left_front, left_back, right_front, right_back)
    followLine(car, SPEED_20)
    GPIO.cleanup()
