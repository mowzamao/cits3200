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
        self.set_calibration = QAction("Set Calibration Points", self)
        self.export_data = QAction("Export Results", self)
        self.plot_rgb_graph = QAction("Plot RGB Graph", self)
        self.plot_greyscale = QAction("Plot Greyscale Intensity", self)
       
        self.addAction(self.grayscale)
        self.addAction(self.analyze_rgb)
        self.addAction(self.detect_perimeter)
       
        # plot_greyscale_button = self.create_button("Plot Greyscale Intensity", button_style)

        # layout.addWidget(grayscale_button)
        # layout.addWidget(rgb_analysis_button)
        # layout.addWidget(perimeter_detection_button)
        # layout.addWidget(set_calibration_button)
        # layout.addWidget(export_data_button)
        # layout.addWidget(plot_rgb_graph_button)
        # layout.addWidget(plot_greyscale_button)

        # self.setLayout(layout)

        self.setStyleSheet(self.get_style())

    def get_style(self):
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
    


        #    """
        #     QToolBar {
        #         background-color: #333;
        #         padding: 5px;
        #     }
        #     QToolButton {
        #         background-color: #444;
        #         color: white;
        #         border: 1px solid #555;
        #         border-radius: 5px;
        #         padding: 5px;
        #     }
        #     QToolButton:hover {
        #         background-color: #555;
        #         border: 1px solid #666;
        #     }
        #     QToolButton:pressed {
        #         background-color: #222;
        #         border: 1px solid #444;
        #     }
        #     QToolButton:checked {
        #         background-color: #222;
        #         border: 1px solid #777;
        #     }""")

    
