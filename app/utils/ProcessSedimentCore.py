"""
Functions for processing sediment cores in images as part of the Sediment Core 
Analysis project for CITS3200 at UWA.

Author: Sophie Mowe
Date: September 2024
"""
import cv2 as cv
import numpy as np
import pandas as pd

from . import ImageTransforming as transform

class Scaling():
    """ 
    Class for scaling the sediment core in an image to millimeters

    Attributes:
        core_width_in_mm (int): the width of the sediment core in millimeters
    """
    def __init__(self, core_width_in_mm: int):
        """
        Constructor for the Scaling class.

        Parameters:
            core_width_in_mm (int): the width of the sediment core in millimeters
        """
        self.core_width_in_mm = core_width_in_mm
    
    def get_mm_scale(self, core_width: int) -> float:
        """ 
        Returns the number of pixels per millimeter for the sediment core.

        Parameters:
            core_width (int): the width of the sediment core in pixels
        """
        self.scale = self.core_width_in_mm / core_width
    
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
        img (numpy.ndarray): the image as an array
        core (dict): the extracted sediment core
    """
    def __init__(self, img: np.array, core_width_mm: int, show=False):
        """
        Constructor for the ExtractCore class.
        
        Parameters:
            filepath (str): the file path of the image
            core_width_mm (int): the width of the sediment core in millimeters
        """
        self.core_width_mm = core_width_mm
        self.img = img
        self.show = show

    def find_cores(self) -> list:
        """
        Finds the sediment cores in an image. This function is
        specific to the images in the Sediment Core Analysis project.

        Returns:
            cores (list): a list of the sediment cores in the image
        """
        no_greys = transform.remove_greys(self.img, show=False) # colour segmentation
        contours = transform.get_contours(no_greys, show=False)

        # find contours that correspond to sediment cores
        cores = []
        for contour in contours:
            area = cv.contourArea(contour)
            if area > 100000: # the sediment cores are big!
                x, y, w, h = cv.boundingRect(contour)
                if w > h*2 or h > w*2: # the sediment cores are long and thin
                    cores.append([x, y, w, h])
                    if self.show == True:
                        cv.rectangle(self.img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if self.show == True:
            transform.show_img(self.img, title='Sediment Cores')
        return cores    
    
    def get_largest_core(self, cores: list) -> list:
        """
        Returns the largest sediment core in an array of sediment cores.

        Parameters:
            cores (list): a list of sediment cores

        Returns:
            largest_core (list): the largest sediment core's x and y coordinates, width, and height
        """
        largest_core = cores[0]
        for core in cores:
            _, _, w, h = core
            _, _, largest_w, largest_h = largest_core
            if w * h > largest_w * largest_h:
                largest_core = core
        return largest_core

    def extract_core(self) -> dict:
        """
        Extracts the largest sediment core in an image.
        
        Returns:
            core (dict): a dictionary containing the length of the sediment core in millimeters
            and the cropped image of the sediment core
        """
        cores = self.find_cores()

        num_cores = len(cores)
        if num_cores == 0: return 0
        elif num_cores == 1: core = cores[0]
        else: core = self.get_largest_core(cores)
        
        x, y, width, height = core
        scaling = Scaling(self.core_width_mm)
        self.core = {
            "Length": scaling.get_core_length(core),
            "Scale" : scaling.scale,
            "Image": transform.orient_array(transform.crop_img(self.img, x, y, width, height))
        }
        return self.core

class Colours():
    """
    A class for determining the colour of each layer in a sediment core.
    
    Attributes:
        img (numpy.ndarray): the image of the sediment core
        height (int): the height of the sediment core in pixels
        width (int): the width of the sediment core in pixels
        colour (int): the number of colour channels in the image
        weights (numpy.ndarray): the weights for the weighted average of the colour channels
    """
    def __init__(self, img: np.array, scale: float):
        """
        Constructor for the Colours class.
        
        Parameters:
            img (numpy.ndarray): the image of the sediment core
        """
        self.img = transform.orient_array(img)
        self.height, self.width, self.colour = self.img.shape
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
            row = self.img[y, :]
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


def process_core_image(img: np.array, core_width_mm: int, df: bool=True, show: bool=False) -> dict:
    """ 
    Function for processing a sediment core image.

    Steps:
    1. Finds the largest sediment core in an image.
    2. Crops the image to the sediment core.
    3. Finds the length of the sediment core in millimeters.
    4. Rotates the sediment core so that it is vertical.
    5. Determines the colour of each layer in the sediment core.

    If a sediment core is not found, the function returns 0.
    Otherwise, returns a dictionary with the following:
    - Image: the cropped colour image of the sediment core
    - Length: the length of the sediment core in millimeters
    - Colours: the weighted average colours of each layer of the sediment core 
    (as a pandas `DataFrame` if the parameter `df` is set to `True`)

    Parameters:
        filepath (str): the file path of the image
        core_width_mm (int): the width of the sediment core in millimeters
        df (bool): whether to return the colours as a pandas DataFrame
    
    Returns:
        core (dict): a dictionary containing the image, length, and colours of the sediment core
    """
    core_data = ExtractCore(img, core_width_mm, show).extract_core()
    if core_data == 0: return 0
    image = core_data['Image']
    length = core_data['Length']
    scale = core_data['Scale']
    colours = Colours(image, scale).get_weighted_average_layer_colours(df=df)
    core = {
        "Image": image,
        "Length (mm)": length,
        "Colours": colours
    }
    return core

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
    
    Returns:
        df (pd.DataFrame): a DataFrame of the image
    """
    img_array = img.reshape((len(img), 3))
    columns = ['Blue', 'Green', 'Red'] if colourspace == 'BGR' else ['L', 'a', 'b']
    return pd.DataFrame(img_array, columns=columns)

def core_to_rgb(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Converts a DataFrame of a sediment core to RGB
    
    Parameters:
        df (pd.DataFrame): a DataFrame of a sediment core
        
    Returns:
        img (pd.DataFrame): a DataFrame of the sediment core in RGB
    """
    img = reshape_df_to_img(df, colourspace='Lab')
    img = cv.cvtColor(img, cv.COLOR_Lab2BGR)
    img = unscale_rgb_values(img)
    img = reshape_img_to_df(img, colourspace='BGR')
    img['Depth (mm)'] = df['Depth (mm)']
    return img[['Depth (mm)', 'Blue', 'Green', 'Red']]

def core_to_lab(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Converts a DataFrame of a sediment core to CIE Lab 
    
    Parameters:
        df (pd.DataFrame): a DataFrame of a sediment core
        
    Returns:
        img (pd.DataFrame): a DataFrame of the sediment core in CIE Lab
    """
    img = reshape_df_to_img(df, colourspace='BGR')
    img = scale_rgb_values(img)
    img = cv.cvtColor(img, cv.COLOR_BGR2Lab)
    img = reshape_img_to_df(img, colourspace='Lab')
    img['Depth (mm)'] = df['Depth (mm)']
    return img[['Depth (mm)', 'L', 'a', 'b']]

""" tests """
def test_core_colour_conversion():
    """ Test function for the core_to_rgb and core_to_lab functions """
    df = pd.DataFrame({
        'Depth (mm)': [0, 1, 2, 3],
        'Blue': [0, 0, 255, 255],
        'Green': [0, 255, 0, 255],
        'Red': [255, 0, 0, 255]
    })
    lab = core_to_lab(df)
    rgb = core_to_rgb(lab)
    assert np.allclose(df, rgb), 'Core Colour Conversion Test failed!'
    print('Core Colour Conversion Test passed!')

if __name__ == '__main__':
    # Testing
    core_width_mm = 76 # sediment core width in millimeters
    file_path = 'app/utils/image-data/MI-24_03/SCREEN banner 96dpi-3192-2.jpg' # for testing purposes
    img = transform.import_img(file_path)
    core = process_core_image(img, core_width_mm, df=True)
    transform.show_img(core['Image'], title='Extracted Sediment Core')

    # Testing core colour conversion functions
    test_core_colour_conversion()