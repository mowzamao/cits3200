import sys
from PyQt6.QtWidgets import QApplication, QWidget, QStatusBar, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from app.widgets.Thumbnail import Thumbnail

class ThumbnailPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.count = 0
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
    

    def add_thumbnail(self, thumbnail):
        self.layout.addWidget(thumbnail, alignment=Qt.AlignmentFlag.AlignLeft)
        self.count += 1
    
