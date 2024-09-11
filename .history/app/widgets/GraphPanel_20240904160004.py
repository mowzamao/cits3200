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

        channels = ["Red", "Green", "Blue"]
        graph = MplCanvas(self, width=4, height=5, dpi=100)
        for i, colour in enumerate(channels):
            graph.setStyleSheet("border: 1px solid black; color: black; background-color: white;")
            graph.axes.plot(round(100*df[colour]/255,  4), df['Depth'],  color=colour.lower())
            
            graph.axes.grid(axis = 'y')

            graph.axes.invert_yaxis()
            graph.axes.set_xlabel('Intensity (%)')
            graph.axes.set_xlim(0, 100)

            if i == 0:
                graph.axes.set_title('Red')
                graph.axes.set_ylabel('Depth (m)')
            if i == 1:
                graph.axes.set_title('Green')
            if i == 2:
                graph.axes.set_title('Blue')

            layout.addWidget(graph)  
            
        self.setLayout(layout)