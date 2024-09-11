DEPTH_RANGE = {'min':1,    'max':2}     # The depth of random cores in metres
LAYER_RANGE = {'min':0.01, 'max':0.05}  # The depth of a given layer  in metres

COLOURS     = [(234,208,168),    # The bases colours for randomly sampling
               (182,159,102), 
               (107,84,40), 
               (118,85,43),
               (255,77,179), 
               (64,41,5)]

NOISE       =  {'mean':0, 'sd':2}
COLOR_MAX   =  255

class RandomDataGenerator():

    """Creates random RGB data for use in testing the GUI graph
    """
    def __init__(self):

