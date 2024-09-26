
#import matplotlib and set backend configuration for pyqt compatability
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.axes
import matplotlib.figure
import numpy as np
import pandas as pd

#import FigureCanvasQTAGG - a class used as a widget which displays matplotlib plots in pyqt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.ticker import MaxNLocator,MultipleLocator

#import Figure - a class which is matplotlib's top-end container for plots
from matplotlib.figure import Figure

from PyQt6 import QtCore, QtWidgets

class ColoursGraph(FigureCanvasQTAgg):
    """
    A class acting as a PyQt widget which will contain matplotlib plots.
    FigureCanvasQTAGG acts a base class for ColoursGraph class (thus inheriting methods for matplotlib compatability).
    The widget will show 3 subplots where each plot shows a component of the RGB or L*A*B* colour space. 
    The plots are displayed vertically on the MainWindow of the application. 

    Parameters:
        FigureCanvasQTAgg(Class): Child class allowing ColoursGraph class to inheret methods for matplotlib and PyQt compatability
    """

    def __init__(self, parent:classmethod=None, dpi:int=100, df:pd.DataFrame = None):
        """ 
        Initialisation function for the ColourGraph PyQt Widget.

        Parameters:
            parent(None): Variable declaring that this widget has no parent widget (except the main window). 
            width(int): The width of the matplotlib figure. 
            height(int): The height of the matplot figure. 
            dpi(int): matplotlib resolution settings - Dots Per Inch. 
            df(pd.Dataframe): A Pandas Dataframe containing the data to be displayed. 
        """

        #define default values for subplot graphical parameters
        self.label_min_font_size = 3
        self.label_max_font_size = 20
        self.axes_min_width = 0.35
        self.base_font_size = 10
        self.df = df 
        self.dpi = dpi
        
        #Defining the top-end matplotlib figure 
        self.fig = Figure(dpi=dpi)

        self.plotColourData(df)

        #connecting resize event to graph
        self.fig.canvas.mpl_connect('resize_event',self.resizeEvent)


        # initialise an instance of the ColoursGraph class
        super(ColoursGraph, self).__init__(self.fig)

    def getLineHeightRelativeCoordinates(self):
        first_data_point = (self.df.iloc[0,1],self.df.iloc[0,0])
        last_data_point = (self.df.iloc[-1,1],self.df.iloc[-1,0])
        
        first_data_point = self.getNormalisedCoords(first_data_point)
        last_data_point = self.getNormalisedCoords(last_data_point)
        return first_data_point, last_data_point
    
    def getNormalisedCoords(self,data_point):
        width,height = self.fig.get_size_inches()
        data_point = self.fig.axes[0].transData.transform(data_point) 
        return (data_point[0]/(width*self.dpi),data_point[1]/(height*self.dpi))
    
    def plotColourData(self,df:pd.DataFrame):
        """
        Function which iterative plots data from an inputted pandas dataframe onto three subplots.
        """
        # Drawing three subplots, one for each colour channel
        axes_left = self.fig.add_subplot(131)
        axes_center = self.fig.add_subplot(132)
        axes_right = self.fig.add_subplot(133)

        for index,ax in enumerate(self.fig.axes,start=1):
            color_data = round(100*df.iloc[:,index]/255,  4)
            depth = df.iloc[:,0]
            color_component = df.columns[index]

            ax.plot(color_data, depth, color = color_component)

            ax.set_title(color_component, fontweight='bold',pad = 10)

            ax = self.setCustomTicks(ax)

            ax.grid(axis = 'both',visible=True)
            ax.set_xlim(0,100)
            ax.set_ylim(bottom=0)
            ax.invert_yaxis()
        
        #add title to figure 
        self.addFigureTitle(df = df)

        #adding headings for the entire ColoursGraph figure
        axes_left.set_ylabel('Depth (m)')
        axes_center.set_xlabel('Intensity (%)')

    def setCustomTicks(self,ax:matplotlib.axes.Axes):
        ax.yaxis.set_major_locator(MaxNLocator(nbins=20))
        ax.xaxis.set_major_locator(MaxNLocator(nbins=4))

        ax.yaxis.minorticks_on()
        ax.yaxis.set_minor_locator(MultipleLocator(0.05))
        ax.xaxis.set_minor_locator(MultipleLocator(5))

        ax.tick_params(axis='x', which='both', top=True, labeltop=False)
        ax.tick_params(axis='y', which='both', right=True, labelright=False)

        ax.tick_params(which='minor', length=4, color='grey')
        return ax
        

    def addFigureTitle(self,figure_title:str=None,df:pd.DataFrame = None,fontsize:int = 16):
        """
        Function to add a title to the entire ColoursGraph Matplotlib figure. The string
        to be rendered as a title can be generated through two methods. 1) using the first letter 
        of the 2nd - 4th column names of a pandas dataframe passed to the function, 2)using a string
        passed into the function. 

        parameters:
            df(pd.Dataframe - optional): A pandas dataframe containing the plotted data. The column names of the dataframe are used for the title
            fontsize(int): Parameter setting the size of the title.
            title(str - optional): A string which will be rendered as the matplotlib figure's title.
        """
        #if no title string is provided generate a title string based of df column names
        if df is not None and figure_title is None:
            analysis_type = df.columns[1][0] + df.columns[2][0] + df.columns[3][0]
            figure_title = analysis_type + ' Colour Space Plot'

        #render new title onto matplotlib figure  
        self.fig.suptitle(figure_title, fontweight='bold',fontsize = fontsize)
    
    def resizeEvent(self,event):
        """
        Event handler function that will adjust the graphical parameters of the 
        matplotlib figure. 
        
        There are two main changes: 
            1) changing font size
            2) turning tight layout on and off.
        """
        #change font size if current font size and subplot width not below minimum values
        if self.verifyLabelGreaterThanMinFontSize():
            self.setFontSize()

        #set tight_layout setting to figure if figure has dimensions
        if self.verifyTightLayout():
            self.fig.tight_layout()

        # Redraw the figure
        self.draw_idle()
        super().resizeEvent(event)


    def setFontSize(self,):
        """
        Sets new parameters for font size graphical elements of the matplotlib figure.
        These include title, tick markers and axis labels font sizes.
        """
        new_font_size = self.calcNewFont()
        for ax in self.fig.get_axes():
            #setting new font size for figure x and y labels
            ax.xaxis.label.set_fontsize(new_font_size)
            ax.yaxis.label.set_fontsize(new_font_size)

            #setting new font size for tick/axis labels
            ax.tick_params(axis='x', labelsize=new_font_size)
            ax.tick_params(axis='y', labelsize=new_font_size)

            #setting new font size for title
            ax.set_title(label = ax.get_title(), fontsize=new_font_size,fontweight = 'bold',pad = 10)
        
        #adjusting font size of title
        self.addFigureTitle(figure_title = self.fig.get_suptitle(),fontsize=new_font_size + 2)
        

    def calcNewFont(self):
        """
        Calculates the new font size for x and y axis labels when
        the ColoursGraph widget gets resized. 
        """
        width, _ = self.fig.get_size_inches()
        scale_factor = width / 5

        #choose smallest font out of the new scaled font or the outright maximum font
        new_font_size = min(self.base_font_size * scale_factor,self.label_max_font_size)

        #choose largest font out of the outright minimum font size and the new scaled font size
        font_size = max(self.label_min_font_size , new_font_size)
        return font_size

    def verifyLabelGreaterThanMinFontSize(self):
        """
        Function checking if the current font size of a subplots labels
        are greater than the minimum label font size
        """
        return self.fig.axes[0].xaxis.label.get_fontsize() >= self.label_min_font_size

    def verifyTightLayout(self):
        """
        Function to check if the matplotlib Figure being rendered in the 
        FigureCanvasQTAGG (Colours Graph) widget has a width and height 
        greater than 0 inches.
        """
        width, height = self.fig.get_size_inches()
        return width > 0 and height > 0 


