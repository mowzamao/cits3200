import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QDialog, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPixmap, QFontMetrics
from PyQt6.QtCore import Qt

class Thumbnail(QFrame):
    def __init__(self, image_path=None, main_window=None):
        super().__init__()

        self.image_path = image_path
        self.main_window = main_window  # Reference to the main window to send panel updates
        self.indicator = None  # Indicator for "Left" or "Right"

        # Set up the layout (Vertical stacking: indicator, image, and name)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Top element: Left/Right indicator
        self.indicator_label = QLabel(self)
        self.indicator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.indicator_label.setStyleSheet("font-weight: bold; color: black; padding: 5px;")

        # Middle element: Image display
        self.image = QLabel(self)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Bottom element: Image name
        self.caption = QLabel(self)
        self.caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.caption.setStyleSheet("font-weight: bold; color: black; padding: 5px;")

        # Add widgets to the layout in order
        self.layout.addWidget(self.indicator_label)  # First: Indicator
        self.layout.addWidget(self.image, stretch=5)  # Second: Image
        self.layout.addWidget(self.caption, stretch=1)  # Third: Caption

        # Caption setup
        name = image_path.split("/")[-1].split(".")[0] if image_path else image_path
        font_metrics = QFontMetrics(self.caption.font())
        elided_name = font_metrics.elidedText(name, Qt.TextElideMode.ElideLeft, self.image.width())
        self.caption.setText(elided_name)

        # Set the style for the frame
        self.setStyleSheet("""
        QFrame {
            background-color: rgba(255, 255, 255, 150);
            border-radius: 0px;
        }
        QFrame:hover {
            background-color: lightgray;
        }
        QLabel {
            font-size: 14px;
            color: black;
        }
        """)

        # Load the image
        self.load_image()

    def load_image(self):
        pixmap = QPixmap(self.image_path)
        self.image.resize(100, 200)
        self.image.setPixmap(pixmap.scaled(self.image.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def set_indicator(self, panel_side=None):
        """Set or clear the indicator for this thumbnail."""
        if panel_side == "left":
            self.indicator = "left"
            self.indicator_label.setText("Left")
        elif panel_side == "right":
            self.indicator = "right"
            self.indicator_label.setText("Right")
        else:
            self.reset_indicator()  # If no side is passed, reset the indicator

    def reset_indicator(self):
        """Clear the indicator for this thumbnail."""
        self.indicator = None
        self.indicator_label.setText("")  # Clear the displayed indicator

    def mousePressEvent(self, event):
        """Open a dialog when the thumbnail is clicked."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.show_panel_selection_dialog()

    def show_panel_selection_dialog(self):
        """Show the dialog to choose Left, Right, or Single Image Analysis panel."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Panel")
        layout = QVBoxLayout()

        label = QLabel("Select a panel to display:")
        layout.addWidget(label)

        left_button = QPushButton("Left Panel")
        right_button = QPushButton("Right Panel")
        single_analysis_button = QPushButton("Single Image Analysis")  # New button

        layout.addWidget(left_button)
        layout.addWidget(right_button)
        layout.addWidget(single_analysis_button)  # Add the third button

        left_button.clicked.connect(lambda: self.select_panel("left", dialog))
        right_button.clicked.connect(lambda: self.select_panel("right", dialog))
        single_analysis_button.clicked.connect(lambda: self.select_panel("single", dialog))  # Handle single image analysis

        dialog.setLayout(layout)
        dialog.exec()


    def select_panel(self, panel_side, dialog):
        """Update the graph panel based on the selected side (left or right)."""
        if self.main_window:
            self.main_window.update_graph_panel(self.image_path, panel_side)
            self.set_indicator(panel_side)  # Update the indicator on the thumbnail

        dialog.accept()  # Close the dialog
