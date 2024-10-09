from os import getcwd
from PyQt6.QtGui import QAction
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtGui import QAction, QIcon


class GraphsToolbar(NavigationToolbar):
    def __init__(self, canvas, parent):

        super().__init__(canvas, parent)  # Initialize the canvas
        
        self.grid_visible = True

        self.save_actions = [None, None, None, None]

        self.add_grid_button()
        self.add_save_buttons()
        self.remove_buttons(["Subplots", "Customize", "Save"])

        self.setStyleSheet("""
                            QToolBar {
                                background-color: #f3f2f0;
                            }
                            QToolButton {
                                color: #080808;
                                background-color: #f3f2f0;
                                font-weight: 400;
                            }
                            QToolButton:hover {
                                color: white;
                                background-color: #8a4c57;
                           }
                           """
                           )


    def remove_buttons(self, labels):
        """Removes buttons from the toolbar by their labels."""
        for action in self.actions():
            if action.text() in labels:
                self.removeAction(action)

    def add_grid_button(self):
        """Creating a new action for gridlines, and adding the action to the toolbar"""
        icon = QIcon.fromTheme(f"{getcwd()}/app/style/grid.svg")
        self.grid_action = QAction("Toggle Grid", self, icon = icon)

        self.insertAction(self.actions()[6], self.grid_action)
        self.grid_action.triggered.connect(self.toggle_grid)

    def add_save_buttons(self):
        save_formats = ["csv","excel" ,"image", "pdf"]
        for index, format in enumerate(save_formats):
            icon = QIcon.fromTheme(f"""{getcwd()}/app/style/{format}.svg""")
            self.save_actions[index] = QAction(f"""Save as {format}""", self, icon = icon)
            self.insertAction(self.actions()[11+index], self.save_actions[index])


    def toggle_grid(self):
        """Toggle the gridlines on the plot.""" 
        self.grid_visible = not self.grid_visible
        for ax in self.canvas.figure.get_axes():
            ax.grid(axis = 'both', visible = self.grid_visible)
        self.canvas.draw_idle()  


