from PyQt6.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from app.widgets.Graphs import Graphs
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from app.widgets.ColoursGraph import ColoursGraph
from app.widgets.LayersGraph import LayersGraph
from app.widgets.GraphsToolbar import GraphsToolbar

class GraphPanel(QWidget):
    """
    The PyQt class that defines the panel showing the colour graphs
    """
    
    def __init__(self, parent=None, df=None, image=None):
        """
        The initialization function for the GraphPanel class/PyQt widget.
        """
        super().__init__(parent)
        self.df = df  # Store the dataframe directly
        self.image = image
        self.layout = QVBoxLayout(self)  # Create a layout for the GraphPanel
        self.init_empty()


    def init_empty(self):
        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("border: 1px solid lightgrey; background-color: white;")
        
        # Set the layout
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


    def init_ui(self):
        """
        Function to generate and define plots for the GraphPanel Widget.
        """
        # Clear existing layout and refresh the graph
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)  # Remove old widget

        # Ensure the dataframe (df) is used to generate the graphs
        if self.df is not None:
            self.graphs = Graphs(df=self.df)  # Pass the dataframe to the graph widget
        else:
            print("No dataframe provided. Please upload and process an image.")
        
        self.toolbar = GraphsToolbar(self.graphs.colours_graph, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.graphs)

    def switch_graph_fullscreen(self):
        """
        Toggles between fullscreen and normal mode by hiding or showing the image panel.
        """
        parent_window = self.parent().parent()
        image_panel = parent_window.image_panel
        image_panel.setVisible(not image_panel.isVisible())
