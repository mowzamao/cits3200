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
        """Initialises the user interface
        """
        self.setWindowTitle("Core Colour Toolkit")
        self.setCentralWidget(CustomWidget())
        self.resize(self.get_screen_size())


    def get_screen_size(self):
        return [800, 600]