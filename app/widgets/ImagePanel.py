from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from app.widgets.ImageToolbar import ImageToolbar

class ImagePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = None
        self.init_ui()

    def init_ui(self):
        """Create a core image display panel"""
        """Create and return the QLabel for displaying the sediment core image."""
        # Initialize the QLabel
        self.image_label = QLabel("Sediment core image will be displayed here.")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black; color: black; background-color: white;")
        
        self.toolbar = ImageToolbar(self)
        
        # Set the layout
        layout = QVBoxLayout()

        layout.addWidget(self.toolbar)
        layout.addWidget(self.image_label)

        self.setLayout(layout)
    
    def set_image(self, pixmap):
        """Set the given QPixmap on the image label."""
        self.image = pixmap
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
        
