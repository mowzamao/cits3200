from random import random, choice
from numpy.random import normal

class RandomDataGenerator():
    """Creates random RGB data for use in testing the GUI graph"""

    def __init__(self):
        self.core_bounds   = {'min':1, 'max':2}        # The length of random cores in metres
        self.layer_bounds  = {'min':0.01, 'max':0.05}  # The depth of a given layer  in metres
        self.noise         = {'mean':1, 'sd':2}
        self.granularity = 0.01 # The distance between measurements in a generated core
        
        # The bases colours for randomly sampling
        self.colours = [[234,208,168], [182,159,102], [107,84,40], [118,85,43], [255,77,179], [64,41,5]]
       

    def add_noise(self, value):
        noise = normal(self.noise['mean'], self.noise['sd'], 1)[0]
        # Correcting value if the noise puts in out of bounds
        return max(0, min(255, int(value + noise)))


    
    def get_random_dataset(self):
        core_ruler  = 0 # Outer ruler holds distance from start of the core
        core_length = self.core_bounds['min'] + random()*self.core_bounds['max']
       
        while (core_ruler <= core_length):
            layer_ruler = 0 # Inner ruler holds distance from start of layer
            layer_length = self.layer_bounds['min'] + random()*self.layer_bounds['max']
            layer_colour = choice(self.colours)

            while (layer_ruler <= layer_length):
                rgb_row = [self.add_noise(layer_colour[i]) for i in range(3)]
                print(rgb_row)
                layer_ruler += self.granularity
                core_ruler += self.granularity
        


x = RandomDataGenerator()
x.get_random_dataset()

