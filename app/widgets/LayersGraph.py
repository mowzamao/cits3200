import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

from PyQt6 import QtCore, QtWidgets

class LayersGraph(FigureCanvasQTAgg):
    """A wrapper class for a Matplotlib plot of the sediment layers"""

    def __init__(self, parent=None, dpi=100, df = None):

        #defining metadate for layers plot
        self.layers_title_min_fontsize = 5
        self.layers_title_max_fontsize = 12 
        self.layers_title_base_fontsize = 7 
        height = len(df)
        width = max(1, height//10)

        self.core_as_grid = self.createCore_as_grid(df,height, width)
        top,bottom = self.getColoursGraphCoordinates(parent) 
        self.setupLayersFigure(dpi,top,bottom)
        
        super(LayersGraph, self).__init__(self.layers_fig)
        
        self.layers_fig.canvas.mpl_connect('resize_event',self.resizeEvent)


    def getColoursGraphCoordinates(self,parent):
        figure = self.accessColourGraph(parent)
        first_data_point,last_data_point = self.getFirstAndLastDataPoints(figure)
        first_data_point,last_data_point = self.relativeCoordinatesTransformation(figure,first_data_point,last_data_point)
        return first_data_point[1], last_data_point[1]
    
    def accessColourGraph(self,parent) -> Figure:
        return parent.colours_graph.figure
    
    def getFirstAndLastDataPoints(self,figure:Figure):
        #retrieve intensity and depth data 
        intensity = figure.axes[0].lines[0].get_xdata()
        depth = figure.axes[0].lines[0].get_ydata()
        #retrieve first and last data points of the data
        first_data_point = (intensity[0],depth[0])
        last_data_point = (intensity[-1],depth[-1])
        return first_data_point,last_data_point
    
    def relativeCoordinatesTransformation(self,figure:Figure,first_data_point:tuple,last_data_point:tuple):
        #define transformation
        data_to_figure = figure.axes[0].transData + figure.transFigure.inverted()

        #transform first and last data points
        first_data_point = tuple(data_to_figure.transform((first_data_point)))
        last_data_point = tuple(data_to_figure.transform((last_data_point)))
        return first_data_point,last_data_point
    

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
    
    def setupLayersFigure(self,dpi,top,bottom):
        #define the figure the plot will be rendered in 
        self.layers_fig = Figure(dpi=dpi)

        top_space = 1- top
        bottom_space = bottom
        middle_space = 1 - (top_space + bottom_space)

        # Create a GridSpec with 2 rows and 1 column
        gs = GridSpec(nrows=3, ncols=3, height_ratios=[top_space,middle_space,bottom_space],width_ratios=[0.05,0.9,0.05], figure=self.layers_fig)
        self.layers_axes = self.layers_fig.add_subplot(gs[1, 1])

        # remove axis / make them invisible 
        self.layers_axes.get_xaxis().set_ticks([])
        self.layers_axes.get_yaxis().set_ticks([])

        #render image 
        self.layers_fig.suptitle("Colour Layers",fontsize = 8, fontweight='bold',y = 0.97)
        self.layers_axes.imshow(self.core_as_grid,aspect='auto')
    
    def resizeEvent(self, event):
        """
        Function which resizes graphical parameters of the LayersGraph 
        as PyQt window is changed.  
        """
        if self.verifyDimensions():
            self.setFontSize()
            self.layers_fig.tight_layout()
        
        self.draw_idle()
        # Initialise an instance of the new figure
        super().resizeEvent(event)  

    def setFontSize(self):
        """
        Function which resets fontsize of LayersGraph Title
        """
        new_fontsize = self.calcNewFont()
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
    



