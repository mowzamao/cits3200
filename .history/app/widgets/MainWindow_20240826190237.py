import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QWidget, QFileDialog, QStatusBar, QMenuBar, QMenu
)
from PyQt6.QtGui import QPixmap, QAction  
from PyQt6.QtCore import Qt, QSize

from app.widgets.ImagePanel import ImagePanel
from app.widgets.ControlPanel import ControlPanel

class MainWindow(QMainWindow):
    """ A class defining the structure and actions of the outermost window in the application
        Args:
            QMainWindow (): A child class of QtWidgets that inherits from QWidget.
    """
    def __init__(self):
        """Initialize the main window and setup UI components."""
        super().__init__()

        self.set_window_properties()
        self.create_menus()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.image_panel = ImagePanel()
        self.control_panel = ControlPanel()

        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addWidget(self.image_label)


        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def set_window_properties(self):
        """Set properties for the main window."""
        self.setWindowTitle("Sediment Core Analysis Tool")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: white;")

    def create_menus(self):
        """Create the menu bar with File, Settings, and Help menus."""
        file_menu = self.create_file_menu()
        settings_menu = self.create_settings_menu()
        help_menu = self.create_help_menu()

    def create_file_menu(self):
        """Create the File menu and add actions."""
        file_menu = self.menuBar().addMenu("File")
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)

        open_action.triggered.connect(self.open_image)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

    def create_settings_menu(self):
        """Create the Settings menu and add actions."""
        settings_menu = self.menuBar().addMenu("Settings")
        adjust_params_action = QAction("Adjust Parameters", self)
        calibration_action = QAction("Calibration", self)

        settings_menu.addAction(adjust_params_action)
        settings_menu.addAction(calibration_action)

    def create_help_menu(self):
        """Create the Help menu and add actions."""
        help_menu = self.menuBar().addMenu("Help")
        user_guide_action = QAction("User Guide", self)
        about_action = QAction("About", self)

        help_menu.addAction(user_guide_action)
        help_menu.addAction(about_action)

    def create_image_display_area(self):
        """Create and return the QLabel for displaying the sediment core image."""
        image_label = QLabel("Sediment core image will be displayed here.")
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("border: 2px solid black; color: black; background-color: white;")
        return image_label

   


    def open_image(self):
        """Open an image file and display it in the image_label."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")

        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.status_bar.showMessage(f"Loaded image: {file_name}")
