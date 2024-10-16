# nuitka-project: --onefile
# nuitka-project: --output-filename=sediment_analysis
# nuitka-project: --remove-output
# nuitka-project: --mingw64
# nuitka-project: --enable-plugins=pyqt6
# nuitka-project: --include-data-dir=app/style=app/style

import sys
from PyQt6.QtWidgets import QApplication
from app.widgets.MainWindow import MainWindow

def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()