from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
import matplotlib
matplotlib.use('QtAgg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from app.utils.RandomDataGenerator import RandomDataGenerator 


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(131)
        super(MplCanvas, self).__init__(fig)

class GraphPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        source = RandomDataGenerator()
        df = source.get_random_dataset()

        layout = QHBoxLayout()

        graph = MplCanvas(self, width=5, height=5, dpi=100)
        graph.setStyleSheet("border: 1px solid black; color: black; background-color: white;")
        
        
        graph.axes.plot(round(100*df['Red']/255, 4), df['Depth'])


        graph.axes.set_ylabel('Depth (m)')
        graph.axes.invert_yaxis()
        # graph.axes.set_ylim(50, 0)
        # graph.axes.set_xlim(0, 25)
        graph.axes.set_xlabel('Intensity (%)')

        
        layout.addWidget(graph)        
        self.setLayout(layout)