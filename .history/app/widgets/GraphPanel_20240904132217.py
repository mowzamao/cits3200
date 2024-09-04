from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
import matplotlib
matplotlib.use('QtAgg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class GraphPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):

        Oxygen = [ 0.1 , 0.5, 1, 10, 15, 20, 15, 10, 1, 0.5, 0.5]
        Depth  = [ 0,     1,  2,  4,  8, 10, 12, 14, 16, 20, 40 ]

        layout = QHBoxLayout()

        graph = MplCanvas(self, width=5, height=5, dpi=100)
        graph.setStyleSheet("border: 1px solid black; color: black; background-color: white;")
        graph.axes.plot(Oxygen, Depth, 'go--')


        graph.xaxis.tick_top()

        graph.set_ylabel('depth')
        graph.set_ylim(50, 0)
        graph.set_xlim(0, 25)
        graph.set_xlabel('Oxygen level [ppm]')

        
        layout.addWidget(graph)        
        self.setLayout(layout)