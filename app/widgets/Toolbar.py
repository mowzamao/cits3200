from PyQt6.QtWidgets import QToolBar, QPushButton
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtCore import pyqtSignal
from app.widgets.ColoursGraph import ColoursGraph

class Toolbar(QToolBar):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create the controls panel with buttons for various functions."""

        self.calibrate_image = QAction("Calibrate Image", self)
        self.run_rgb = QAction("Run RGB Analysis", self)
        self.run_cielab = QAction("Run CIELAB Analysis", self)
        self.export_results = QAction("Export Results", self)
       
        self.addAction(self.calibrate_image)
        self.addAction(self.run_rgb)
        self.addAction(self.run_cielab)
        self.addAction(self.export_results)

        self.export_results.triggered.connect(self.parent().export_graphs_as_pdf)# Connect Export Results button to the export method in MainWindow
        self.run_cielab.triggered.connect(self.parent().run_ceilab_analysis)
        self.run_rgb.triggered.connect(self.parent().run_rgb_analysis)
        



    
