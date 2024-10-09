
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

    def __init__(self, parent:classmethod=None, dpi:int=100, df:pd.DataFrame = None,analysis_type:str = 'rgb',units:str = '%'):
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
        self.analysis_type = analysis_type
        self.hline = None
        self.units = units 
        self.fig = Figure(dpi=dpi)
        self.createSubplots()
        self.plotColourData()
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        self.fig.canvas.mpl_connect('resize_event',self.resizeEvent) #connecting resize event to graph
        super(ColoursGraph, self).__init__(self.fig)
    
    def createSubplots(self):
        """
        Defining three subplots, one for each colour channel
        """
        self.axes_left = self.fig.add_subplot(131)
        self.axes_center = self.fig.add_subplot(132, sharex=self.axes_left, sharey=self.axes_left)
        self.axes_right = self.fig.add_subplot(133, sharex=self.axes_left, sharey=self.axes_left)

    def clearSubplots(self):
        """
        Function to clear the data from all axes in the Colours Plot. 
        """
        for ax in self.fig.axes:
            ax.cla()
    
    def plotColourData(self):
        """
        Function which iterative plots data from an inputted pandas dataframe onto three subplots.

        parameters:
            df(pd.Dataframe): the pandas dataframe with the colour data to be plotted
        """
        depth,colour_data_list,colour_name_list,plot_line_colour_list = self.getPlotData()

        for ax, colour_data,colour_name,plot_line_colour in zip(self.fig.axes,colour_data_list,colour_name_list,plot_line_colour_list):

            ax.plot(colour_data, depth,color = plot_line_colour)

            ax.set_title(colour_name, fontweight='bold',pad = 10)

            ax = self.setCustomTicks(ax,20,4,4,2)

            ax.grid(axis = 'both',visible=True)

            ax = self.setPlotXlim(ax)

            ax.invert_yaxis()
        
        #add title to figure 
        self.addFigureTitle()

        #adding headings for the entire ColoursGraph figure
        self.axes_left.set_ylabel('Depth (mm)',fontweight = 'bold')
        self.setPlotXlabel()

    def setPlotXlabel(self):
        """
        Function setting xlabel for the x-axis of the Colours Plot. 
        """
        if self.analysis_type == 'rgb' and self.units == '%':
            xlabel_str = 'Intensity (%)'
        elif self.analysis_type == 'rgb' and self.units == '.':
            xlabel_str = ' RGB Colour Values'
        elif self.analysis_type == 'lab' and self.units == '%':
            xlabel_str = 'Intensity (%)'
        elif self.analysis_type == 'lab' and self.units == '.':
            xlabel_str = 'CIELAB Values'
        else:
            xlabel_str = ''
        self.axes_center.set_xlabel(xlabel_str,fontweight = 'bold')

    def setPlotXlim(self,ax):
        """
        Function setting limit for x values on the x axis. 
        """
        if self.analysis_type == '%':
            ax.set_xlim(0,100)
            return ax
        else:
            ax.autoscale(True,axis='x')
            return ax

    def getPlotData(self):
        """
        Function preparing data to be plotted in the Colours Graph.

        Returns:
            depth(pd.Series): depth of sample from geological core for row of data.
            colour_data_list(list[pd.Series]): list of pd.Series objects containing the data for each colour channel of analysis.
            colour_name_list(list[str]): the name of each colour channel in the analysis - used as headings for the colours graph subplots.
            plot_line_colour_list(list[str]): a list of strings passed to plt.plot to set the colour of the lines on the plot.
        """
        if self.analysis_type == 'rgb':
            depth = self.df['Depth (mm)']
            colour_name_list = ['Red',"Green",'Blue']
            colour_data_list = [self.setDataUnits(self.df[colour_name]) for colour_name in colour_name_list]
            plot_line_colour_list = ['r',"g",'b']
        if self.analysis_type =='lab':
            depth = self.df['Depth (mm)']
            colour_name_list = ['L*',"A*",'B*']
            colour_data_list = [self.df['L']]
            for data in [self.setDataUnits(self.df[colour_name],colour_name) for colour_name in ['a','b']]:
                colour_data_list.append(data)
            plot_line_colour_list = ['b','b','b']
        return depth,colour_data_list,colour_name_list,plot_line_colour_list
    
    def setDataUnits(self,data:pd.Series,colour_name:str = None)->pd.Series:
        if self.analysis_type =='rgb' and self.units == '%':
            return round(100*data/255,4)
        elif self.analysis_type =='lab' and self.units == '%' and (colour_name =='a' or colour_name == 'b'):
            return round(100*(data + 128)/255,4)
        else:
            return data

    def getColumnNames(self,analysis_type:str):
        """
        Function which returns the column names of the colour data to be plotted. 
        The list is order according to what is rendered on the GUI. This function can 
        later be used to handle and setup CEILAB analysis. 

        parameters:
            analysis_type(str): a string either 'rgb' or 'lab' indicating the analysis to be done. 
        """
        if analysis_type == 'rgb':
            return ['Red',"Green",'Blue']
        elif analysis_type == 'lab':
            return ['L','a','b']
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
        

    def addFigureTitle(self,figure_title:str=None,fontsize:int = 16):
        """
        Add a title to the Colours Plot based of the type on analysis being visualised. 
        """
        if self.analysis_type == 'rgb':
            figure_title = 'RGB Colour Space Plot'
        elif self.analysis_type == 'lab':
            figure_title = 'CIELAB Colour Space Plot'
        else:
            figure_title = ''
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
        Function returning normalised display coordinates for the hight of the edge of the y-axis.
        """
        lower_y_coords = self.fig.axes[0].get_ybound()[0]
        upper_y_coords = self.fig.axes[0].get_ybound()[1]
        norm_lower_y_coords = self.getNormalisedCoords((0,lower_y_coords))[1]
        norm_upper_y_coords = self.getNormalisedCoords((0,upper_y_coords))[1]
        return norm_upper_y_coords,norm_lower_y_coords
    
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
    
    def onClick(self, event):
        """
        Function which adds a grey line onto the Colours Graphs subplots when 
        they are clicked on.
        """
        if event.inaxes is None:
            # Click occurred outside any axes
            return
        if self.hline is None:
            # No line exists; create it
            ydata = event.ydata
            self.hline = []
            for ax in self.fig.axes:
                line = ax.axhline(y=ydata, color='grey',alpha = 0.5)
                self.hline.append(line)
        else:
            # Line exists; remove it
            for line in self.hline:
                line.remove()
            self.hline = None
        self.fig.canvas.draw_idle()

