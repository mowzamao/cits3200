from PyQt6.QtWidgets import QMainWindow, QApplication
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
        self.setFixedSize(QApplication.instance().primaryScreen().size())
        self.setWindowTitle("Core Colour Toolkit")
        self.setCentralWidget(CustomWidget())


