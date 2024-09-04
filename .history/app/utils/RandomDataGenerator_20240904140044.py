from random import random

class RandomDataGenerator():
    """Creates random RGB data for use in testing the GUI graph"""

    def __init__(self):
        self.core_bounds   = {'min':1, 'max':2}        # The length of random cores in metres
        self.layer_bounds  = {'min':0.01, 'max':0.05}  # The depth of a given layer  in metres
    
        self.noise      = {'mean':0, 'sd':2}
        self.rgb_range  = {'min':0, 'max':255}

        self.granularity = 0.01 # The distance between measurements in a generated core

        # The bases colours for randomly sampling
        self.colours   = [(234,208,168), (182,159,102), (107,84,40), (118,85,43), (255,77,179), (64,41,5)]
       
    
    def get_random_dataset(self):
        
        # Inner ruler holds distance from start of layer
        # Outer ruler holds distance from start of the core

        outer_ruler = 0
        inner_ruler = 0

        core_length = self.core_bounds['min'] + random()*self.core_bounds['max']

        while (outer_ruler <= core_length) {
            layer_length = self.layer_s['min'] + random()*self.length['max']

            outer_ruler += self.granularity
        }



