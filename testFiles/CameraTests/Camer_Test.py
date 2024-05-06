import cv2

LEFT_TURN_IMAGE_PATH = 'test_Pictures/Lturn_image.jpg'
RIGHT_TURN_IMAGE_PATH = 'test_Pictures/Rturn_image.jpg'
STRAIGHT_IMAGE_PATH = 'test_Pictures/straight_line_image.jpg'
STOP_IMAGE_PATH = 'test_Pictures/stop_line_image.jpg'

OUT_PATH = 'test_Pictures/output/'


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


def find_centroid(image, color_image):
    # Find all contours in frame
    contours, hierarchy = cv2.findContours(image.copy(), 1, cv2.CHAIN_APPROX_NONE)
    # Find the largest contour and display the centroid
    if len(contours) > 0:
        # Find the largest contour area and image moments
        c = max(contours, key=cv2.contourArea)
        # display the largest contour
        cv2.drawContours(color_image, [c], -1, (0, 255, 0), 2)
        M = cv2.moments(c)
        # Find x-axis centroid using image moments
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(color_image, (cx, cy), 5, (0, 0, 255), -1)
        return color_image


if __name__ == '__main__':
    # read image file
    Lturn_image = cv2.imread(LEFT_TURN_IMAGE_PATH)
    Rturn_image = cv2.imread(RIGHT_TURN_IMAGE_PATH)
    straight_image = cv2.imread(STRAIGHT_IMAGE_PATH)
    stop_image = cv2.imread(STOP_IMAGE_PATH)
    # Display and save the original images
    cv2.imshow('Original Left Turn Image', Lturn_image)
    cv2.imshow('Original Right Turn Image', Rturn_image)
    cv2.imshow('Original Straight Image', straight_image)
    cv2.imshow('Original Stop Image', stop_image)
    cv2.imwrite(OUT_PATH + 'Original_Lturn_image.jpg', Lturn_image)
    cv2.imwrite(OUT_PATH + 'Original_Rturn_image.jpg', Rturn_image)
    cv2.imwrite(OUT_PATH + 'Original_straight_image.jpg', straight_image)
    cv2.imwrite(OUT_PATH + 'Original_stop_image.jpg', stop_image)
    # Resize the images
    Lturn_image_c = resize_image(Lturn_image)
    Rturn_image_c = resize_image(Rturn_image)
    straight_image_c = resize_image(straight_image)
    stop_image_c = resize_image(stop_image)
    # Display the resized images
    cv2.imshow('Resized Left Turn Image', Lturn_image_c)
    cv2.imshow('Resized Right Turn Image', Rturn_image_c)
    cv2.imshow('Resized Straight Image', straight_image_c)
    cv2.imshow('Resized Stop Image', stop_image_c)
    cv2.imwrite(OUT_PATH + 'Resized_Lturn_image.jpg', Lturn_image_c)
    cv2.imwrite(OUT_PATH + 'Resized_Rturn_image.jpg', Rturn_image_c)
    cv2.imwrite(OUT_PATH + 'Resized_straight_image.jpg', straight_image_c)
    cv2.imwrite(OUT_PATH + 'Resized_stop_image.jpg', stop_image_c)
    # Convert the images to use in the contour detection
    Lturn_image = convert_image(Lturn_image_c)
    Rturn_image = convert_image(Rturn_image_c)
    straight_image = convert_image(straight_image_c)
    stop_image = convert_image(stop_image_c)
    # Display the converted images
    cv2.imshow('Converted Left Turn Image', Lturn_image)
    cv2.imshow('Converted Right Turn Image', Rturn_image)
    cv2.imshow('Converted Straight Image', straight_image)
    cv2.imshow('Converted Stop Image', stop_image)
    cv2.imwrite(OUT_PATH + 'Converted_Lturn_image.jpg', Lturn_image)
    cv2.imwrite(OUT_PATH + 'Converted_Rturn_image.jpg', Rturn_image)
    cv2.imwrite(OUT_PATH + 'Converted_straight_image.jpg', straight_image)
    cv2.imwrite(OUT_PATH + 'Converted_stop_image.jpg', stop_image)
    # Find the centroid of the images
    Lturn_image = find_centroid(Lturn_image, Lturn_image_c)
    Rturn_image = find_centroid(Rturn_image, Rturn_image_c)
    straight_image = find_centroid(straight_image, straight_image_c)
    stop_image = find_centroid(stop_image, stop_image_c)
    # Display the images with the centroid
    cv2.imshow('Left Turn Image with Centroid', Lturn_image)
    cv2.imshow('Right Turn Image with Centroid', Rturn_image)
    cv2.imshow('Straight Image with Centroid', straight_image)
    cv2.imshow('Stop Image with Centroid', stop_image)
    cv2.imwrite(OUT_PATH + 'Centroid_Lturn_image.jpg', Lturn_image)
    cv2.imwrite(OUT_PATH + 'Centroid_Rturn_image.jpg', Rturn_image)
    cv2.imwrite(OUT_PATH + 'Centroid_straight_image.jpg', straight_image)
    cv2.imwrite(OUT_PATH + 'Centroid_stop_image.jpg', stop_image)
    # Wait for user to press a key
    cv2.waitKey(0)
    cv2.destroyAllWindows()
