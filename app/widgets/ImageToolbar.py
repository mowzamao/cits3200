from os import getcwd
from PyQt6.QtWidgets import QToolBar, QPushButton
from PyQt6.QtGui import QPixmap, QAction,QTransform, QIcon

class ImageToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create the controls panel for images."""

      # Fullscreen button for toggling view
        icon = QIcon.fromTheme(f"{getcwd()}/app/style/rotate.svg")

        self.rotate = QAction("Rotate Image", self, icon=icon)
        self.rotate.triggered.connect(self.rotate_image)
        self.addAction(self.rotate)

    def rotate_image(self):
        transform = QTransform().rotate(180) 
        img = self.parent().image
        if img != None:
            img_flipped = img.transformed(transform)
            self.parent().set_image(img_flipped)
    
