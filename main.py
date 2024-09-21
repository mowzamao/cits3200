# nuitka-project: --onefile
# nuitka-project: --plugin-enable=pyqt6

import sys
from PyQt5.QtWidgets import QApplication
from app.widgets.MainWindow import MainWindow

def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
