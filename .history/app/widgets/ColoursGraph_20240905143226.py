import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from app.utils.RandomDataGenerator import RandomDataGenerator 

class ColoursGraph(FigureCanvasQTAgg):
    """A wrapper class for Matplotlib RGB or cielab plots"""

    def __init__(self, parent=None, width=5, height=5, dpi=100):    
        #### Testing with random data #####
        source = RandomDataGenerator()
        df = source.get_random_dataset()
        ###################################
        
        fig = Figure(figsize=(width, height), dpi=dpi)

        # Drawing three subplots, one for each colour channel
        self.axes_left = fig.add_subplot(131)
        self.axes_center = fig.add_subplot(132)
        self.axes_right = fig.add_subplot(133)
        super(Plots, self).__init__(fig)

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

