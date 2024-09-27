from PyQt6.QtWidgets import QToolBar, QPushButton
from PyQt6.QtGui import QPixmap, QAction  

class Toolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create the controls panel with buttons for various functions."""

        self.calibrate_image = QAction("Calibrate Image", self)
        self.run_rgb = QAction("Run RGB Analysis", self)
        self.rub_cielab = QAction("Run CIELAB Analysis", self)
        self.export_results = QAction("Export Results", self)
       
        self.addAction(self.calibrate_image)
        self.addAction(self.run_rgb)
        self.addAction(self.rub_cielab)
        self.addAction(self.export_results)
        self.export_results.triggered.connect(self.parent().export_graphs_as_pdf)# Connect Export Results button to the export method in MainWindow



    
