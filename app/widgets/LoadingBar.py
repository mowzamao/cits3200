import sys
import time
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QProgressBar, QPushButton
from PyQt6.QtCore import  Qt, QTimer


class LoadingBar(QDialog):
    def __init__(self):
        self.progress = 0
        super().__init__()

        # Removing the x close button
        self.setModal(True) 

        self.setWindowTitle("Loading Image...")

        # Creating a QVBoxLayout to hold the progress bar
        layout = QVBoxLayout()
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)

        # Add the progress bar to the layout
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        # Center the modal
        self.center()
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.exec()  # Show the modal

    def step(self, value):
        for i in range(value):
            self.update_progress()

    def update_progress(self):
        if self.progress < 100:
            self.progress += 1  # Simulate progress
            self.progress_bar.setValue(self.progress)
        else:
            self.accept()  # Close the modal after loading completes

    def center(self):
        # Get the parent window's geometry
        if self.parent() is not None:
            parent_geom = self.parent().geometry()
            dialog_width = 500
            dialog_height = 500
            x = parent_geom.x() + (parent_geom.width() - dialog_width) // 2
            y = parent_geom.y() + (parent_geom.height() - dialog_height) // 2
            
            self.setGeometry(x, y, dialog_width, dialog_height)
