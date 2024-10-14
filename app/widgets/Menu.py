from PyQt6.QtWidgets import QWidget, QFileDialog, QMenuBar, QMenu, QMessageBox
from PyQt6.QtGui import QPixmap, QAction  
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
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
        file_action = self.create_file_action()
        help_menu = self.create_help_menu()

        self.addAction(file_action) 
        self.addMenu(help_menu) 


    def create_file_action(self):
        """Create the File actions."""
        file_action = QAction("File", self)
        file_action .triggered.connect(self.open_image)
        return file_action 

    def create_help_menu(self):
        """Create the Help menu and add actions."""
        help_menu =  QMenu("Help", self)
        user_guide_action = QAction("User Guide", self)
        about_action = QAction("About", self)

        user_guide_action.triggered.connect(self.open_user_guide)
        user_guide_action.triggered.connect(self.open_about)



        help_menu.addAction(user_guide_action)
        help_menu.addAction(about_action)

        return help_menu
    
    def open_user_guide(self):
        """Open the user guide in the default web browser."""
        # Replace with the actual URL where the user guide is hosted
        url = "https://docs.google.com/document/d/1Ut9xIydCe57XhlXjVJ60JIHLIcsG98q0NrMVG0WW0_U/edit?usp=sharing"  # Use the actual URL

        # Open the URL in the default browser
        QDesktopServices.openUrl(QUrl(url))

    def open_about(self):
        """Open the user guide in the default web browser."""
        # Replace with the actual URL where the user guide is hosted
        url = "https://github.com/mowzamao/cits3200"  # Use the actual URL

        # Open the URL in the default browser
        QDesktopServices.openUrl(QUrl(url))

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
                display_image = QPixmap(file_name)

                # Process the core image to get the data (df)
                data_dict = process_core_image(oriented_image, 77)  # Use 77mm as core width

                #checking image has been correctly processed
                if type(data_dict) != dict:
                    self.analysis_fail_popup()
                    return
                
                #setting up dataframe for the colours graph
                rgb_df = data_dict['Colours']
                lab_df = core_to_lab(rgb_df)
                df = pd.merge(rgb_df,lab_df,on = 'Depth (mm)')

                if data_dict != 0:
                    image = data_dict["Image"]
                    
                    # Call the MainWindow method to add the image and its graph
                    self.parent.add_image_and_graph_panel(file_name, df, image)
    
    def analysis_fail_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle('Analysis Failure')
        msg.setText('Core not detected in image.')
        msg.exec()

