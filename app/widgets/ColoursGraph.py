
#import matplotlib and set backend configuration for pyqt compatability
import matplotlib
matplotlib.use('QtAgg')

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
            width(int) - Inches: The width of the matplotlib figure. 
            height(int) - Inches: The height of the matplot figure. 
            dpi(int) - Dots Per Inch: matplotlib resolution settings. 
            df(pd.Dataframe): A Pandas Dataframe containing the data to be displayed. 
        """    
        
        #Defining the top-end matplotlib figure 
        fig = Figure(figsize=(width, height), dpi=dpi)

        # Drawing three subplots, one for each colour channel
        self.axes_left = fig.add_subplot(131)
        self.axes_center = fig.add_subplot(132)
        self.axes_right = fig.add_subplot(133)

        # Calling the initialsation function of ColourGraph's parent class FigureCanvasQTAGG and passing in 
        #matplotlib's Figure class to specify the parameters of the plots
        super(ColoursGraph, self).__init__(fig)

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

