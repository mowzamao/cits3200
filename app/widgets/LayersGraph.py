import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtCore import QTimer

class LayersGraph(FigureCanvasQTAgg):
    """A wrapper class for a Matplotlib plot of the sediment layers"""
    layers_title_min_fontsize = 5
    layers_title_max_fontsize = 12 
    layers_title_base_fontsize = 7

    def __init__(self, parent=None, dpi=100, df = None):
        self.dpi = dpi
        self.parent = parent 
        height = len(df)
        width = 5
        df = df[self.getAnalysisType(df)]

        self.core_as_grid = self.createCore_as_grid(df,height, width)
        top,bottom = self.getColoursGraphCoordinates(parent) 
        self.layers_fig,self.layers_axes,self.layers_axes_top = self.setLayersFigure(dpi,top,bottom)
        self.layers_fig.canvas.mpl_connect('resize_event',self.resizeEvent)
        
        super(LayersGraph, self).__init__(self.layers_fig)

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
    
    def getAnalysisType(self,df:pd.DataFrame):
        """
        Function which returns a list of column names in the order of depth, R,G,B so that 
        imshow is given the correct colour values as inputs. For later development, this function can 
        be used to handle and setup CEILAB analysis.

        parameters:
            df(pd.Dataframe): pandas dataframe containing the data to be plotted.
        """
        df_columns = df.columns
        if 'Blue' in df_columns and 'Red' in df_columns and 'Green' in df_columns:
            return ['Depth (mm)','Red',"Green",'Blue']
        else:
            return None
    
    def setLayersFigure(self,dpi,top,bottom):
        #define the figure the plot will be rendered in
        layers_fig = Figure(dpi=dpi)

        #set axis
        layers_axes = layers_fig.add_subplot(111) 
        layers_axes.clear()
        layers_axes.set_position([0.1,bottom,0.8,(top-bottom)])
        layers_axes.set_xlim(0,1)
        layers_axes.set_ylim(0,1)
        layers_axes.set_xlabel('Bottom',fontweight = 'bold',labelpad = 10)
        layers_axes_top = layers_axes.twiny()
        layers_axes_top.set_xlabel('Top',fontweight = 'bold',labelpad = 10)
        #render image 
        layers_axes.imshow(self.core_as_grid,aspect = 'auto',extent=[0,1,0,1],origin = 'upper')

        #add title
        layers_fig.suptitle("Colour Layers",fontsize = 8, fontweight='bold',y = 0.97)

        #hiding ticks and their labels
        layers_axes.get_xaxis().set_ticks([])
        layers_axes.get_yaxis().set_ticks([])
        layers_axes_top.get_xaxis().set_ticks([])
        return layers_fig,layers_axes,layers_axes_top

    def getColoursGraphCoordinates(self,parent):
        top,bottom = parent.colours_graph.getLineHeightRelativeCoordinates()
        return top[1],bottom[1]

    def resizeEvent(self, event):
        """
        Function which resizes graphical parameters of the LayersGraph 
        as PyQt window is changed. There is a delayed run time for this function 
        to allow for the ColoursGraph to fully render. Without doing this the layers graph
        receives the wrong coordinates for the locaiton of the start and end points of the data.
        """
        # Call delayed function after 2 seconds
        QTimer.singleShot(10, self.delayed_resize_logic)

        # Initialise an instance of the new figure
        super().resizeEvent(event)

    def delayed_resize_logic(self):
        """ This method handles the delayed resizing logic. """
        if self.verifyDimensions():
            top, bottom = self.getColoursGraphCoordinates(self.parent)
            self.layers_axes.set_position([0.1, bottom, 0.8, (top - bottom)])
            self.setFontSize()
        self.draw_idle()


    def setFontSize(self):
        """
        Function which resets fontsize of LayersGraph Title
        """
        new_fontsize = self.calcNewFont()
        self.layers_fig.suptitle(self.layers_fig.get_suptitle(),fontsize = new_fontsize, fontweight='bold',y = 0.97)

        if new_fontsize > 14.5:
            new_fontsize = 14.5

        self.layers_axes.set_xlabel(self.layers_axes.get_xlabel(),fontsize = new_fontsize, fontweight='bold',labelpad = 10 )
        self.layers_axes_top.set_xlabel(self.layers_axes_top.get_xlabel(),fontsize = new_fontsize, fontweight='bold',labelpad = 10)

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
    



