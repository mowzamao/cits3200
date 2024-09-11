from PyQt6.QtWidgets import QWidget,  QHBoxLayout
from PyQt6.QtCore import Qt

from app.utils.RandomDataGenerator import RandomDataGenerator 
from app.widgets.ColoursGraph import ColoursGraph
from app.widgets.LayersGraph import LayersGraph

class GraphPanel(QWidget):
    """The pyqt class that defines the panel containing the colour graphs
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):

        ####### Testing with random data, remove for MVP ######
        source = RandomDataGenerator()
        df = source.get_random_dataset()
        ######################################################

        layout = QHBoxLayout()
        colours_graph = ColoursGraph(self, width=5, height=5, dpi=100, df = df)
        layers_graph  = LayersGraph(self, width=5, height=5, dpi=100, df = df)

        layout.addWidget(layers_graph)  
        layout.addWidget(colours_graph)  
        self.setLayout(layout)