from PyQt6.QtWidgets import QToolBar, QPushButton
from PyQt6.QtGui import QPixmap, QAction  

class Toolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create the controls panel with buttons for various functions."""

        self.grayscale = QAction("Convert to Grayscale", self)
        self.analyze_rgb = QAction("RGB Analysis", self)
        self.detect_perimeter = QAction("Perimeter Detection", self)
       
        self.addAction(self.grayscale)
        self.addAction(self.analyze_rgb)
        self.addAction(self.detect_perimeter)
       
       
        # set_calibration_button = self.create_button("Set Calibration Points", button_style)
        # export_data_button = self.create_button("Export Results", button_style)
        # plot_rgb_graph_button = self.create_button("Plot RGB Graph", button_style)
        # plot_greyscale_button = self.create_button("Plot Greyscale Intensity", button_style)

        # layout.addWidget(grayscale_button)
        # layout.addWidget(rgb_analysis_button)
        # layout.addWidget(perimeter_detection_button)
        # layout.addWidget(set_calibration_button)
        # layout.addWidget(export_data_button)
        # layout.addWidget(plot_rgb_graph_button)
        # layout.addWidget(plot_greyscale_button)

        # self.setLayout(layout)

        self.setStyleSheet("""
            QToolBar {
                background-color: #333;
                padding: 5px;
            }
            QToolButton {
                background-color: #444;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
            QToolButton:hover {
                background-color: #555;
                border: 1px solid #666;
            }
            QToolButton:pressed {
                background-color: #222;
                border: 1px solid #444;
            }
            QToolButton:checked {
                background-color: #222;
                border: 1px solid #777;
            }"""


    def get_button_style(self):
        """Return the CSS style for buttons."""
        return """
            QPushButton {
                background-color: #0078d4;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0C4F83;
            }
        """
    

    def create_button(self, text, style):
        """Create and return a QPushButton with the given text and style."""
        button = QPushButton(text)
        button.setStyleSheet(style)
        return button