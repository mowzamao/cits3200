"""
This module contains functions for importing, displaying, and processing images,
as part of the Sediment Core Analysis project for CITS3200.

Authors: Sophie Mowe, Blair Smith
Date: September 2024
"""
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

""" Image importing and displaying functions """
def import_image(image_path: str) -> np.array:
    """ Imports an image from a file path"""
    image = cv.imread(image_path)
    assert image is not None, "No image found at the specified path"
    return image

def show_image(image: np.array, title: str='Image') -> None:
    """ Displays an image"""
    plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    plt.title(title)
    plt.show()


""" Image Processing Functions """
def remove_greys(image: np.array, show: bool=False) -> np.array:
    """ Removes grey and white areas of an image"""
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    lower_grey = np.array([0, 0, 50])
    upper_grey = np.array([180, 50, 200])
    mask_grey = cv.inRange(hsv, lower_grey, upper_grey)

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 20, 255])
    mask_white = cv.inRange(hsv, lower_white, upper_white)

    mask_combined = cv.bitwise_or(mask_grey, mask_white)
    mask_non_grey_white = cv.bitwise_not(mask_combined)
    image_no_grey_white = cv.bitwise_and(image, image, mask=mask_non_grey_white)
    if show == True:
        show_image(image_no_grey_white, title='Image with Greys and Whites Removed')
    return image_no_grey_white

def get_contours(image: np.array, show: bool=False) -> list:
    """ Processes and finds contours in an image"""
    grey = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(grey, (101, 101), 0)
    _, binary = cv.threshold(blurred, 127, 255, cv.THRESH_OTSU)
    contours, _ = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    if show == True:
        cv.drawContours(image, contours, -1, (0, 255, 0), 3)
        show_image(image, title='Contours')
    return contours

def crop_image(image: np.array, bounding_box: list=None) -> np.array:
    """ Crops an image to a bounding box"""
    if bounding_box is None:
        return image
    
    x, y, w, h = bounding_box
    return image[y:y+h, x:x+w]


""" Functions for converting between DataFrames and images """
def reshape_df_to_image(df: pd.DataFrame, colourspace:str) -> np.array:
    """ Converts a Dataframe into a 1D colour image """
    df = df[['Blue', 'Green', 'Red'] if colourspace == 'BGR' else ['L', 'a', 'b']]
    return df.to_numpy().reshape((len(df), 1, 3)).astype(np.float32)

def scale_rgb_values(image: np.array) -> pd.DataFrame:
    """ Scales the RGB values of an image to between 0 and 1"""
    image *=1./255
    return image

def unscale_rgb_values(image: np.array) -> pd.DataFrame:
    """ Unscales the RGB values of an image to between 0 and 255"""
    image *= 255
    return np.round(image, 0)

def reshape_image_to_df(image: np.array, colourspace: str) -> pd.DataFrame:
    """
    Reshapes a 1D colour image into a Dataframe, with a column for each colour channel
    
    Parameters:
        image (np.array): an image
        colourspace (str): the colourspace of the image
    """
    image_array = image.reshape((len(image), 3))
    columns = ['Blue', 'Green', 'Red'] if colourspace == 'BGR' else ['L', 'a', 'b']
    return pd.DataFrame(image_array, columns=columns)

def core_to_rgb(df: pd.DataFrame) -> pd.DataFrame:
    """ Converts a DataFrame of a sediment core to RGB """
    image = reshape_df_to_image(df, colourspace='Lab')
    image = cv.cvtColor(image, cv.COLOR_Lab2BGR)
    image = unscale_rgb_values(image)
    image = reshape_image_to_df(image, colourspace='BGR')
    image['Depth (mm)'] = df['Depth (mm)']
    return image[['Depth (mm)', 'Blue', 'Green', 'Red']]

def core_to_lab(df: pd.DataFrame) -> pd.DataFrame:
    """ Converts a DataFrame of a sediment core to CIE Lab """
    image = reshape_df_to_image(df, colourspace='BGR')
    image = scale_rgb_values(image)
    image = cv.cvtColor(image, cv.COLOR_BGR2Lab)
    image = reshape_image_to_df(image, colourspace='Lab')
    image['Depth (mm)'] = df['Depth (mm)']
    return image[['Depth (mm)', 'L', 'a', 'b']]


""" Functions for flipping images """
def swap_df_cols(data, new_col, old_col):
    """ Swaps two columns in a dataframe"""
    data[new_col], data[old_col] = data[old_col], data[new_col]
    data = data.sort_values(by=old_col)
    data.reset_index(drop=True, inplace=True)
    return data

def flip (data: pd.DataFrame) -> pd.DataFrame:
    """ Flips a core dataframe"""
    if 'Flipped Depth (mm)' not in data.columns:
        data['Flipped Depth (mm)'] = data['Depth (mm)'].max() - data['Depth (mm)']
    data = swap_df_cols(data, 'Flipped Depth (mm)', 'Depth (mm)')
    return data


""" Other Fucntions """
def orient_array(array: np.array) -> np.array:
    """Orients input 2D or larger array to have it's height (1st axis) be longer than it's width (2nd axis)
    Sediment core should be vertical, not horizontal.
    """
    height, width = array.shape[:2]
    if height < width:
        return np.swapaxes(array, 0, 1)
    return array