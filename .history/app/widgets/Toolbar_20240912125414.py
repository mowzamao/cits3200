from PyQt6.QtWidgets import QToolBar, QPushButton
from PyQt6.QtGui import QPixmap, QAction  

class Toolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create the controls panel with buttons for various functions."""

        self.greyscale = QAction("Convert to Greyscale", self)
        self.analyze_rgb = QAction("RGB Analysis", self)
        self.detect_perimeter = QAction("Perimeter Detection", self)
        self.set_calibration = QAction("Set Calibration Points", self)
        self.export_data = QAction("Export Results", self)
        self.plot_rgb_graph = QAction("Plot RGB Graph", self)
        self.plot_greyscale = QAction("Plot Greyscale Intensity", self)
       
        self.addAction(self.greyscale)
        self.addAction(self.analyze_rgb)
        self.addAction(self.detect_perimeter)
        self.addAction(self.set_calibration)
        self.addAction(self.export_data)
        self.addAction(self.plot_rgb_graph)
        self.addAction(self.greyscale)

        self.setStyleSheet(self.get_style())

    def get_style(self):
        """Returns the CSS style for buttons."""
        return open('./app/style/buttons.css').read() 
    


    
