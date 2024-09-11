from PyQt6.QtWidgets import QMainWindow
from app.widgets.CustomWidget import CustomWidget

class MainWindow(QMainWindow):
    """ A class defining the structure and actions of the outermost window in the application
        
        Args:
            QMainWindow (): A child class of QtWidgets that inherits from QWidget.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('My PyQt App')
        self.setCentralWidget(CustomWidget())
        self.resize(800, 600)