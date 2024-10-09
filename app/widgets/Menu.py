from PyQt6.QtWidgets import QWidget, QFileDialog, QMenuBar, QMenu
from PyQt6.QtGui import QPixmap, QAction  
from PyQt6.QtCore import Qt
import cv2 as cv
import numpy as np
from app.utils.ImageTransforming import * 
from app.utils.ProcessSedimentCore import *   
from app.widgets.GraphPanel import GraphPanel

class Menu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Create a menu to select image files"""
        file_menu = self.create_file_menu()
        settings_menu = self.create_settings_menu()
        help_menu = self.create_help_menu()

        self.addMenu(file_menu) 
        self.addMenu(settings_menu) 
        self.addMenu(help_menu) 


    def create_file_menu(self):
        """Create the File menu and add actions."""
        file_menu = QMenu("File", self)
        open_action = QAction("Open", self)
        exit_action = QAction("Exit", self)

        open_action.triggered.connect(self.open_image)
        exit_action.triggered.connect(self.parent.close)

        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        return file_menu

    def create_settings_menu(self):
        """Create the Settings menu and add actions."""
        settings_menu = QMenu("Settings", self)
        adjust_params_action = QAction("Adjust Parameters", self)
        calibration_action = QAction("Calibration", self)

        settings_menu.addAction(adjust_params_action)
        settings_menu.addAction(calibration_action)

        return settings_menu

    def create_help_menu(self):
        """Create the Help menu and add actions."""
        help_menu =  QMenu("Help", self)
        user_guide_action = QAction("User Guide", self)
        about_action = QAction("About", self)

        help_menu.addAction(user_guide_action)
        help_menu.addAction(about_action)

        return help_menu

    def open_image(self):
        """Open an image file and process it to display the image and its corresponding graph."""
        # Open a file dialog to select an image file
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Image", 
            "", 
            "Images (*.png *.jpg *.bmp)"
        )

        if file_name:
            # Read the image using OpenCV
            image = cv.imread(file_name)

            if image is not None:
                # Process the image (assuming orient_array and process_core_image are your utility functions)
                oriented_image = orient_array(image)

                # Assuming process_core_image returns a data dictionary with color data
                data_dict = process_core_image(oriented_image, 77)  # Example core width 77mm

                if data_dict != 0:
                    df = data_dict["Colours"]  # Assuming the processed data is in 'Colours'

                    # Call the MainWindow method to add the image and its graph
                    self.parent.add_image_and_graph_panel(file_name, df)

                    # Optionally, show a success message in the status bar
                    self.parent.statusBar().showMessage(f"Loaded and processed image: {file_name}")
                else:
                    # Handle processing failure
                    self.parent.statusBar().showMessage("Failed to process the image.")
            else:
                # Handle case where the image could not be read
                self.parent.statusBar().showMessage("Failed to load the image.")