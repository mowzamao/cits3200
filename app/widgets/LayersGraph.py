import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

class LayersGraph(FigureCanvasQTAgg):
    """A wrapper class for a Matplotlib plot of the sediment layers"""

    def __init__(self, parent=None, width=5, height=5, dpi=100, df = None):

        #defining metadate for layers plot
        self.layers_title_min_fontsize = 5
        self.layers_title_max_fontsize = 12 
        self.layers_title_base_fontsize = 7 
        self.layers_min_width = 1.5
        height = len(df)
        width = max(1, height//10)
        self.core_as_grid = self.createCore_as_grid(df,height, width) 
        self.setupLayersFigure(width,height,dpi)
        super(LayersGraph, self).__init__(self.layers_fig)

        self.layers_fig.canvas.mpl_connect('resize_event',self.resizeEvent)

    def setupLayersFigure(self,width,height, dpi):
        #define the figure the plot will be rendered in 
        self.layers_fig = Figure(figsize=(width, height), dpi=dpi)
        
        # Create a GridSpec with 2 rows and 1 column
        gs = GridSpec(nrows=3, ncols=3, height_ratios=[0.1, 0.8,0.1],width_ratios=[0.05,0.9,0.05], figure=self.layers_fig)
        self.layers_axes = self.layers_fig.add_subplot(gs[1, 1])

        # #remove axis / make them invisible 
        self.layers_axes.get_xaxis().set_ticks([])
        self.layers_axes.get_yaxis().set_ticks([])

        #render image 
        self.layers_fig.suptitle("Colour Layers",fontsize = 8, fontweight='bold',y = 0.97)
        self.layers_axes.imshow(self.core_as_grid,aspect='auto')


    def createCore_as_grid(self,df:pd.DataFrame,height:int,width:int):
        """
        Function to add RGB data to the core_as_grid variable for the Layers plot. 
        The array has every row as a specific layer / colour and each column shows 
        a component of an RGB value.

        Parameters:
            df(pd.Dataframe): the data to be rendered in the layers plot.
        """
        core_as_grid = np.zeros((height, width, 3), dtype=int)

        for row in range(height):
            for col in range(width):
                for channel in range(3):
                    core_as_grid[row][col][channel] = int(df.loc[row, df.columns[channel+1]])
        return core_as_grid
    
    def resizeEvent(self, event):
        """
        Function which resizes graphical parameters of the LayersGraph 
        as PyQt window is changed.  
        """
        if self.verifyDimensions():
            if self.verifyFigGreaterThanMinWidth(): 
                self.setFontSize()
            self.layers_fig.tight_layout()
        
        self.draw()
        # Initialise an instance of the new figure
        super().resizeEvent(event)  
        

    def setFontSize(self):
        """
        Function which resets fontsize of LayersGraph Title
        """
        new_fontsize = self.calcNewFont()
        print(new_fontsize)
        self.layers_fig.suptitle("Colour Layers",fontsize = new_fontsize, fontweight='bold',y = 0.97)

    def calcNewFont(self):
        """
        Function which calculates new fontsize for LayersGraph as it's resized. 
        """
        fig_width = self.layers_fig.get_figwidth()
        scale_factor = fig_width / 0.9

        #choose smallest font out of the new scaled font or the outright maximum font
        new_fontsize = min(self.layers_title_base_fontsize * scale_factor,self.layers_title_max_fontsize)

        #choose largest font out of the outright minimum font size and the new scaled font size
        font_size = max(self.layers_title_min_fontsize,new_fontsize)
        return font_size

    def verifyDimensions(self):
        """
        Function to check dimensions of layers Graph is greater than 0.
        """
        width, height = self.layers_fig.get_size_inches()
        return width > 0 and height > 0 
    
    def verifyFigGreaterThanMinWidth(self):
        """
        Function which checks LayersGraph Figure is less than minimum width. 
        """
        #calculation of subplot size in inches, requires conversion form normalised units
        fig_width = self.layers_fig.get_figwidth()
        return fig_width <= self.layers_min_width



