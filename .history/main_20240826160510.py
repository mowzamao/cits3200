import sys
from PyQt6.QtWidgets import QApplication
from app.MainWindow import MainWindow

def main():
    """The initial entry point of the application. 
        Creates root window.
    """
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    window = MainWindow(screen.size())
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()