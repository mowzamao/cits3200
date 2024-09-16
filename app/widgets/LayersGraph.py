import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class LayersGraph(FigureCanvasQTAgg):
    """A wrapper class for a Matplotlib plot of the sediment layers"""

    def __init__(self, parent=None, width=5, height=5, dpi=100, df = None):    

        #define metadata for layer plot
        self.height = len(df)
        self.width = max(1, height//10)
        self.core_as_grid = np.zeros((height, width, 3), dtype=int)

        #populate the numpy array with RGB values which numpy.imshow will render
        self.populateCore_as_grid(df)

        #define the figure the plot will be rendered in 
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        #remove axis / make them invisible 
        self.axes.get_xaxis().set_ticks([])
        self.axes.get_yaxis().set_ticks([])

        #initialise instance of the plot and render image 
        super(LayersGraph, self).__init__(fig)
        self.axes.imshow(self.core_as_grid)

    def populateCore_as_grid(self,df:pd.DataFrame):
        """
        Function to add RGB data to the core_as_grid variable for the Layers plot. 
        The array has every row as a specific layer / colour and each column shows 
        a component of an RGB value.

        Parameters:
            df(pd.Dataframe): the data to be rendered in the layers plot. gi
        """
        for row in range(self.height):
            for col in range(self.width):
                for channel in range(3):
                    self.core_as_grid[row][col][channel] = int(df.loc[row, df.columns[channel+1]])



