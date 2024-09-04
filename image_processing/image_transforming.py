import cv2
import numpy as np
import argparse

def import_img(image_path):
    """ Imports an image from a file path"""
    image = cv2.imread(image_path)
    assert image is not None, "No image found at the specified path"
    return image

def get_sediment_cores(image):
    # remove grey and white areas of the image
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_grey = np.array([0, 0, 50])
    upper_grey = np.array([180, 50, 200])
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 20, 255])
    mask_grey = cv2.inRange(hsv, lower_grey, upper_grey)
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_combined = cv2.bitwise_or(mask_grey, mask_white)
    mask_non_grey_white = cv2.bitwise_not(mask_combined)
    image_no_grey_white = cv2.bitwise_and(image, image, mask=mask_non_grey_white)

    # find contours
    gray = cv2.cvtColor(image_no_grey_white, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (101, 101), 0)
    _, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # find contours that correspond to sediment cores
    sediment_cores = []
    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > 100000:  
            x, y, w, h = cv2.boundingRect(contour)
            if w > h*2 or h > w*2:
                # Draw the bounding box on the original image
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, 'Sediment Core Detected', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                sediment_cores.append([x, y, w, h])

    print(f"Number of sediment cores detected: {len(sediment_cores)}")
    print(sediment_cores)

    cv2.imshow('Sediment Core Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return sediment_cores

image = import_img('image_processing\image-data\MI-24_03\SCREEN banner 96dpi-3148-2.jpg')
# sediment_cores = get_sediment_cores(image)

def select_cm(image):
    def shape_selection(event, x, y, flags, param): 
        # grab references to the global variables 
        global ref_point, crop 
    
        # if the left mouse button was clicked, record the starting 
        # (x, y) coordinates and indicate that cropping is being performed 
        if event == cv2.EVENT_LBUTTONDOWN: 
            ref_point = [(x, y)] 
    
        # check to see if the left mouse button was released 
        elif event == cv2.EVENT_LBUTTONUP: 
            # record the ending (x, y) coordinates and indicate that 
            # the cropping operation is finished 
            ref_point.append((x, y)) 
    
            # draw a rectangle around the region of interest 
            cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2) 
            cv2.imshow("image", image) 
    
    # load the image, clone it, and setup the mouse callback function 
    clone = image.copy() 
    cv2.namedWindow("image") 
    cv2.setMouseCallback("image", shape_selection) 
    
    
    # keep looping until the 'q' key is pressed 
    while True: 
        # display the image and wait for a keypress 
        cv2.imshow("image", image) 
        key = cv2.waitKey(1) & 0xFF
    
        # press 'r' to reset the window 
        if key == ord("r"): 
            image = clone.copy() 
    
        # if the 'c' key is pressed, break from the loop 
        elif key == ord("c"): 
            break
    
    if len(ref_point) == 2: 
        crop_img = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]: 
                                                            ref_point[1][0]] 
        cv2.imshow("crop_img", crop_img) 
        cv2.waitKey(0) 

select_cm(image)