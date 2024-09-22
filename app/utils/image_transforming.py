import cv2
import numpy as np

def import_img(image_path):
    """ Imports an image from a file path"""
    image = cv2.imread(image_path)
    assert image is not None, "No image found at the specified path"
    return image

def show_img(image, title='Image'):
    """ Displays an image"""
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def remove_greys(image, show=False):
    """ Removes grey and white areas of an image"""
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
    if show == True:
        show_img(image_no_grey_white, title='Image with Greys and Whites Removed')
    return image_no_grey_white

def get_contours(image, show=False):
    """ Processes and finds contours in an image"""
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    show_img(grey, title='Grey Image')
    blurred = cv2.GaussianBlur(grey, (101, 101), 0)
    show_img(blurred, title='Blurred Image')
    _, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_OTSU)
    show_img(binary, title='Binary Image')
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if show == True:
        cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        show_img(image, title='Contours')
    return contours

def get_sediment_cores(filepath, show=True, print_results=False):
    """
    Basic function to detect coloured sediment cores in an image. Very
    specific to the images we have been provided: for instance, removes white
    and grey areas of the image to make processing easier.
    
    Params
    ------
        filepath (str): path to the image file
        show (bool): whether to display the image with bounding boxes around the sediment cores
        print_results (bool): whether to print the locations of the sediment cores

    Returns
    -------
        array of arrays of the form [x, y, w, h] where x, y are the coordinates of the 
        top left corner of the bounding box
    """
    image = import_img(filepath)
    no_greys = remove_greys(image, show=True)
    contours = get_contours(no_greys, show=True)

    # find contours that correspond to sediment cores
    sediment_cores = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100000: # the sediment cores are big!
            x, y, w, h = cv2.boundingRect(contour)
            if w > h*2 or h > w*2:
                # Draw the bounding box on the original image
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, 'Sediment Core Detected', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                sediment_cores.append([x, y, w, h])

    if print_results == True:
        print(f"Number of sediment cores detected: {len(sediment_cores)}")
        print(sediment_cores)

    if show == True:
        show_img(image, title='Sediment Core Detection')
    return sediment_cores

sediment_cores = get_sediment_cores('image_processing\image-data\MI-24_03\SCREEN banner 96dpi-3148-2.jpg', print_results=True)

# def select_cm(image):
"""" Selects a region of interest in an image: Use for cropping the image to a cm? """
#     def shape_selection(event, x, y, flags, param): 
#         # grab references to the global variables 
#         global ref_point, crop 
    
#         # if the left mouse button was clicked, record the starting 
#         # (x, y) coordinates and indicate that cropping is being performed 
#         if event == cv2.EVENT_LBUTTONDOWN: 
#             ref_point = [(x, y)] 
    
#         # check to see if the left mouse button was released 
#         elif event == cv2.EVENT_LBUTTONUP: 
#             # record the ending (x, y) coordinates and indicate that 
#             # the cropping operation is finished 
#             ref_point.append((x, y)) 
    
#             # draw a rectangle around the region of interest 
#             cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2) 
#             cv2.imshow("image", image) 
    
#     # load the image, clone it, and setup the mouse callback function 
#     clone = image.copy() 
#     cv2.namedWindow("image") 
#     cv2.setMouseCallback("image", shape_selection) 
    
    
#     # keep looping until the 'q' key is pressed 
#     while True: 
#         # display the image and wait for a keypress 
#         cv2.imshow("image", image) 
#         key = cv2.waitKey(1) & 0xFF
    
#         # press 'r' to reset the window 
#         if key == ord("r"): 
#             image = clone.copy() 
    
#         # if the 'c' key is pressed, break from the loop 
#         elif key == ord("c"): 
#             break
    
#     if len(ref_point) == 2: 
#         crop_img = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]: 
#                                                             ref_point[1][0]] 
#         cv2.imshow("crop_img", crop_img) 
#         cv2.waitKey(0) 

# select_cm(image)