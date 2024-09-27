from PyQt6.QtWidgets import QToolBar, QPushButton
from PyQt6.QtGui import QPixmap, QAction  

class Toolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create the controls panel with buttons for various functions."""

        self.calibrate_image = QAction("Calibrate Image", self)
        self.run_rbg = QAction("Run RGB Analysis", self)
        self.rub_cielab = QAction("Run CIELAB Analysis", self)
        self.export_results = QAction("Export Results", self)
       
        self.addAction(self.calibrate_image)
        self.addAction(self.self.run_rbg)
        self.addAction(self.calibrate_image)
        self.addAction(self.calibrate_image)


    
