"""
Functions for processing sediment cores in images as part of the Sediment Core 
Analysis project for CITS3200 at UWA.

Author: Sophie Mowe
Date: September 2024
"""
import os
import cv2 as cv
import numpy as np
import pandas as pd

import app.utils.ImageTransforming as transform

class Scaling():
    """ 
    Class for scaling the sediment core in an image to millimeters

    Attributes:
        core_width_in_mm (int): the width of the sediment core in millimeters
    """
    def __init__(self, core_width_in_mm: int):
        self.core_width_in_mm = core_width_in_mm
    
    def get_mm_scale(self, core_width_px: int) -> float:
        """ Returns the number of pixels per millimeter for the sediment core. """
        self.scale = self.core_width_in_mm / core_width_px
        return self.scale
    
    def get_core_length(self, core: list) -> float:
        """ 
        Returns the length of a sediment core in millimeters.

        Parameters:
            core (list): a list containing the x, y, width (px), and height (px) of the sediment core
        """
        _, _, w, h = core
        if w < h: # the sediment core is vertical
            self.get_mm_scale(w)
            length = h * self.scale
        else: # the sediment core is horizontal
            self.get_mm_scale(h)
            length = w * self.scale
        return length

class ExtractCore():
    """
    A class for extracting the largest sediment core in an image.

    Attributes:
        filepath (str): the file path of the image
        core_width_mm (int): the width of the sediment core in millimeters
        image (numpy.ndarray): the image as an array
        core (dict): the extracted sediment core
    """
    def __init__(self, image: np.array, core_width_mm: int):
        self.core_width_mm = core_width_mm
        self.image = image

    def find_cores(self) -> list:
        """
        Finds the sediment cores in an image. This function is
        specific to the images in the Sediment Core Analysis project.

        Returns:
            cores (list): a list of the sediment cores in the image
        """
        no_greys = transform.remove_greys(self.image) # colour segmentation
        contours = transform.get_contours(no_greys)

        # find contours that correspond to sediment cores
        cores = []
        for contour in contours:
            area = cv.contourArea(contour)
            if area > 100000: # the sediment cores are big!
                x, y, w, h = cv.boundingRect(contour)
                if w > h*2 or h > w*2: # the sediment cores are long and thin
                    cores.append([x, y, w, h])
        return cores    
    
    def get_largest_core(self, cores: list) -> list:
        """
        Returns the largest sediment core's x coordinate, y coordinate, width and height
        from an array of sediment cores. in an array of sediment cores.
        """
        largest_core = cores[0]
        for core in cores:
            _, _, w, h = core
            _, _, largest_w, largest_h = largest_core
            if w * h > largest_w * largest_h:
                largest_core = core
        return largest_core

    def get_bounding_box(self) -> list:
        """ Returns the bounding box of the largest sediment core in an image """
        bounding_boxes = self.find_cores()
        num_cores = len(bounding_boxes)
        if num_cores == 0:
            return 0
        elif num_cores == 1:
            bounding_box = bounding_boxes[0]
        else:
            bounding_box = self.get_largest_core(bounding_boxes)
        return bounding_box

    def extract_core(self, from_bounding_box=False, bounding_box=None) -> dict:
        """
        Extracts the largest sediment core in an image.
        
        Returns:
            core (dict): a dictionary containing the length of the sediment core in millimeters (`'Length'`), 
            the scale (`'Scale'`), the cropped image (`'Image'`) and the bounding box (`'Bounding Box'`) 
            of the sediment core
        """
        if from_bounding_box == False:
            bounding_box = self.get_bounding_box()
        if bounding_box == None or bounding_box == 0:
            return 0
        scaling = Scaling(self.core_width_mm)
        self.core = {
            "Length": scaling.get_core_length(bounding_box),
            "Scale" : scaling.scale,
            "Image": transform.orient_array(transform.crop_image(self.image, bounding_box)),
            "Bounding Box": bounding_box
        }
        return self.core

class Colours():
    """
    A class for determining the colour of each layer in a sediment core.
    
    Attributes:
        image (numpy.ndarray): the image of the sediment core
        height (int): the height of the sediment core in pixels
        width (int): the width of the sediment core in pixels
        colour (int): the number of colour channels in the image
        weights (numpy.ndarray): the weights for the weighted average of the colour channels
    """
    def __init__(self, image: np.array, scale: float):
        self.image = transform.orient_array(image)
        self.height, self.width, self.colour = self.image.shape
        self.weights = None
        self.scale = scale
    
    def get_weights(self):
        """ Returns the weights for the weighted average of the colour channels """
        if self.width % 2 == 0: # sediment core is even
            left_weights = np.arange(0, self.width/2)
            right_weights = np.flip(left_weights)
        else:
            left_weights = np.arange(0, self.width//2 + 1)
            right_weights = np.flip(left_weights[:-1])
        weights = np.concatenate((left_weights, right_weights))
        self.weights = weights
        return weights
    
    def get_weighted_avg_colour_channel(self, colour_values: np.array) -> np.array:
        """ Returns the rounded weighted average for a colour channel"""
        return np.round(np.average(colour_values, weights=self.weights), 0)
    
    def get_weighted_average_layer_colours(self, df: bool=True) -> np.array:
        """
        Returns the weighted average colours of each layer of a sediment core.
        
        Parameters:
            df (bool): whether to return the colours as a pandas DataFrame
            
        Returns:
            weighted_avgs (list): a list of the weighted average colours of each layer.
            If `df` is set to `True`, the function returns a pandas DataFrame.
        """
        self.get_weights()
        weighted_avgs = []
        for y in range(0, self.height):
            row = self.image[y, :]
            channel_avgs = []
            for c in range(0, self.colour):
                colour_values = row[:, c]
                weighted_avg = self.get_weighted_avg_colour_channel(colour_values)
                channel_avgs.append(weighted_avg)
            weighted_avgs.append(channel_avgs)
        
        scaled_depths = [y * self.scale for y in range(0, self.height)]
        if df == True:
            df = pd.DataFrame(weighted_avgs, columns=['Blue', 'Green', 'Red'])
            df['Depth (mm)'] = scaled_depths
            df = df[['Depth (mm)', 'Blue', 'Green', 'Red']]
            return df
        return np.array(weighted_avgs)


def process_core_image(image: np.array, core_width_mm: int, 
                       from_bounding_box: bool=False, bounding_box: list=None,
                       df: bool=True) -> dict:
    """ 
    Function for processing a sediment core image.

    Steps:
    1. Finds the largest sediment core in an image. 
        If `from_bounding_box` is `True`, the function 
        extracts the sediment core from the bounding box.
    2. Crops the image to the sediment core.
    3. Finds the length of the sediment core in millimeters.
    4. Rotates the sediment core so that it is vertical.
    5. Determines the colour of each layer in the sediment core.

    If a sediment core is not found, the function returns 0.
    Otherwise, returns a pandas `DataFrame` with the following:
    - `'Image'`: the cropped colour image of the sediment core
    - `'Length (mm)'`: the length of the sediment core in millimeters
    - `'Colours'`: the weighted average colours of each layer of the sediment core 
    (as a pandas `DataFrame` if the parameter `df` is set to `True`)
    - `'Scale'`: the number of pixels per millimeter
    - `'Bounding Box'`: the bounding box (`[x, y, width, height]`) of the sediment core in the image

    Parameters:
        image (numpy.ndarray): the image of the sediment core
        core_width_mm (int): the width of the sediment core in millimeters
        from_bounding_box (bool): whether to extract the sediment core from a bounding box
        bounding_box (list): the bounding box of the sediment core (if `from_bounding_box` is `True`)

    Returns:
        core (pd.DataFrame): a `DataFrame` containing the image, length, colours, 
            scale, and bounding box of the sediment core.
    """
    extract_core = ExtractCore(image, core_width_mm)

    core_data = extract_core.extract_core(from_bounding_box=from_bounding_box, bounding_box=bounding_box)
    if core_data == 0: return 0
    image = core_data['Image']
    scale = core_data['Scale']
    colours = Colours(image, scale).get_weighted_average_layer_colours(df=df)
    core = {
        "Image": image,
        "Length (mm)": core_data['Length'],
        "Colours": colours,
        "Scale": scale,
        "Bounding Box": core_data['Bounding Box']
    }
    return core

def show_bounding_box(image, bounding_box):
    """ Draws a bounding box around a sediment core in an image """
    x, y, w, h = bounding_box
    image_with_bb = image.copy()
    cv.rectangle(image_with_bb, (x, y), (x+w, y+h), (0, 255, 0), 10)
    return image_with_bb