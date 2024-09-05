import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class LayersGraph(FigureCanvasQTAgg):
    """A wrapper class for a Matplotlib plot of the sediment layers"""

    def __init__(self, parent=None, width=5, height=5, dpi=100, df = None):    
        
        fig = Figure(figsize=(width, height), dpi=dpi)

        # Drawing three subplots, one for each colour channel
        self.axes_left = fig.add_subplot(131)
        self.axes_center = fig.add_subplot(132)
        self.axes_right = fig.add_subplot(133)
        super(LayersGraph, self).__init__(fig)

        # Red channel
        self.axes_left.set_title('Red')
        self.axes_left.plot(round(100*df['Red']/255,  4), df['Depth'],  color='red')
        self.axes_left.grid(axis = 'y')
        self.axes_left.invert_yaxis()
        self.axes_left.set_ylabel('Depth (m)')
        self.axes_left.set_xlim(0, 100)


