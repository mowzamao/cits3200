import cv2 as cv
import numpy as np

def img_rgb_array(image, is_BGR=False):
    """Turns an OpenCV RGB or BGR image into 3 seperate Red, Green, and Blue arrays of all the same length"""
    red = image[:,:,2] if is_BGR else image[:,:,0]
    green = image[:,:,1]
    blue = image[:,:,0] if is_BGR else image[:,:,2]
    return red, green, blue

def img_lab_array(image):
    """Turns an OpenCV CIELAB image into 3 seperate L*, a*, and b* arrays of all the same length"""
    light = image[:,:,0]
    a_coord = image[:,:,1]
    b_coord = image[:,:,2]
    return light, a_coord, b_coord