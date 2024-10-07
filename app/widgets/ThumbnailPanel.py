import sys
from PyQt6.QtWidgets import QApplication, QWidget, QStatusBar, QGridLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from app.widgets.Thumbnail import Thumbnail

class ThumbnailPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.count = 0
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.layout.setColumnStretch(0, 1)
    

    def add_thumbnail(self, thumbnail):
        self.layout.addWidget(thumbnail, 0, self.count, 1, 1)
        self.count += 1
    
