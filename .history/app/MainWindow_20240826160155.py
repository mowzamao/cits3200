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
        self.setWindowTitle("Sediment Colour Toolkit")
        self.setCentralWidget(CustomWidget())

        width, height = self.get_screen_size()
        self.resize(width, height)


    def get_screen_size(self):
        """Returns the current viewport's width and height in pixels
        """
        return [800, 600]