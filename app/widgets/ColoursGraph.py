
#import matplotlib and set backend configuration for pyqt compatability
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.axes
import matplotlib.figure
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator
from matplotlib.widgets import SpanSelector


#import FigureCanvasQTAGG - a class used as a widget which displays matplotlib plots in pyqt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.ticker import MaxNLocator,AutoMinorLocator

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
    label_min_font_size = 3
    label_max_font_size = 14.5
    axes_min_width = 0.35
    base_font_size = 10


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
        self.df = df 
        self.dpi = dpi 
        self.fig = Figure(dpi=self.dpi)
        self.plotColourData(df)

        #connecting resize event to graph
        self.fig.canvas.mpl_connect('resize_event',self.resizeEvent)

        super(ColoursGraph, self).__init__(self.fig)

    
    def plotColourData(self,df:pd.DataFrame):
        """
        Function which iterative plots data from an inputted pandas dataframe onto three subplots.

        parameters:
            df(pd.Dataframe): the pandas dataframe with the colour data to be plotted
        """
        # Drawing three subplots, one for each colour channel
        self.axes_left = self.fig.add_subplot(131)
        self.axes_center = self.fig.add_subplot(132, sharex=self.axes_left, sharey=self.axes_left)
        self.axes_right = self.fig.add_subplot(133, sharex=self.axes_left, sharey=self.axes_left)
        
        column_names = self.getAnalysisType(df)

        for ax,column_name in zip(self.fig.axes,column_names):
            #get colour arrays to be plotted 
            color_data = round(100*df[column_name]/255,  4)
            depth = df['Depth (mm)']
            color_component = column_name

            ax.plot(color_data, depth, color = color_component.lower())

            #set graphical parameters for each subplot
            ax.set_title(color_component, fontweight='bold',pad = 10)
            ax = self.setCustomTicks(ax,20,4,4,2)
            ax.grid(axis = 'both',visible=True)
            ax.set_xlim(0,100)
            ax.invert_yaxis()
        
        #add title to figure 
        self.addFigureTitle(df = df)

        #adding headings for the entire ColoursGraph figure
        self.axes_left.set_ylabel('Depth (mm)',fontweight = 'bold')
        self.axes_center.set_xlabel('Intensity (%)',fontweight = 'bold')



    def getAnalysisType(self,df:pd.DataFrame):
        """
        Function which returns the column names of the colour data to be plotted. 
        The list is order according to what is rendered on the GUI. This function can 
        later be used to handle and setup CEILAB analysis. 

        parameters:
            df(pd.Dataframe): pandas dataframe containing the data to be plotted.
        """
        df_columns = df.columns
        if 'Blue' in df_columns and 'Red' in df_columns and 'Green' in df_columns:
            return ['Red',"Green",'Blue']
        else:
            return None


    def setCustomTicks(self,ax:matplotlib.axes.Axes,y_axis_nbins:int,x_axis_nbins:int,y_axis_nminor:int,x_axis_nminor:int):
        """
        Function to setup the ticks on the axis of the ColoursGraph Plot.

        parameters:
            ax(matplotlib.axes.Axes): the axes object of a matplotlib subfigure which newly set ticks will be placed on.
            y_axis_nbins(int): the number of bins / major ticks on the y axis of the ColoursGraph
            x_axis_nbins(int): the number of bins / major ticks on the x axis of the ColoursGraph
            y_axis_nminor(int) the number of minor ticks to sit between the major ticks on the y axis of the ColoursGraph
            x_axis_nminor(int): the number of minor ticks to sit between the major ticks on the x axis of the ColoursGraph
        """
        ax.yaxis.set_major_locator(MaxNLocator(nbins=y_axis_nbins))
        ax.xaxis.set_major_locator(MaxNLocator(nbins=x_axis_nbins))

        ax.yaxis.set_minor_locator(AutoMinorLocator(y_axis_nminor))
        ax.xaxis.set_minor_locator(AutoMinorLocator(x_axis_nminor))


        ax.tick_params(axis='x', which='both', top=True, labeltop=False)
        ax.tick_params(axis='y', which='both', right=True, labelright=False)

        ax.tick_params(which='minor', length=2, color='grey')
        ax.tick_params(which='major', length=4, color='grey')

        ax.yaxis.minorticks_on()
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
            columns = self.getAnalysisType(df)
            if columns == ['Red',"Green","Blue"]:
                figure_title = 'RGB Colour Space Plot'
            else:
                figure_title = 'Colour Space Plot'

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
    
    def setTopBottomCoordinates(self)->tuple:
        """
        Function called upon the resizing of the LayersGraph. 
        This function returns the coordinates for the limits of the y axis of the layers graph.
        THis function returns in normalised / relative figure coordinates (i.e. a point between 0 and 1).
        A top value of 0.5 means the top of the layers graph will be halfway up the layersgraph's matplotlib figure. 
        """
        norm_top_axis_point,norm_bottom_axis_point = self.getAxisRelativeCoordinates()
        norm_top_point, norm_bottom_point = self.getLineHeightRelativeCoordinates()
        top = min(norm_top_axis_point,norm_top_point)
        bottom = max(norm_bottom_axis_point,norm_bottom_point)
        return top,bottom 
    
    def getAxisRelativeCoordinates(self)->tuple:
        """
        Function returning the normalised/relative figure coordiantes for the top and bottom of the y axis on 
        the ColoursGraph subplots. 
        """
        y_axis_bounds = self.fig.axes[0].get_ybound()
        top_axis_point = (0,y_axis_bounds[0])
        bottom_axis_point = (0,y_axis_bounds[1])
        norm_top_axis_point = self.getNormalisedCoords(top_axis_point)[1]
        norm_bottom_axis_point = self.getNormalisedCoords(bottom_axis_point)[1]
        return norm_top_axis_point,norm_bottom_axis_point
    
    def getLineHeightRelativeCoordinates(self)->tuple:
        """
        Function that gets the height display coordinates for the first and last data points 
        on the first subplot of the ColoursGraph. This is called by Layers Graph to align the layers 
        with the ColoursGraph.
        """
        first_data_point = (self.df.iloc[0,1],self.df.iloc[0,0])
        last_data_point = (self.df.iloc[-1,1],self.df.iloc[-1,0])
        
        norm_top_point = self.getNormalisedCoords(first_data_point)[1]
        norm_bottom_point = self.getNormalisedCoords(last_data_point)[1]
        return norm_top_point, norm_bottom_point
    
    def getNormalisedCoords(self, data_point)->tuple:
        """
        Function that converts a matplotlib data coordinates into normalized figure coordinates.
        """
        # Get the figure's bounding box in display (pixel) coordinates
        bbox = self.fig.bbox
        width, height = bbox.width, bbox.height
        
        # Transform the data point to display coordinates
        data_point = self.fig.axes[0].transData.transform(data_point)
        
        # Normalize based on the figure's bounding box size
        return (data_point[0] / width, data_point[1] / height)

