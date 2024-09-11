from PyQt6.QtWidgets import QWidget,  QHBoxLayout
from PyQt6.QtCore import Qt
from app.widgets.Plots import ColoursGraph

class GraphPanel(QWidget):
    """The pyqt class that defines the panel containing the colour graphs
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):

        layout = QHBoxLayout()
        plots = ColoursGraph(self, width=5, height=5, dpi=100)

        layout.addWidget(plots)  
        self.setLayout(layout)