from PyQt6.QtWidgets import QMainWindow
from app.widgets.CustomWidget import CustomWidget

class MainWindow(QMainWindow):
    """ A class defining the structure and actions of the outermost window in the application
        Args:
            QMainWindow (): A child class of QtWidgets that inherits from QWidget.
    """
    def __init__(self, screen_size):
        """ Args:
            screen_size: A PyQt6.QtCore.QSize() object holding the screen length and width
        """
        super().__init__()
        self.init_ui(screen_size)

    def init_ui(self, screen_size):
        """Initialises the user interface
        """
        self.setWindowTitle("Core Colour Toolkit")
        self.setCentralWidget(CustomWidget())

        width, height = self.get_screen_size()
        self.size = screen_size


    def get_screen_size(self):
        """Returns the current viewport's width and height in pixels
        """
        return [800, 600]