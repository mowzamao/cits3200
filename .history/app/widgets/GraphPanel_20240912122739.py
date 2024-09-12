from PyQt6.QtWidgets import QWidget,  QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap, QIcon, QColor
from PyQt6.QtCore import Qt, QSize

from app.utils.RandomDataGenerator import RandomDataGenerator 
from app.widgets.Graphs import Graphs

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


        layout = QVBoxLayout()

        graphs = Graphs(df = df)
        

        temp_pixmap = QPixmap(25, 25)
        temp_pixmap.fill(QColor("red"))
        fullscreen_icon = QIcon("./app/style/fullscreen.svg")
        fullscreen_icon_size = fullscreen_icon.actualSize(QSize(50,50))
        fullscreen_button = QPushButton(self, icon = fullscreen_icon)
        fullscreen_button.clicked.connect(self.switch_graph_fullscreen)
        fullscreen_button.setFixedSize(fullscreen_icon_size)
        fullscreen_button.move(fullscreen_button.geometry().bottomRight())

        layout.addWidget(fullscreen_button,Qt.AlignmentFlag(1))
        layout.addWidget(graphs)  
        self.setLayout(layout)

    def switch_graph_fullscreen(self):
        self.parent().parent().image_panel.setVisible(not self.parent().parent().image_panel.isVisible)