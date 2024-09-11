from PyQt6.QtWidgets import QWidget, QLabel

class ImagePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create a core image display panel"""
        """Create and return the QLabel for displaying the sediment core image."""
        image_label = QLabel("Sediment core image will be displayed here.")
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("border: 2px solid black; color: black; background-color: white;")
        return image_label