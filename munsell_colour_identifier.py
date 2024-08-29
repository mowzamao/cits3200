
import numpy as np
import pandas as pd
from munsell_colour_mapping import get_munsell_dictionary

def find_closest_munsell_color(input_colour:list, input_type:str, munsell_dict:dict):
    """
    Find the closest Munsell Rock Color Code to the given RGB or LAB value.
    Achieved through iterating through the items of a dictionary mapping
    RGB and LAB data to Munsell Colour Code. 
    
    Parameters:
    input_color(list): A list of 3 values representing RGB or LAB color.
    input_type(str): A string, either "RGB" or "LAB", indicating the type of the input color.
    munsell_dict(dict): A dictionary containing Munsell color codes mapped to their RGB and LAB values.
    
    Returns:
    closest_colour_code(): The Munsell Rock Color Code that is closest to the input color.
    """
    closest_colour_code = None
    min_distance = None

    for munsell_code in munsell_dict.keys():
        colour_values = munsell_dict[munsell_code][input_type]
        distance = euclidean_distance_calc(input_colour, colour_values)
        closest_colour_code,min_distance = colour_similarity_check(distance,munsell_code,closest_colour_code,min_distance)

    return closest_colour_code

def euclidean_distance_calc(input_colour:list, colour_values:list):
    """Calculate the Euclidean distance between two color vectors."""
    return np.sqrt(np.sum((np.array(input_colour) - np.array(colour_values)) ** 2))

def colour_similarity_check(distance:float,munsell_code:str,closest_colour_code:str,min_distance:float):
    """
    Helper function which compares the euclidean distance of a colour to the current 
    closest colour in the iteration through the munsell dictionary. 
    """
    if closest_colour_code is None:
        min_distance = distance
        closest_colour_code = munsell_code

    elif distance < min_distance:
        min_distance = distance
        closest_colour_code = munsell_code

    return closest_colour_code,min_distance

munsell_dict = get_munsell_dictionary(['munsell_data/real_CIELAB.csv','munsell_data/real_sRGB.csv'],['l*','a*','b*','h','v','c','r','g','b'])
print(find_closest_munsell_color([1,60,90],'rgb',munsell_dict))