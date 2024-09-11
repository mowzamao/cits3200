from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("This is a custom widget")
        layout.addWidget(label)
        self.setLayout(layout)