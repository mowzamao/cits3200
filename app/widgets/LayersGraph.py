import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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
        self.df = df[['Depth (mm)','Red',"Green",'Blue']] 
        height = len(df)
        width = 1
        self.core_as_grid = self.createCore_as_grid(height, width)
        top,bottom = self.parent.colours_graph.setTopBottomCoordinates()
        self.setLayersFigure(dpi,top,bottom)

        self.layers_fig.canvas.mpl_connect('resize_event',self.resizeEvent)
        
        super(LayersGraph, self).__init__(self.layers_fig)

    def createCore_as_grid(self,height:int,width:int):
        """
        Function to add RGB data to the core_as_grid variable for the Layers plot. 
        The array has every row as a specific layer / colour and each column shows 
        a component of an RGB value.

        Parameters:
            df(pd.Dataframe): the data to be rendered in the layers plot.
        """
        core_as_grid = np.zeros((height, width, 3), dtype=float)

        for row in range(height):
            for col in range(width):
                for channel in range(3):
                    core_as_grid[row][col][channel] = int(self.df.loc[row, self.df.columns[channel+1]])/255
        return core_as_grid
    
    def setLayersFigure(self,dpi,top,bottom):
        self.layers_fig = Figure(dpi=dpi)
        self.setLayerPlotAxes(top,bottom)
        self.plotLayers()
        self.layers_axes.invert_yaxis()
        self.layers_fig.suptitle("Colour Layers",fontsize = 8, fontweight='bold',y = 0.97)
        self.setTopBottomLabels(fontweight = 'bold',labelpad = 10)
        self.setCustomTicks(which='both',labelleft=False,left=False,labelbottom=False,bottom=False)

    def setLayerPlotAxes(self,top:float,bottom:float):
        """
        Function defining the axes of the layers graph. 
        """
        self.layers_axes = self.layers_fig.add_subplot(111) 
        self.layers_axes.clear()
        self.layers_axes.set_position([0.1,bottom,0.8,(top-bottom)])
        self.layers_axes.set_xlim([0, 1])
    
    def setTopBottomLabels(self,fontweight:str = 'bold',labelpad:float = 10):
        """
        Function setting the labels for the layers graph which indicate the top and bottom of the core (and thus 
        the direction of image processing / scanning).
        """
        self.layers_axes.set_xlabel('Bottom',fontweight = fontweight,labelpad = labelpad)
        self.layers_axes_top = self.layers_axes.twiny()
        self.layers_axes_top.set_xlabel('Top',fontweight = fontweight,labelpad = labelpad)


    def setCustomTicks(self,which:str,labelleft:bool,left:bool,labelbottom:bool,bottom:bool):
        """
        Function setting custom tick parameters for the layers plot. 
        """
        self.layers_axes.yaxis.set_tick_params(which = which,labelleft = labelleft,left = left)
        self.layers_axes.xaxis.set_tick_params(which = which,labelbottom = labelbottom,bottom = bottom)
        self.layers_axes_top.get_xaxis().set_ticks([])


    def plotLayers(self):
        """
        Function iterating through core as gird variable and plotting coloured rectangles
        onto the layer plot axes to represent the core laminations. 
        """
        depths = list(self.df['Depth (mm)'])
        thickness = depths[1] - depths[0]
        for i, color in enumerate(self.core_as_grid):
            depth = depths[i]
            rect = patches.Rectangle((0, depth), 1,  thickness, facecolor=color)
            self.layers_axes.add_patch(rect)

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
            top, bottom = self.parent.colours_graph.setTopBottomCoordinates()
            self.layers_axes.set_position([0.1, bottom, 0.8, (top - bottom)])
            self.layers_axes.invert_yaxis()
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
    
    def flipTopBottomLabels(self):
        """
        Function to flip the location of the top and bottom labels on the layers graph.
        """
        old_bottom_xlabel = self.layers_axes.get_xlabel()
        old_top_label = self.layers_axes_top.get_xlabel()
        self.layers_axes_top.set_xlabel(old_bottom_xlabel)
        self.layers_axes.set_xlabel(old_top_label)
    



