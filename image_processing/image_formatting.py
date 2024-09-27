import cv2 as cv
import numpy as np

""" Color Space Conversion Functions """
def to_rgb(image):
    """ Converts an image to the RGB color space from CIE Lab"""
    rgb = cv.cvtColor(image, cv.COLOR_Lab2RGB)
    return rgb

def to_lab(image):
    """ Converts an image to the Lab color space from RGB"""
    lab = cv.cvtColor(image, cv.COLOR_RGB2Lab)
    return lab

def orient_array(array: np.array) -> np.array:
    """Orients input 2D or larger array to have it's height (1st axis) be longer than it's width (2nd axis)"""
    height, width = array.shape[:2]
    if height >= width:
        return np.swapaxes(array, 0, 1)
    return array

def img_rgb_array(image, is_BGR=False) -> tuple[np.array]:
    """Turns an OpenCV RGB or BGR image into 3 seperate Red, Green, and Blue arrays of all the same shape"""
    red = image[:,:,2] if is_BGR else image[:,:,0]
    green = image[:,:,1]
    blue = image[:,:,0] if is_BGR else image[:,:,2]
    return red, green, blue

def img_lab_array(image) -> tuple[np.array]:
    """Turns an OpenCV CIELAB image into 3 seperate L*, a*, and b* arrays of all the same shape"""
    light = image[:,:,0]
    a_coord = image[:,:,1]
    b_coord = image[:,:,2]
    return light, a_coord, b_coord