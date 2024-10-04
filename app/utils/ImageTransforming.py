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

def crop_img(img: np.array, x: int, y: int, w: int, h: int) -> np.array:
    """ Crops an image to a bounding box"""
    return img[y:y+h, x:x+w]


""" Functions for converting between DataFrames and images """
def reshape_df_to_img(df: pd.DataFrame, colourspace:str) -> np.array:
    """ Converts a Dataframe into a 1D colour image """
    df = df[['Blue', 'Green', 'Red'] if colourspace == 'BGR' else ['L', 'a', 'b']]
    return df.to_numpy().reshape((len(df), 1, 3)).astype(np.float32)

def scale_rgb_values(img: np.array) -> pd.DataFrame:
    """ Scales the RGB values of an image to between 0 and 1"""
    img *=1./255
    return img

def unscale_rgb_values(img: np.array) -> pd.DataFrame:
    """ Unscales the RGB values of an image to between 0 and 255"""
    img *= 255
    return np.round(img, 0)

def reshape_img_to_df(img: np.array, colourspace: str) -> pd.DataFrame:
    """
    Reshapes a 1D colour image into a Dataframe, with a column for each colour channel
    
    Parameters:
        img (np.array): an image
        colourspace (str): the colourspace of the image
    """
    img_array = img.reshape((len(img), 3))
    columns = ['Blue', 'Green', 'Red'] if colourspace == 'BGR' else ['L', 'a', 'b']
    return pd.DataFrame(img_array, columns=columns)

def core_to_rgb(df: pd.DataFrame) -> pd.DataFrame:
    """ Converts a DataFrame of a sediment core to RGB """
    img = reshape_df_to_img(df, colourspace='Lab')
    img = cv.cvtColor(img, cv.COLOR_Lab2BGR)
    img = unscale_rgb_values(img)
    img = reshape_img_to_df(img, colourspace='BGR')
    img['Depth (mm)'] = df['Depth (mm)']
    return img[['Depth (mm)', 'Blue', 'Green', 'Red']]

def core_to_lab(df: pd.DataFrame) -> pd.DataFrame:
    """ Converts a DataFrame of a sediment core to CIE Lab """
    img = reshape_df_to_img(df, colourspace='BGR')
    img = scale_rgb_values(img)
    img = cv.cvtColor(img, cv.COLOR_BGR2Lab)
    img = reshape_img_to_df(img, colourspace='Lab')
    img['Depth (mm)'] = df['Depth (mm)']
    return img[['Depth (mm)', 'L', 'a', 'b']]


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