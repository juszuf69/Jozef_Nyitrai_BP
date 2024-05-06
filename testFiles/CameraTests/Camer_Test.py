import cv2

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
    # Find the largest contour and display the centroid
    if len(contours) > 0:
        # Find the largest contour area and image moments
        c = max(contours, key=cv2.contourArea)
        # display the largest contour
        cv2.drawContours(image_resized, [c], -1, (0, 255, 0), 2)
        M = cv2.moments(c)
        # Find x-axis centroid using image moments
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(image_resized, (cx, cy), 5, (0, 0, 255), -1)
        return image_resized


if __name__ == '__main__':
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
    cv2.waitKey(0)
    cv2.destroyAllWindows()
