from PyQt6.QtWidgets import QMainWindow
from app.widgets.custom_widget import CustomWidget

class MainWindow(QMainWindow):
    """ A class defining the outermost window in the application

    Args:
        QMainWindow (): A child class of QtWidgets that inherits from QWidget.
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My PyQt App')
        self.setCentralWidget(CustomWidget())
        self.resize(800, 600)