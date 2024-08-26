import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QWidget, QFileDialog, QStatusBar, QMenuBar, QMenu
)
from PyQt6.QtGui import QPixmap, QAction  
from PyQt6.QtCore import Qt, QSize

from app.widgets.MenuBar import MenuBar
from app.widgets.ImagePanel import ImagePanel
from app.widgets.ControlPanel import ControlPanel
from app.widgets.GraphPanel import GraphPanel

class MainWindow(QMainWindow):
    """ A class defining the structure and actions of the outermost window in the application
        Args:
            QMainWindow (): A child class of QtWidgets that inherits from QWidget.
    """
    def __init__(self):
        """Initialize the main window and setup UI components."""
        super().__init__()

        self.set_window_properties()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QGridLayout(self.central_widget)


        self.image_panel = ImagePanel()
        self.graph_panel = GraphPanel()
        self.control_panel = ControlPanel()
        self.menu_bar = MenuBar()


        self.main_layout.addWidget(self.control_panel, 0, 0)
        self.main_layout.addWidget(self.image_panel, 2, 1)
        self.main_layout.addWidget(self.graph_panel, 2, 2)

    def set_window_properties(self):
        """Set properties for the main window."""
        self.setWindowTitle("Sediment Core Analysis Tool")
        self.showMaximized()
        self.setStyleSheet("background-color: #eaeaea;")

 