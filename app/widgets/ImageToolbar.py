from os import getcwd
from PyQt6.QtWidgets import QApplication, QToolBar, QPushButton, QInputDialog, QLineEdit
from PyQt6.QtGui import QPixmap, QAction,QTransform, QIcon
from app.widgets.GraphPanel import GraphPanel
import numpy as np
from app.utils.ProcessSedimentCore import process_core_image

class ImageToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create the controls panel for images."""

      # Fullscreen button for toggling view
        iconRotate = QIcon.fromTheme(f"{getcwd()}/app/style/rotate.svg")
        self.rotate = QAction("Rotate Image", self, icon=iconRotate)
        self.rotate.triggered.connect(self.rotate_image)
        self.addAction(self.rotate)

      # Prompt dialog button for user to input sediment core width manually
        iconChangeWidth = QIcon.fromTheme("edit-find")
        self.core_width = QAction("Change Length Measurement", self, icon=iconChangeWidth)
        self.core_width.triggered.connect(self.change_width_measurement)
        self.addAction(self.core_width)

    def rotate_image(self):

        # Flipping the image in the image panel
        transform = QTransform().rotate(180) 
        img = self.parent().image
        if img != None:
            img_flipped = img.transformed(transform)
            self.parent().set_image(img_flipped)

            # Inverting the dataframe and re-showing the graphs
            graph_panel = self.parent().parent().findChild(GraphPanel)
            
            max_depth = max(graph_panel.df['Depth (mm)'])
            new_depths = graph_panel.df['Depth (mm)'].apply(lambda x: max_depth - x)
            
            graph_panel.df['Depth (mm)'] = new_depths
            graph_panel.init_ui()
    
    def change_width_measurement(self):
        """
        Creates PyQt6 QInputDialog to prompt user for width of sediment core, then reloads graph display with the new width
        """
        image_data = self.parent().parent().parent().graph_panel.image
        if not image_data is None:
            text, ok = QInputDialog.getText(self, "Sediment Core Analysis", "Please input the width of the core in the image (in mm):")
            if ok:
                if text and text.isdigit():
                    new_data = process_core_image(image_data, int(text), True)
                    if new_data != 0:
                        self.parent().parent().parent().graph_panel.df = new_data["Colours"]
                        self.parent().parent().parent().graph_panel.init_ui()
                else:
                    self.parent().parent().parent().statusBar().showMessage(f"Input '{text}' is not a number")
        else:
            self.parent().parent().parent().statusBar().showMessage("No image opened")