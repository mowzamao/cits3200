import sys
from PyQt6.QtWidgets import {QApplication}
from widgets import MainWindow

def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
