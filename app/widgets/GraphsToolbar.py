from os import getcwd
from PyQt6.QtGui import QAction
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (QFileDialog)
from matplotlib.backends.backend_pdf import PdfPages

from app.widgets.ColoursGraph import ColoursGraph



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

        # Connecting save to csv
        self.save_actions[0].triggered.connect(self.export_data_to_csv)
        self.save_actions[1].triggered.connect(self.export_data_to_excel)
        self.save_actions[2].triggered.connect(self.actions()[10].trigger)
        self.save_actions[3].triggered.connect(self.export_graphs_as_pdf)


    def toggle_grid(self):
        """Toggle the gridlines on the plot.""" 
        self.grid_visible = not self.grid_visible
        for ax in self.canvas.figure.get_axes():
            ax.grid(axis = 'both', visible = self.grid_visible)
        self.canvas.draw_idle()  


    def export_graphs_as_pdf(self):
            """Export the graphs displayed in the graph panel as a PDF file."""
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save Graphs as PDF",
                "",
                "PDF Files (*.pdf)"
            )

            if file_name:
                if not file_name.endswith('.pdf'):
                    file_name += '.pdf'

                # Assuming ColoursGraph is within the graph panel
                graphs_widget = self.parent().layout.itemAt(1).widget()
                colours_graph = graphs_widget.findChild(ColoursGraph)

                with PdfPages(file_name) as pdf:
                    if colours_graph:
                        pdf.savefig(colours_graph.fig)


    def export_data_to_csv(self):
        """Export the raw data to a CSV file."""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Raw Data as CSV",
            "",
            "CSV Files (*.csv)"
        )
        if file_name:
            if not file_name.endswith('.csv'):
                file_name += '.csv'

            df = self.parent().df
            if df is not None:
                df.to_csv(file_name, index=False)


    def export_data_to_excel(self):
        """Export the raw data to an Excel file."""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Raw Data as Excel",
            "",
            "Excel Files (*.xlsx)"
        )
        if file_name:
            if not file_name.endswith('.xlsx'):
                file_name += '.xlsx'

            df = self.parent().df
            if df is not None:
                df.to_excel(file_name, index=False)


