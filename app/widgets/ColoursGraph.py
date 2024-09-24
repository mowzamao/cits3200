
#import matplotlib and set backend configuration for pyqt compatability
import matplotlib
matplotlib.use('QtAgg')
import numpy as np
import pandas as pd

#import FigureCanvasQTAGG - a class used as a widget which displays matplotlib plots in pyqt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

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

    def __init__(self, parent:classmethod=None, width:float=5, height:float=5, dpi:int=100, df:pd.DataFrame = None):
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
        self.subplot_min_width = 0.35
        self.base_font_size = 10     
        
        #Defining the top-end matplotlib figure 
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        

        # Drawing three subplots, one for each colour channel
        self.axes_left = self.fig.add_subplot(131)
        self.axes_center = self.fig.add_subplot(132)
        self.axes_right = self.fig.add_subplot(133)

        # initialise an instance of the ColoursGraph class
        super(ColoursGraph, self).__init__(self.fig)

        #plot data for the ColourGraph Panel
        self.plotColourData(df)

        #adding headings for the entire ColoursGraph figure
        self.setFigureAxisLabels('Depth (m)','Intensity (%)')

        #adding title to the entire matplotlib figure
        self.addFigureTitle(df)

        #connecting resize event to graph
        self.fig.canvas.mpl_connect('resize_event',self.resizeEvent)
        

    def plotColourData(self,df:pd.DataFrame):
        """
        Function which iterative plots data from an inputted pandas dataframe onto three subplots.
        """
        for index,subplot in enumerate([self.axes_left,self.axes_center,self.axes_right],start=1):

            #for each subplot in the ColoursGraph panel prepare the pandas series to be plotted
            data_column_name,depth_column, data_column = self.graphDataPreperation(df,index)

            #plot the data from the pandas dataframe
            subplot.plot(data_column, depth_column,  color = data_column_name)

            #set the graphical parameters for each subplot
            subplot.set_title(data_column_name)
            subplot.grid(axis = 'y')
            subplot.invert_yaxis()
            subplot.set_xlim(0,100)

    def addFigureTitle(self,df:pd.DataFrame = None,fontsize:int = 16,title:str = None):
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
        if df is not None and title is None:
            analysis_type = df.columns[1][0] + df.columns[2][0] + df.columns[3][0]
            title = analysis_type + ' Colour Space Plot'

        #store title string as a class variable for later access
        self.figure_title = title

        #render new title onto matplotlib figure  
        self.fig.suptitle(title, fontweight='bold',y = 0.97,fontsize = fontsize)


    def setFigureAxisLabels(self,x_label:str,y_label:str):
        """
        Function which sets the axis labels for the entire ColoursGraph plot panel. 
        """
        self.axes_left.set_ylabel(x_label)
        self.axes_center.set_xlabel(y_label)


    def graphDataPreperation(self,df:pd.DataFrame,index:int):
        """
        Function that takes a dataframe and an index (ranging in values from 1-3) and 
        returns two series and a string. The two series contain data to be plotted in the 
        graphsPanel window. The string is the title for the subplot (and also is the column name
        from which the plotted data originates). 
        """
        df_columns = df.columns

        #extracting name of column to be plotted
        data_column_name = df_columns[index]
        
        #cleaning and scaling the data to be plotted 
        data_column = round(100*df[data_column_name]/255,  4)

        #defining the data to be plotted on the x_axis
        depth_column = df.iloc[:,0]
        return data_column_name,depth_column, data_column 

    
    def resizeEvent(self, event):
        """
        Event handler function that will adjust the graphical parameters of the 
        matplotlib figure. 
        
        There are two main changes: 
            1) changing font size
            2) turning tight layout on and off.
        """
        #change font size if current font size and subplot width not below minimum values
        if self.verifyLabelFontChange():
            self.setFontSize()

        #set tight_layout setting to figure if figure has dimensions
        if self.verifyTightLayout():
            self.fig.tight_layout()

        # Redraw the figure
        self.draw()
        # Initialise an instance of the new figure  
        super().resizeEvent(event)

    def changeEvent(self, event):
        """
        Override the changeEvent to handle maximization and minimization.
        When the window is minimized or maximized, this method will be called,
        and we can trigger the resizing logic.
        """
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            window_state = self.window().windowState()
            if window_state & QtCore.Qt.WindowState.WindowMinimized:
                # The window has been minimized
                self.resizeEvent(event)
            elif window_state & QtCore.Qt.WindowState.WindowMaximized:
                # The window has been maximized
                self.resizeEvent(event)
            elif window_state == QtCore.Qt.WindowState.WindowNoState:
                # The window has been restored from minimized or maximized
                self.resizeEvent(event)
        super().changeEvent(event)

    def setFontSize(self):
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
            ax.set_title(ax.get_title(), fontsize=new_font_size)
        
        #adjusting font size of title
        self.addFigureTitle(title = self.figure_title,fontsize=new_font_size + 2)
        

    def calcNewFont(self):
        """
        Calculates the new font size for x and y axis labels when
        the ColoursGraph widget gets resized. 
        """
        width, height = self.fig.get_size_inches()
        scale_factor = width / 5

        #choose smallest font out of the new scaled font or the outright maximum font
        new_font_size = min(self.base_font_size * scale_factor,self.label_max_font_size)

        #choose largest font out of the outright minimum font size and the new scaled font size
        font_size = max(self.label_min_font_size,new_font_size)
        return font_size

    def verifyLabelFontChange(self):
        """
        Function to check is the matplotlib Figure being rendered in the 
        FigureCanvasQtAgg (Colours Graph) widget currently has the smallest font
        size setting set.
        """
        if self.verifyLabelGreaterThanMinFontSize() is False:
            return None
        if self.verifySubplotGreaterThanMinWidth() is False:
            return None
        return True

    def verifyLabelGreaterThanMinFontSize(self):
        """
        Function checking if the current font size of a subplots labels
        are greater than the minimum label font size
        """
        x_label_font_size = self.axes_left.xaxis.label.get_fontsize()

        if x_label_font_size <= self.label_min_font_size:
            return False
        return True

    
    def verifySubplotGreaterThanMinWidth(self):
        """
        Function checking if the width of subplots is greater than
        the minimum allowable width of a subplot
        """
        #calculation of subplot size in inches, requires conversion form normalised units
        norm_width = self.axes_center.get_position().width
        fig_width, fig_height = self.fig.get_size_inches()
        subplot_width_inches = fig_width *norm_width

        if subplot_width_inches <= self.subplot_min_width:
            return False
        return True

    def verifyTightLayout(self):
        """
        Function to check if the matplotlib Figure being rendered in the 
        FigureCanvasQTAGG (Colours Graph) widget has a width and height 
        greater than 0 inches.
        """
        # Get the current width and height of the figure
        width, height = self.fig.get_size_inches()

        if width > 0 and height > 0:
            return True
        else:
            return None


