from os import getcwd
from PyQt6.QtGui import QAction
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtGui import QAction, QIcon


class GraphsToolbar(NavigationToolbar):
    def __init__(self, canvas, parent):

        super().__init__(canvas, parent)  # Initialize the canvas
        
        self.grid_visible = True
        self.parent = parent

        self._add_grid_button()
        self._add_unit_button()
        self._remove_buttons(["Subplots", "Customize"])

        self.setStyleSheet("""
                            QToolBar {
                                background-color: #f3f2f0;
                                padding: 7px;
                            }
                            QToolButton {
                                color: #080808;
                                background-color: #f3f2f0;
                                border-radius: 5px;
                                padding: 10px;
                                font-weight: 400;
                            }
                            QToolButton:hover {
                                color: white;
                                background-color: #8a4c57;
                           }
                           """
                           )


    def _remove_buttons(self, labels):
        """
        Removes buttons from the toolbar by their labels.
        """
        for action in self.actions():
            if action.text() in labels:
                self.removeAction(action)

    def _add_grid_button(self):
        """
        Add a custom button to toggle gridlines
        """
        # Create a new action for gridlines
        icon = QIcon.fromTheme(f"{getcwd()}/app/style/grid.svg")

        self.grid_action = QAction("Toggle Grid", self, icon = icon)

        # Add the action to the toolbar
        self.insertAction(self.actions()[5], self.grid_action)

        # Connect the action to a function that toggles gridlines
        self.grid_action.triggered.connect(self._toggle_grid)

    def _toggle_grid(self):
        """
        Toggle the gridlines on the plot.
        """ 
        self.grid_visible = not self.grid_visible

        for ax in self.canvas.figure.get_axes():
            ax.grid(axis = 'both', visible = self.grid_visible)

        self.canvas.draw_idle()  # Redraw the canvas

    def _add_unit_button(self):
        
        icon = QIcon.fromTheme(f"{getcwd()}/app/style/grid.svg")

        self.unit_action = QAction('Chnage Units',self,icon = icon)

        self.insertAction(self.actions()[6],self.unit_action)

        self.unit_action.triggered.connect(self._toggle_units)
    
    def _toggle_units(self):
        self.parent.graphs.colours_graph.units = self.getNewUnit(self.parent.graphs.colours_graph.units)
        self.parent.graphs.colours_graph.clearSubplots()
        self.parent.graphs.colours_graph.plotColourData()
        self.parent.graphs.colours_graph.draw_idle()

    def getNewUnit(self, unit):
        return {'%': '.', '.': '%'}.get(unit, '')


