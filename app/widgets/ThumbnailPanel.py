import sys
from PyQt6.QtWidgets import QApplication, QWidget, QStatusBar, QGridLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from app.widgets.Thumbnail import Thumbnail

class ThumbnailPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.count = 0
        self.max_count = 14
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        self.setGeometry(0, 0, 400, 300)  # Initial size of the main window

    def add_thumbnail(self, thumbnail):
        if self.count <= self.max_count:
            self.layout.addWidget(thumbnail, 0, self.count, 3, 1)
            self.count += 1
    
