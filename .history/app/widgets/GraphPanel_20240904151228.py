from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from app.utils.RandomDataGenerator import RandomDataGenerator 


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=3, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class GraphPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        source = RandomDataGenerator()
        df = source.get_random_dataset()

        layout = QHBoxLayout()

        graph = MplCanvas(self, width=3, height=5, dpi=100)
        graph.setStyleSheet("border: 1px solid black; color: black; background-color: white;")
        
        graph.axes.plot(round(100*df['Red']/255,  4), df['Depth'],  color='red')
        graph.axes.plot(round(100*df['Green']/255,  4) + 100, df['Depth'],  color='green')        
        graph.axes.plot(round(100*df['Blue']/255,  4) + 200, df['Depth'],  color='blue')

        graph.axes.invert_yaxis()
        graph.axes.axvline(100)
        graph.axes.set_xlabel('Intensity (%)')
        graph.axes.set_ylabel('Depth (m)')

        layout.addWidget(graph)    

            
        self.setLayout(layout)