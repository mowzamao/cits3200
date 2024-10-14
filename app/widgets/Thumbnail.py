import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QDialog, QPushButton, QVBoxLayout, QStackedLayout, QGridLayout
from PyQt6.QtGui import QPixmap, QFontMetrics, QPixmap, QTransform
from PyQt6.QtCore import Qt

class Thumbnail(QFrame):
    def __init__(self, image_path=None, main_window=None):
        super().__init__()

        self.image_path = image_path
        self.main_window = main_window  # Reference to the main window to send panel updates
        self.indicator = None  # Indicator for "Left" or "Right"

        # Set up the layout (Vertical stacking: indicator, image, and name)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)   
        self.setLayout(self.layout)

        # Top element: Left/Right indicator
        self.indicator_label = QLabel(self)
        self.indicator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.indicator_label.setStyleSheet("")

        # Middle element: Image display
        self.image = QLabel(self)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setStyleSheet("border: none; padding: 5px; margin: 0;  background-color: rgba(255, 255, 255, 150);")

        # Bottom element: Image name
        self.caption = QLabel(self)
        self.caption.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add widgets to the layout in order
        self.layout.addWidget(self.indicator_label, 0,0,1,200)  # First: Indicator
        self.layout.addWidget(self.image, 0, 0, 200, 500)  # Second: Image
        self.layout.addWidget(self.caption, 200, 0, 1, 500)  # Third: Caption

        # Caption setup
        name = image_path.split("/")[-1].split(".")[0] if image_path else image_path
        font_metrics = QFontMetrics(self.caption.font())
        elided_name = font_metrics.elidedText(name, Qt.TextElideMode.ElideLeft, self.image.width())
        self.caption.setText(elided_name)

        # Set the style for the frame
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 150);
                border: 4px solid rgba(255, 255, 255, 150); 
                padding: 0;
                margin: 2px;    
            }
        """)

        # Load the image
        self.load_image()      

    def load_image(self):
        pixmap = QPixmap(self.image_path)

        # Rotating pixmap 90 degrees if it is taller than it is wide
        if pixmap.height() > pixmap.width():
            # Create a transformation object
            transform = QTransform()
            # Rotate the pixmap by 90 degrees
            transform.rotate(90)
            # Apply the transformation and return the rotated pixmap
            pixmap = pixmap.transformed(transform)

        self.image.resize(100, 200)
        self.image.setPixmap(pixmap.scaled(self.image.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def set_indicator(self, panel_side=None):
        """Set or clear the indicator for this thumbnail."""

        if panel_side == "left":
            self.indicator = "left"
            self.indicator_label.setText("Left")
            self.indicator_label.setStyleSheet("border: none; padding: 0; margin: 0; font-size: 12px; font-weight: 500; color: white;  background-color: #8a4c57;")
            self.indicator_label.raise_()

        elif panel_side == "right":
            self.indicator = "right"
            self.indicator_label.setText("Right")
            self.indicator_label.setStyleSheet("border: none; padding: 0; margin: 0;  font-size: 12px; font-weight: 500; color: white;  background-color: #8a4c57;")
            self.indicator_label.raise_()

        else:
            self.reset_indicator()  # If no side is passed, reset the indicator
            self.indicator_label.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
            self.indicator_label.lower()

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
        dialog.resize(200, 80) 
        dialog.setWindowTitle("Select panel to display:")
        layout = QGridLayout()

        left_button = QPushButton("Left graph")
        right_button = QPushButton("Right graph")
        single_analysis_button = QPushButton("Image and graph")  # New button

        layout.addWidget(left_button, 0, 0, 1, 1)
        layout.addWidget(right_button, 0, 1, 1, 1)
        layout.addWidget(single_analysis_button, 1, 0, 1, 0)  # Add the third button

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
