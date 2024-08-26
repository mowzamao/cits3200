import sys
from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow

def main():
    """The initial entry point of the application. 
        Creates root window.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()