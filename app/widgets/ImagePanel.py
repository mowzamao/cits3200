from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QImage, QTransform, QPainter, QColor
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
        self.image_label.setStyleSheet("border: 20px solid white; background-color: white;")
        self.toolbar = ImageToolbar(self)
        
        # Set the layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 7, 5, 3)
        self.layout.setSpacing(5)   

        self.layout.addWidget(self.image_label)

        self.setLayout(self.layout)
    
    def set_image(self, pixmap):
        """Set the given QPixmap on the image label."""
        self.image = pixmap
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
        self.layout.insertWidget(0, self.toolbar)

    def draw_box(self, x: int, y: int, width: int, height: int):
        rect = QRect(x, y, width, height)
        painter = QPainter(self.image)
        painter.setPen(QColor(255, 0, 0, 127))
        painter.drawRect(rect)
        painter.end()