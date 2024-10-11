from PyQt6.QtWidgets import QWidget,  QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap, QIcon, QColor
from PyQt6.QtCore import Qt, QSize

from app.utils.RandomDataGenerator import RandomDataGenerator 
from app.widgets.ColoursGraph import ColoursGraph
from app.widgets.LayersGraph import LayersGraph
from app.widgets.Toolbar import Toolbar

class Graphs(QWidget):
    """The pyqt class that defines the panel containing the colour graphs
    """
    def __init__(self, parent=None, df = None):
        super().__init__(parent)
        self.df = df

        #generate instances of the sediment graphs
        self.colours_graph = ColoursGraph(self,dpi=60, df = self.df)
        self.layers_graph  = LayersGraph(self, dpi=60, df = self.df)
        
        self.layers_graph.layers_axes.sharey(self.colours_graph.axes_left)
        self.init_ui()

    def init_ui(self):
        #create layout for colour graph
        colours_layout = QHBoxLayout()
        colours_layout.addWidget(self.colours_graph)

        #create layout for layers graph
        layers_layout = QHBoxLayout()
        layers_layout.addWidget(self.layers_graph)

        #create main layout of Graphs panel
        main_layout = QHBoxLayout()
        main_layout.addLayout(layers_layout,stretch=2)
        main_layout.addLayout(colours_layout,stretch=8)

        #Set the layout of this instance of the Graph Panel
        main_layout.setContentsMargins(3, 5, 5, 3)
        main_layout.setSpacing(3)   
        self.setLayout(main_layout)