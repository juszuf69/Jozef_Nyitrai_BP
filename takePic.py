import picamera
from time import sleep

def capture_and_save(filename):
    # Initialize the camera
    with picamera.PiCamera() as camera:
        # Set resolution to maximum supported by the camera
        camera.resolution = (640,480)

        # Capture a picture
        camera.capture(filename)

# Define the filename for the captured image
filename = 'stop_line_image.jpg'

# Call the function to capture and save the image
capture_and_save(filename)

print(f"Image captured and saved as '{filename}'.")

