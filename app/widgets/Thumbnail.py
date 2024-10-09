import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtGui import QPixmap, QFont, QFontMetrics
from PyQt6.QtCore import Qt

class Thumbnail(QFrame):
    def __init__(self, image_path = None):
        super().__init__()
    
        self.image_path = image_path
        self.is_left = False
        self.is_right = False
        
        # Set up the layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.image = QLabel(self)
        self.caption = QLabel(self)

        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)    
        self.caption.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.image, stretch = 5)
        self.layout.addWidget(self.caption, stretch = 1)


        #Setting up the caption
        self.caption.setWordWrap(False)  # Disable word wrapping
        self.caption.setStyleSheet("color: black; font-weight: bold; padding: 5px;")

        # Converting the image_path to the image name for the caption
        try:
            name = image_path.split("/")[-1]
            try:
                name = name.split(".")[0]
            except:
                name = name
        except:
            name = image_path

        # Ensuring caption text doesn't flow out of bounds
        font_metrics = QFontMetrics(self.caption.font())
        elided_name = font_metrics.elidedText(name, Qt.TextElideMode.ElideLeft, self.image.width()) 
        self.caption.setText(elided_name)


        # Setting the style
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

        # Loading the image
        self.load_image()
        

    def load_image(self):
        # Loading the image and resizing it to thumbnail size
        pixmap = QPixmap(self.image_path)
        self.image.resize(100, 200)     
        self.image.setPixmap(pixmap.scaled(self.image.size(), Qt.AspectRatioMode.KeepAspectRatio))


    def mousePressEvent(self, event):
        # Check if the mouse click is within the widget
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.is_left:
                self.setStyleSheet("""QFrame {background-color: lightblue;}""")
                self.is_left = True
            else:
                self.setStyleSheet("""QFrame {background-color: rgba(255, 255, 255, 150);}""")
                self.is_left = False