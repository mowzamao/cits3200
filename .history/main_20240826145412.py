from PyQt6.QtWidgets import *

app = QApplication([])

main_window = QMainWindow()
main_layout = QHBoxLayout()

left_window = QWidget()
right_window = QWidget()


main_layout.addWidget(left_window)
main_layout.addWidget(right_window)

main_window.setLayout(main_layout)

main_window.show()
app.exec()