from PyQt6.QtWidgets import QWidget, QFileDialog, QMenuBar, QMenu
from PyQt6.QtGui import QPixmap, QAction  
from PyQt6.QtCore import Qt
import cv2 as cv
import numpy as np
from app.utils.ImageTransforming import *   
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
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)

        open_action.triggered.connect(self.open_image)
        save_action.triggered.connect(self.save_image)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
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

    """Opens, formats, and displays an image. It handles the user input for selecting an image file, processes the image with the formatting functions, and then displays it in the application."""
    def open_image(self):
        """Open an image file amd display it in the ImagePanel."""
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

                self.parent.graph_panel.init()

                # Format the image
                oriented_image = orient_array(image)
                red, green, blue = img_rgb_array(oriented_image, is_BGR=True)
                
                # Convert back to displayable format using QPixmap
                display_image = QPixmap(file_name)
                self.parent.image_panel.set_image(display_image)

                self.parent.statusBar().showMessage(f"Loaded and formatted image: {file_name}")
            else:
                self.parent.statusBar().showMessage("Failed to load image.")

    """Saves the currently displayed image to a user-specified location. It handles user input for selecting a save location, converts the image to a format that can be saved, and then saves it using OpenCV."""
    def save_image(self):
        """Prompt for an output location to save the formatted image."""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "Images (*.png *.jpg *.bmp)"
        )

        if file_name:
            # Assuming the image is already processed and saved in self.image
            oriented_image = self.parent.image_panel.image_label.pixmap().toImage()
            if not oriented_image.isNull():
                # Convert QImage to OpenCV image for saving
                buffer = oriented_image.constBits().asstring(
                    oriented_image.width() * oriented_image.height() * oriented_image.depth() // 8
                )
                image = np.frombuffer(buffer, np.uint8).reshape(
                    (oriented_image.height(), oriented_image.width(), oriented_image.depth() // 8)
                )

                # Save the image
                cv.imwrite(file_name, image)
                self.parent.statusBar().showMessage(f"Image saved to: {file_name}")
            else:
                self.parent.statusBar().showMessage("No image available to save.")


