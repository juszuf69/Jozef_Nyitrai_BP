import cv2
import numpy as np

def get_left_right_points(contour):
    # Initialize leftmost and rightmost points with extreme values
    leftmost = tuple(contour[0][0])
    rightmost = tuple(contour[0][0])
    
    # Iterate through all points in the contour to find leftmost and rightmost
    for point in contour:
        point = tuple(point[0])  # Convert to tuple for easier comparison
        
        # Update leftmost point if current point is more left
        if point[0] < leftmost[0]:
            leftmost = point
        
        # Update rightmost point if current point is more right
        if point[0] > rightmost[0]:
            rightmost = point
    
    return leftmost, rightmost

def draw_vertical_lines(image, spacing):
    height, width = image.shape[:2]
    for x in range(spacing, width, spacing):
        cv2.line(image, (x, 0), (x, height), (0, 0, 255), 1)

# Load the image
image = cv2.imread('straight_line_image_out.jpg', cv2.IMREAD_GRAYSCALE)
imageR = cv2.imread('Rturn_image_out.jpg', cv2.IMREAD_GRAYSCALE)
imageL = cv2.imread('Lturn_image_out.jpg', cv2.IMREAD_GRAYSCALE)
image = cv2.resize(image,(640,480))
imageR = cv2.resize(imageR,(640,480))
imageL = cv2.resize(imageL,(640,480))


height, width = image.shape[:2]
roi_start = height // 4
roi_end = 3 * height // 4
roi = image[roi_start:roi_end, :]
roiR = imageR[roi_start:roi_end, :]
roiL = imageL[roi_start:roi_end, :]

# Preprocessing
_, thresh = cv2.threshold(roi, 127, 255, cv2.THRESH_BINARY)
_, threshR = cv2.threshold(roiR, 127, 255, cv2.THRESH_BINARY)
_, threshL = cv2.threshold(roiL, 127, 255, cv2.THRESH_BINARY)


# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contoursR, _ = cv2.findContours(threshR, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contoursL, _ = cv2.findContours(threshL, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



# Get the largest contour
if contours and contoursR and contoursL:
    largest_contour = max(contours, key=cv2.contourArea)
    largest_contourR = max(contoursR, key=cv2.contourArea)
    largest_contourL = max(contoursL, key=cv2.contourArea)
    print("##### STRAIGHT #####")
    print(get_left_right_points(largest_contour))
    left_most_p , right_most_p = get_left_right_points(largest_contour)
    
    # Example decision making based on angle
    if left_most_p[0] < 200:
        print("Turn left")
    elif right_most_p[0] > 440:
        print("Turn right")
    else:
        print("Go straight")
    
    print("\n##### RIGHT #####")
    print(get_left_right_points(largest_contourR))
    left_most_p , right_most_p = get_left_right_points(largest_contourR)
    
    # Example decision making based on angle
    if left_most_p[0] < 200:
        print("Turn left")
    elif right_most_p[0] > 440:
        print("Turn right")
    else:
        print("Go straight")
    
    print("\n##### LEFT #####")
    print(get_left_right_points(largest_contourL))
    left_most_p , right_most_p = get_left_right_points(largest_contourL)
    
    # Example decision making based on angle
    if left_most_p[0] < 200:
        print("Turn left")
    elif right_most_p[0] > 440:
        print("Turn right")
    else:
        print("Go straight")
    
    

image_with_contours = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
image_with_contours = image_with_contours[roi_start:roi_end, :]
cv2.drawContours(image_with_contours, [largest_contour], -1, (0, 255, 0), 2)

image_with_contoursR = cv2.cvtColor(imageR, cv2.COLOR_GRAY2BGR)
image_with_contoursR = image_with_contoursR[roi_start:roi_end, :]
cv2.drawContours(image_with_contoursR, [largest_contourR], -1, (0, 255, 0), 2)

image_with_contoursL = cv2.cvtColor(imageL, cv2.COLOR_GRAY2BGR)
image_with_contoursL = image_with_contoursL[roi_start:roi_end, :]
cv2.drawContours(image_with_contoursL, [largest_contourL], -1, (0, 255, 0), 2)

draw_vertical_lines(image_with_contours,40)
draw_vertical_lines(image_with_contoursR,40)
draw_vertical_lines(image_with_contoursL,40)

# Display the image with contours
cv2.imshow('STRAIGHT', image_with_contours)
cv2.imshow('RIGHT', image_with_contoursR)
cv2.imshow('LEFT', image_with_contoursL)
cv2.imwrite('left_final_img.jpg',image_with_contoursL)
cv2.imwrite('right_final_img.jpg',image_with_contoursR)
cv2.imwrite('straight_final_img.jpg',image_with_contours)
cv2.waitKey(0)
cv2.destroyAllWindows()


