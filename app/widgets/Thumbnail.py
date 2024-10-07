import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class Thumbnail(QWidget):
    def __init__(self, image_path = None):
        super().__init__()
        
        self.image_path = image_path
        
        # Set up the layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Create and set the image label
        self.image_label = QLabel(self)

        self.layout.addWidget(self.image_label)

        # Load the image
        self.load_image()

    def load_image(self):
        # Load the image and resize it to thumbnail size
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))