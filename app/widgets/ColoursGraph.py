
#import matplotlib and set backend configuration for pyqt compatability
import matplotlib
matplotlib.use('QtAgg')
import numpy as np

#import FigureCanvasQTAGG - a class used as a widget which displays matplotlib plots in pyqt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

#import Figure - a class which is matplotlib's top-end container for plots
from matplotlib.figure import Figure

class ColoursGraph(FigureCanvasQTAgg):
    """
    A class acting as a PyQt widget which will contain matplotlib plots.
    FigureCanvasQTAGG acts a base class for ColoursGraph class (thus inheriting methods for matplotlib compatability).
    The widget will show 3 subplots where each plot shows a component of the RGB or L*A*B* colour space. 
    The plots are displayed vertically on the MainWindow of the application. 

    Parameters:
        FigureCanvasQTAgg(Class): Child class allowing ColoursGraph class to inheret methods for matplotlib and PyQt compatability
    """

    def __init__(self, parent=None, width=5, height=5, dpi=100, df = None):
        """ 
        Initialisation function for the ColourGraph PyQt Widget.

        Parameters:
            parent(None): Variable declaring that this widget has no parent widget (except the main window). 
            width(int): The width of the matplotlib figure. 
            height(int): The height of the matplot figure. 
            dpi(int): matplotlib resolution settings - Dots Per Inch. 
            df(pd.Dataframe): A Pandas Dataframe containing the data to be displayed. 
        """    
        
        #Defining the top-end matplotlib figure 
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.label_min_font_size = 3
        self.label_max_font_size = 20
        self.subplot_min_width = 5

        # Drawing three subplots, one for each colour channel
        self.axes_left = self.fig.add_subplot(131)
        self.axes_center = self.fig.add_subplot(132)
        self.axes_right = self.fig.add_subplot(133)

        # Calling the initialsation function of ColourGraph's parent class FigureCanvasQTAGG and passing in 
        #matplotlib's Figure class to specify the parameters of the plots
        super(ColoursGraph, self).__init__(self.fig)

        # Red channel
        self.axes_left.set_title('Red')
        self.axes_left.plot(round(100*df['Red']/255,  4), df['Depth'],  color='red')
        self.axes_left.grid(axis = 'y')
        self.axes_left.invert_yaxis()
        self.axes_left.set_ylabel('Depth (m)')
        self.axes_left.set_xlim(0, 100)

        # Green channel
        self.axes_center.set_title('Green')
        self.axes_center.plot(round(100*df['Green']/255,  4), df['Depth'],  color='green')
        self.axes_center.grid(axis = 'y')
        self.axes_center.invert_yaxis()
        self.axes_center.set_xlabel('Intensity (%)')
        self.axes_center.set_xlim(0, 100)

        # Blue channel
        self.axes_right.set_title('Blue')
        self.axes_right.plot(round(100*df['Blue']/255,  4), df['Depth'],  color='blue')
        self.axes_right.grid(axis = 'y')
        self.axes_right.invert_yaxis()
        self.axes_right.set_xlim(0, 100)

        # Call tight_layout initially
        self.fig.tight_layout()
    
    def resizeEvent(self, event):
        #set new graphical parameters for figure on resize of window
        self.setResizeFormatParameters()
        # Redraw the figure
        self.draw()
        # Initialise an instance of the new figure  
        super().resizeEvent(event)

    def setResizeFormatParameters(self):
        #set tight_layout setting to figure if figure has dimensions
        if self.verifyTightLayout():
            self.fig.tight_layout()
        
        if self.verifyLabelFontChange():
            self.setFontSize()

    def setFontSize(self):
        """
        Sets a new font size for the x and y labels on the matplotlib plot.
        """
        font_size = self.calcNewFont()
        for ax in self.fig.get_axes():
            ax.xaxis.label.set_fontsize(font_size)
            ax.yaxis.label.set_fontsize(font_size)

    def calcNewFont(self):
        """
        Calculates the new font size for x and y axis labels when
        the ColoursGraph widget gets resized. 
        """
        width, height = self.fig.get_size_inches()
        scale_factor = width / 3
        base_font = 10 

        #choose smallest font out of the new scaled font or the outright maximum font
        new_font_size = min(base_font * scale_factor,self.label_max_font_size)

        #choose largest font out of the outright minimum font size and the new scaled font size
        font_size = max(self.label_min_font_size,new_font_size)
        return font_size

    def verifyLabelFontChange(self):
        """
        Function to check is the matplotlib Figure being rendered in the 
        FigureCanvasQtAgg (Colours Graph) widget currently has the smallest font
        size setting set.
        """
        if self.verifyLabelGreaterThanMinFontSize() is None:
            return None
        if self.verifySubplotGreaterThanMinWidth() is None:
            return None
        return True

    def verifyLabelGreaterThanMinFontSize(self):
        """
        Function checking if the current font size of a subplots labels
        are greater than the minimum label font size
        """
        x_label_font_size = self.axes_left.xaxis.label.get_fontsize()
        font_size_bool = bool(x_label_font_size > self.label_min_font_size)
        if font_size_bool is False:
            return None
        return True

    
    def verifySubplotGreaterThanMinWidth(self):
        """
        Function checking if the width of subplots is greater than
        the minimum allowable width of a subplot
        """
        subplot_width = self.axes_center.get_position().width
        subplot_size_bool = bool(subplot_width > self.subplot_min_width)
        if subplot_size_bool is False:
            return None
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


