from PyQt6.QtWidgets import *

app = QApplication([])

main_window = QMainWindow(["A", "B"])

menu_bar  = QMenuBar()

main_layout = QVBoxLayout()


main_layout.addWidget(menu_bar)

main_window.setLayout(main_layout)

main_window.show()
app.exec()