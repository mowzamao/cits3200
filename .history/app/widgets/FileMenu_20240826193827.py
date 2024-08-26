from PyQt6.QtWidgets import QWidget, QFileDialog, QMenuBar, QMenu
from PyQt6.QtGui import QPixmap, QAction  
from PyQt6.QtCore import Qt

class FileMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create a menu to select image files"""
        file_menu = self.create_file_menu()
        settings_menu = self.create_settings_menu()
        help_menu = self.create_help_menu()

        self.addMenu(file_menu) 
        self.addMenu(settings_menu) 
        self.addMenu(help_menu) 

        self._createMenuBar()


    def create_file_menu(self):
        """Create the File menu and add actions."""
        file_menu = QMenu("File")
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)

        open_action.triggered.connect(self.open_image)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        return file_menu

    def create_settings_menu(self):
        """Create the Settings menu and add actions."""
        settings_menu = QMenu("Settings")
        adjust_params_action = QAction("Adjust Parameters", self)
        calibration_action = QAction("Calibration", self)

        settings_menu.addAction(adjust_params_action)
        settings_menu.addAction(calibration_action)

        return settings_menu

    def create_help_menu(self):
        """Create the Help menu and add actions."""
        help_menu = self.menuBar().addMenu("Help")
        user_guide_action = QAction("User Guide", self)
        about_action = QAction("About", self)

        help_menu.addAction(user_guide_action)
        help_menu.addAction(about_action)

        return help_menu


    # def open_image(self):
    #     """Open an image file and display it in the image_label."""
    #     file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")

    #     if file_name:
    #         pixmap = QPixmap(file_name)
    #         self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
    #         self.status_bar.showMessage(f"Loaded image: {file_name}")
