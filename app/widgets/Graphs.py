from PyQt6.QtWidgets import QWidget,  QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap, QIcon, QColor
from PyQt6.QtCore import Qt, QSize

from app.utils.RandomDataGenerator import RandomDataGenerator 
from app.widgets.ColoursGraph import ColoursGraph
from app.widgets.LayersGraph import LayersGraph

class Graphs(QWidget):
    """The pyqt class that defines the panel containing the colour graphs
    """
    def __init__(self, parent=None, df = None):
        super().__init__(parent)
        self.df = df
        #generate instances of the sediment graphs
        self.colours_graph = ColoursGraph(self,dpi=100, df = self.df)
        self.layers_graph  = LayersGraph(self, dpi=100, df = self.df)
        self.init_ui(self.colours_graph,self.layers_graph)

    def init_ui(self,colours_graph,layers_graph):
        #create layout for colour graph
        colours_layout = QHBoxLayout()
        colours_layout.addWidget(colours_graph)

        #create layout for layers graph
        layers_layout = QHBoxLayout()
        layers_layout.addWidget(layers_graph)

        #create main layout of Graphs panel
        main_layout = QHBoxLayout()
        main_layout.addLayout(layers_layout,stretch=2)
        main_layout.addLayout(colours_layout,stretch=8)


        #Set the layout of this instance of the Graph Panel
        self.setLayout(main_layout)