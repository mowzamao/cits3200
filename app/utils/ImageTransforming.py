"""
This module contains functions for importing, displaying, and processing images,
as part of the Sediment Core Analysis project for CITS3200.

Authors: Sophie Mowe, Blair Smith
Date: September 2024
"""
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

""" img importing and displaying functions """
def import_img(img_path: str) -> np.array:
    """ Imports an image from a file path"""
    img = cv.imread(img_path)
    assert img is not None, "No image found at the specified path"
    return img

def show_img(img: np.array, title: str='Image') -> None:
    """ Displays an image"""
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.title(title)
    plt.show()

""" img Processing Functions """
def remove_greys(img: np.array, show: bool=False) -> np.array:
    """ Removes grey and white areas of an image"""
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower_grey = np.array([0, 0, 50])
    upper_grey = np.array([180, 50, 200])
    mask_grey = cv.inRange(hsv, lower_grey, upper_grey)

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 20, 255])
    mask_white = cv.inRange(hsv, lower_white, upper_white)

    mask_combined = cv.bitwise_or(mask_grey, mask_white)
    mask_non_grey_white = cv.bitwise_not(mask_combined)
    img_no_grey_white = cv.bitwise_and(img, img, mask=mask_non_grey_white)
    if show == True:
        show_img(img_no_grey_white, title='Image with Greys and Whites Removed')
    return img_no_grey_white

def get_contours(img: np.array, show: bool=False) -> list:
    """ Processes and finds contours in an image"""
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(grey, (101, 101), 0)
    _, binary = cv.threshold(blurred, 127, 255, cv.THRESH_OTSU)
    contours, _ = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    if show == True:
        cv.drawContours(img, contours, -1, (0, 255, 0), 3)
        show_img(img, title='Contours')
    return contours

""" Color Space Conversion Functions """
def crop_img(img: np.array, x: int, y: int, w: int, h: int) -> np.array:
    """ Crops an image to a bounding box"""
    return img[y:y+h, x:x+w]

def to_rgb(img: np.array) -> np.array:
    """ Converts an image to the RGB color space from CIE Lab"""
    rgb = cv.cvtColor(img, cv.COLOR_Lab2RGB)
    return rgb

def to_lab(img: np.array) -> np.array:
    """ Converts an image to the Lab color space from RGB"""
    lab = cv.cvtColor(img, cv.COLOR_RGB2Lab)
    return lab

def img_rgb_array(img: np.array, is_BGR: bool=False) -> tuple[np.array]:
    """Turns an OpenCV RGB or BGR image into 3 seperate Red, Green, and Blue arrays of all the same shape"""
    red = img[:,:,2] if is_BGR else img[:,:,0]
    green = img[:,:,1]
    blue = img[:,:,0] if is_BGR else img[:,:,2]
    return red, green, blue

def img_lab_array(img: np.array) -> tuple[np.array]:
    """Turns an OpenCV CIELAB image into 3 seperate L*, a*, and b* arrays of all the same shape"""
    light = img[:,:,0]
    a_coord = img[:,:,1]
    b_coord = img[:,:,2]
    return light, a_coord, b_coord

""" Other Fucntions """
def orient_array(array: np.array) -> np.array:
    """Orients input 2D or larger array to have it's height (1st axis) be longer than it's width (2nd axis)
    Sediment core should be vertical, not horizontal.
    """
    height, width = array.shape[:2]
    if height < width:
        return np.swapaxes(array, 0, 1)
    return array

