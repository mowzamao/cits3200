from PyQt6.QtWidgets import QWidget,  QHBoxLayout
from PyQt6.QtCore import Qt
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from app.utils.RandomDataGenerator import RandomDataGenerator 

class MplCanvas(FigureCanvasQTAgg):
    """A class that enables Matplotlib plots to be imbedded into a pyqt context 
    """

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        # Drawing three subplots, one for each colour channel
        self.axes_left = fig.add_subplot(131)
        self.axes_center = fig.add_subplot(132)
        self.axes_right = fig.add_subplot(133)
        super(MplCanvas, self).__init__(fig)

class GraphPanel(QWidget):
    """The pyqt class that defines the panel containing the colour graphs
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):

        #### Testing with random data #####
        source = RandomDataGenerator()
        df = source.get_random_dataset()
        ###################################

        layout = QHBoxLayout()
        graph = MplCanvas(self, width=5, height=5, dpi=100)
           
        # Red channel
        graph.axes_left.set_title('Red')
        graph.axes_left.plot(round(100*df['Red']/255,  4), df['Depth'],  color='red')
        graph.axes_left.grid(axis = 'y')
        graph.axes_left.invert_yaxis()
        graph.axes_left.set_ylabel('Depth (m)')
        graph.axes_left.set_xlim(0, 100)

        # Green channel
        graph.axes_center.set_title('Green')
        graph.axes_center.plot(round(100*df['Green']/255,  4), df['Depth'],  color='green')
        graph.axes_center.grid(axis = 'y')
        graph.axes_center.invert_yaxis()
        graph.axes_center.set_xlabel('Intensity (%)')
        graph.axes_center.set_xlim(0, 100)

        # Blue channel
        graph.axes_right.set_title('Blue')
        graph.axes_right.plot(round(100*df['Blue']/255,  4), df['Depth'],  color='blue')
        graph.axes_right.grid(axis = 'y')
        graph.axes_right.invert_yaxis()
        graph.axes_right.set_xlim(0, 100)

        layout.addWidget(graph)  
        self.setLayout(layout)