from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QTransform
import numpy as np

from app.widgets.ImageToolbar import ImageToolbar

class ImagePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = None
        self.image_path = None
        self.init_ui()

    def init_ui(self):
        """Create a core image display panel"""
        """Create and return the QLabel for displaying the sediment core image."""
        # Initialize the QLabel
        self.image_label = QLabel("")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid lightgrey; background-color: white;")
        self.toolbar = ImageToolbar(self)
        
        # Set the layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.image_label)

        self.setLayout(self.layout)
    
    def set_image(self, pixmap):
        """Set the given QPixmap on the image label."""
        self.image = pixmap
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
        self.layout.insertWidget(0, self.toolbar)
