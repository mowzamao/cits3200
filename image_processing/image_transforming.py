import cv2 as cv
import numpy as np

def import_img(image_path):
    """ Imports an image from a file path"""
    image = cv.imread(image_path)
    assert image is not None, "No image found at the specified path"
    return image

def crop_core(segmented_core, core_contour):
    x, y, w, h = cv.boundingRect(core_contour)
    cropped_core = core[y:y+h, x:x+w]
    return cropped_core

def detect_core(image_path):
    """ Detects the sediment core in an image"""
    image = import_img(image_path)

    # image thresholding (convert to binary image)
    grey_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, binary_image = cv.threshold(grey_image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # closing (closes small holes in foreground object)
    kernel = np.ones((5, 5), np.uint8)
    cleaned_image = cv.morphologyEx(binary_image, cv.MORPH_CLOSE, kernel)

    # find image contours (the shape of the core)
    contours, _ = cv.findContours(cleaned_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    core_contour = max(contours, key=cv.contourArea)

    # create a mask and extract the core
    mask = np.zeros_like(grey_image)
    cv.drawContours(mask, [core_contour], -1, 255, thickness=cv.FILLED)
    segmented_core = cv.bitwise_and(image, mask)
    
    # crop the image to just the core
    segmented_core = crop_core(segmented_core, core_contour)
    return segmented_core

""" Color Space Conversion Functions """
def to_rgb(image):
    """ Converts an image to the RGB color space from CIE Lab"""
    rgb = cv.cvtColor(image, cv.COLOR_Lab2RGB)
    return rgb

def to_lab(image):
    """ Converts an image to the Lab color space from RGB"""
    lab = cv.cvtColor(image, cv.COLOR_RGB2Lab)
    return lab

