import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QDialog, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPixmap, QFontMetrics
from PyQt6.QtCore import Qt

class Thumbnail(QFrame):
    def __init__(self, image_path=None, main_window=None):
        super().__init__()

        self.image_path = image_path
        self.main_window = main_window  # Reference to the main window to send panel updates
        self.is_left = False
        self.is_right = False

        # Set up the layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.image = QLabel(self)
        self.caption = QLabel(self)

        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.caption.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.image, stretch=5)
        self.layout.addWidget(self.caption, stretch=1)

        # Setting up the caption
        self.caption.setWordWrap(False)
        self.caption.setStyleSheet("color: black; font-weight: bold; padding: 5px;")

        # Caption setup
        try:
            name = image_path.split("/")[-1]
            try:
                name = name.split(".")[0]
            except:
                name = name
        except:
            name = image_path

        font_metrics = QFontMetrics(self.caption.font())
        elided_name = font_metrics.elidedText(name, Qt.TextElideMode.ElideLeft, self.image.width())
        self.caption.setText(elided_name)

        # Set the style
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

    def mousePressEvent(self, event):
        # Open the dialog when thumbnail is clicked
        if event.button() == Qt.MouseButton.LeftButton:
            self.show_panel_selection_dialog()

    def show_panel_selection_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Panel")
        layout = QVBoxLayout()

        label = QLabel("Select a panel to display the graph:")
        layout.addWidget(label)

        left_button = QPushButton("Left Panel")
        right_button = QPushButton("Right Panel")

        layout.addWidget(left_button)
        layout.addWidget(right_button)

        left_button.clicked.connect(lambda: self.select_panel("left", dialog))
        right_button.clicked.connect(lambda: self.select_panel("right", dialog))

        dialog.setLayout(layout)
        dialog.exec()

    def select_panel(self, panel_side, dialog):
        if self.main_window:
            # Notify main window to update the corresponding panel
            self.main_window.update_graph_panel(self.image_path, panel_side)
    
        dialog.accept()  # Close the dialog

