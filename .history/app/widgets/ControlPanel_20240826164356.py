from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create the controls panel with buttons for various functions."""
        self.layout = QHBoxLayout()
        button_style = self.get_button_style()

        grayscale_button = self.create_button("Convert to Grayscale", button_style)
        rgb_analysis_button = self.create_button("RGB Analysis", button_style)
        perimeter_detection_button = self.create_button("Perimeter Detection", button_style)
        set_calibration_button = self.create_button("Set Calibration Points", button_style)
        export_data_button = self.create_button("Export Results", button_style)
        plot_rgb_graph_button = self.create_button("Plot RGB Graph", button_style)
        plot_greyscale_button = self.create_button("Plot Greyscale Intensity", button_style)

        self.addWidget(grayscale_button)
        self.addWidget(rgb_analysis_button)
        self.addWidget(perimeter_detection_button)
        self.addWidget(set_calibration_button)
        self.addWidget(export_data_button)
        self.addWidget(plot_rgb_graph_button)
        self.addWidget(plot_greyscale_button)