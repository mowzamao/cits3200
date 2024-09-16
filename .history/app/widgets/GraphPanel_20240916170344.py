
#importing classes for PyQT formatting 
from PyQt6.QtWidgets import QWidget,  QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap, QIcon, QColor
from PyQt6.QtCore import Qt, QSize

import app.utils.ProcessSedimentCore
from app.utils.RandomDataGenerator import *
from app.widgets.Graphs import Graphs

class GraphPanel(QWidget):
    """
    The PyQt class that defines the panel showing the colour graphs

    Parameters:
        QWidget(Class): A base/parent class making GraphPanel a PyQT widget.
    """

    def __init__(self, parent=None):
        """
        The initialisation function for the GraphPanel class/PyQt widget.

        Parameters:
            parent(Class): paramater to optionally add a base/parent class upon initialisation. 
        """

        #Initialise instance of the GraphPanel class by using the QWidget initialisation function
        super().__init__(parent)

        #Create and set the graphs for this instance of the GraphPanel class
        self.init_ui()

    def init_ui(self, img = []):
        """
        Function to generate and define plots for the GraphPanel Widget.
        """


        if len(img) == 0: 
            source = RandomDataGenerator()
            df = source.get_random_dataset()
        else:
            data_dict = process_core_image(img, 77, True)
            print("Here!!!!!", data_dict)
            df = data_dict["Colours"]


        layout = QVBoxLayout()
        
        fullscreen_icon = QIcon("./app/style/fullscreen.svg")
        fullscreen_icon_size = fullscreen_icon.actualSize(QSize(20,20))
        fullscreen_button = QPushButton(self, icon = fullscreen_icon)
        fullscreen_button.clicked.connect(self.switch_graph_fullscreen)
        fullscreen_button.setFixedSize(fullscreen_icon_size)
        fullscreen_button.move(fullscreen_button.geometry().bottomRight())

        layout.addWidget(fullscreen_button,Qt.AlignmentFlag(1))
        
        graphs = Graphs(df = df)
        layout.addWidget(graphs)  

        self.setLayout(layout)

    def switch_graph_fullscreen(self):
        self.parent().parent().image_panel.setVisible(not self.parent().parent().image_panel.isVisible)