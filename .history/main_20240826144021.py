from PyQt6.QtWidgets import *

app = QApplication([])


window = QWidget()

layout = QHBoxLayout()

label = QLabel('Hello World!')
label.show()


app.exec()