from PyQt6.QtWidgets import QToolBar, QPushButton, QAction

class Toolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create the controls panel with buttons for various functions."""



        self.grayscale = QAction("Convert to Grayscale", self)
        rgb_analysis_button = self.create_button("RGB Analysis", button_style)
        perimeter_detection_button = self.create_button("Perimeter Detection", button_style)
        set_calibration_button = self.create_button("Set Calibration Points", button_style)
        export_data_button = self.create_button("Export Results", button_style)
        plot_rgb_graph_button = self.create_button("Plot RGB Graph", button_style)
        plot_greyscale_button = self.create_button("Plot Greyscale Intensity", button_style)

        layout.addWidget(grayscale_button)
        layout.addWidget(rgb_analysis_button)
        layout.addWidget(perimeter_detection_button)
        layout.addWidget(set_calibration_button)
        layout.addWidget(export_data_button)
        layout.addWidget(plot_rgb_graph_button)
        layout.addWidget(plot_greyscale_button)

        self.setLayout(layout)


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