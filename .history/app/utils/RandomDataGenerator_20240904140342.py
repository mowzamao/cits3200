from random import random, choice

class RandomDataGenerator():
    """Creates random RGB data for use in testing the GUI graph"""

    def __init__(self):
        self.core_bounds   = {'min':1, 'max':2}        # The length of random cores in metres
        self.layer_bounds  = {'min':0.01, 'max':0.05}  # The depth of a given layer  in metres
    
        self.noise      = {'mean':0, 'sd':2}
        self.rgb_range  = {'min':0, 'max':255}

        self.granularity = 0.01 # The distance between measurements in a generated core

        # The bases colours for randomly sampling
        self.colours = [(234,208,168), (182,159,102), (107,84,40), (118,85,43), (255,77,179), (64,41,5)]
       
    
    def get_random_dataset(self):

        core_ruler  = 0 # Outer ruler holds distance from start of the core
        layer_ruler = 0 # Inner ruler holds distance from start of layer

        core_length = self.core_bounds['min'] + random()*self.core_bounds['max']

        while (core_ruler <= core_length):
            layer_length = self.layer_bounds['min'] + random()*self.bounds['max']
            layer_colour = choice(self.colours)
            while (layer_ruler <= layer_length):

                layer_ruler += self.granularity
                core_ruler += self.granularity
        



