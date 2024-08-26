from PyQt6.QtWidgets import *

app = QApplication([])


window = QWidget()

layout = QHBoxLayout()

layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))

window.setLayout(layout)

window.resize(500,500)

app.exec()