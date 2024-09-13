from PyQt6.QtWidgets import QWidget,  QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap, QIcon, QColor
from PyQt6.QtCore import Qt, QSize

from app.utils.RandomDataGenerator import RandomDataGenerator 
from app.widgets.ColoursGraph import ColoursGraph
from app.widgets.LayersGraph import LayersGraph

class Graphs(QWidget):
    """The pyqt class that defines the panel containing the colour graphs
    """
    def __init__(self, parent=None, df = df):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):

        layout = QHBoxLayout()
        
        colours_graph = ColoursGraph(self, width=5, height=5, dpi=100, df = df)
        layers_graph  = LayersGraph(self, width=20, height=20, dpi=100, df = df)

        layout.addWidget(layers_graph,stretch=2)  
        layout.addWidget(colours_graph, stretch=8)  
        self.setLayout(layout)