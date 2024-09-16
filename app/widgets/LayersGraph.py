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

        #defining metadate for layers plot
        self.layers_title_min_fontsize = 3
        self.layers_title_max_fontsize = 10 
        self.layers_title_base_fontsize = 7 
        self.layers_min_width = 0.15    
        height = len(df)
        width = max(1, height//10)

        core_as_grid = self.createCore_as_grid(df,height, width)
        self.setupLayersFigure(width,height,dpi)
        super(LayersGraph, self).__init__(self.layers_fig)
        self.renderLayersFigure(core_as_grid)


    def renderLayersFigure(self,core_as_grid):
        #render image
        self.layers_axes.imshow(core_as_grid, aspect='auto')
        #show title
        self.layers_axes.set_title("Colour Layers",fontsize = 8, fontweight='bold')

    def setupLayersFigure(self,width,height,dpi):
        #define the figure the plot will be rendered in 
        self.layers_fig = Figure(figsize=(width, height), dpi=dpi)
        self.layers_axes = self.layers_fig.add_subplot(111)

        #remove axis / make them invisible 
        self.layers_axes.get_xaxis().set_ticks([])
        self.layers_axes.get_yaxis().set_ticks([])


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
            self.layers_fig.tight_layout()

        if self.verifyFigGreaterThanMinWidth() and self.verifytitleGreaterThanMinFont():
            self.setFontSize()
        
        self.draw()
        # Initialise an instance of the new figure  
        super().resizeEvent(event)
    
    def verifytitleGreaterThanMinFont(self):
        """
        Function verifying if LayerGraph's newfont is greater than it's
        minimum allowed font. 
        """
        new_fontsize = self.calcNewFont()
        if new_fontsize <= self.layers_title_min_fontsize:
            return False
        return True
    
    def verifyFigGreaterThanMinWidth(self):
        """
        Function which checks LayersGraph Figure is less than minimum width. 
        """
        #calculation of subplot size in inches, requires conversion form normalised units
        norm_width = self.layers_axes.get_position().width
        fig_width, fig_height = self.layers_fig.get_size_inches()
        fig_width_inches = fig_width *norm_width
        
        if fig_width_inches <= self.layers_min_width:
            return False
        return True

    def setFontSize(self):
        """
        Function which resets fontsize of LayersGraph Title
        """
        new_fontsize = self.calcNewFont()
        self.layers_axes.set_title("Colour Layers",fontsize = new_fontsize, fontweight='bold')

    def calcNewFont(self):
        """
        Function which calculates new fontsize for LayersGraph as it's resized. 
        """
        width, height = self.layers_fig.get_size_inches()
        scale_factor = width / 0.9

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
        if width > 0 and height > 0:
            return True
        else:
            return None



