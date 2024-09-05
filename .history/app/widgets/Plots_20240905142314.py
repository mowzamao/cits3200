from PyQt6.QtWidgets import QWidget,  QHBoxLayout
from PyQt6.QtCore import Qt

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from app.utils.RandomDataGenerator import RandomDataGenerator 

class MplCanvas(FigureCanvasQTAgg):
    """A wrapper class for Matplotlib RGB or cielab plots 
    """

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
        super(MplCanvas, self).__init__(fig)