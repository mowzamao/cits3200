import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

def main():
    '''The initial entry point of the application. Creates root window.'''
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()