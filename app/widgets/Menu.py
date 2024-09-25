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
        export_csv_action = QAction("Export as CSV", self)  # New action for CSV export
        export_excel_action = QAction("Export to Excel", self)  # New action for Excel export
        exit_action = QAction("Exit", self)

        open_action.triggered.connect(self.open_image)
        export_csv_action.triggered.connect(self.parent.export_data_to_csv)  # Link to export function
        export_excel_action.triggered.connect(self.parent.export_data_to_excel)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addAction(export_csv_action)  # Add CSV export option to the menu
        file_menu.addAction(export_excel_action)
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
        """Open an image file and display it in the ImagePanel."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Image", 
            "", 
            "Images (*.png *.jpg *.bmp)"
        )
    
        if file_name:
            # Load the image using OpenCV
            image = cv.imread(file_name)

            if image is not None:
                # Format the image and display it in ImagePanel
                oriented_image = orient_array(image)
                display_image = QPixmap(file_name)
                self.parent.image_panel.set_image(display_image)

                # Process the core image to get the data (df)
                data_dict = process_core_image(oriented_image, 77, True)  # Use 77mm as core width

                if data_dict != 0:  # If processing is successful
                    self.parent.graph_panel.df = data_dict["Colours"]  # Set the dataframe for the GraphPanel
                    self.parent.graph_panel.init_ui()  # Reinitialize the graphs with the new data
                
                    self.parent.statusBar().showMessage(f"Loaded and processed image: {file_name}")
            else:
                self.parent.statusBar().showMessage("Failed to load image.")

   
