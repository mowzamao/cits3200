from PyQt6.QtWidgets import QWidget,  QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
import matplotlib
matplotlib.use('QtAgg')

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from app.utils.RandomDataGenerator import RandomDataGenerator 


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes_left = fig.add_subplot(131)
        self.axes_center = fig.add_subplot(132)
        self.axes_right = fig.add_subplot(133)
        super(MplCanvas, self).__init__(fig)

class GraphPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        source = RandomDataGenerator()
        df = source.get_random_dataset()

        layout = QHBoxLayout()

        graph = MplCanvas(self, width=4, height=5, dpi=100)
           
        graph.axes_left.setStyleSheet("border: 1px solid black; color: black; background-color: white;")
        graph.axes_left.plot(round(100*df[colour]/255,  4), df['Depth'],  color=colour.lower())
        graph.axes_left.grid(axis = 'y')

        graph.axes_left.invert_yaxis()
        graph.axes_left.set_xlabel('Intensity (%)')
        graph.axes_left.set_xlim(0, 100)

        # if i == 0:
        #     graph.axes.set_title('Red')
        #     graph.axes.set_ylabel('Depth (m)')
        # if i == 1:
        #     graph.axes.set_title('Green')
        # if i == 2:
        #     graph.axes.set_title('Blue')

        layout.addWidget(graph)  
            
        self.setLayout(layout)