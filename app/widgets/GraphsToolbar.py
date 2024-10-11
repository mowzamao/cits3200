from os import getcwd
from PyQt6.QtGui import QAction
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtGui import QAction, QIcon, QPixmap, QPainter
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QByteArray
from matplotlib.backends.backend_pdf import PdfPages
from app.widgets.ColoursGraph import ColoursGraph


class GraphsToolbar(NavigationToolbar):
    def __init__(self, canvas, parent):

        super().__init__(canvas, parent)  # Initialize the canvas
        
        self.canvas = canvas
        self.grid_visible = True
        self.parent = parent

        self.save_actions = [None, None, None, None]

        self.add_grid_button()
        self.add_save_buttons()
        self.add_unit_button()
        self.remove_buttons(["Subplots", "Customize", "Save"])
        self.replace_icons()

        # Connecting the canvas's motion_notify_event to an empty function
        # to remove the (x, y) = (..., ...) on the right side of the panel
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)

        self.setStyleSheet("""
                            QToolBar {
                                background-color: #f3f2f0;
                            }
                            QToolButton {
                                color: #080808;
                                background-color: #f3f2f0;
                                font-weight: 400;
                                margin: 0;
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


    def svg_to_icon(self, svg_string):
        # Convert SVG string to QByteArray
        svg_bytes = QByteArray(svg_string.encode('utf-8'))
        
        # Create an SVG renderer with the byte array
        renderer = QSvgRenderer(svg_bytes)
        
        # Create a pixmap to render the SVG
        pixmap = QPixmap(100, 100)  # You can adjust the size here
        pixmap.fill()  # Clear the pixmap with a transparent background
        
        # Render the SVG into the pixmap
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        # Return QIcon created from the rendered pixmap
        return QIcon(pixmap)


    def add_grid_button(self):
        """Creating a new action for gridlines, and adding the action to the toolbar"""

        grid_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-grid-3x3" viewBox="0 0 16 16"><rect width="100%" height="100%" fill="#f3f2f0" /> <path d="M0 1.5A1.5 1.5 0 0 1 1.5 0h13A1.5 1.5 0 0 1 16 1.5v13a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 14.5zM1.5 1a.5.5 0 0 0-.5.5V5h4V1zM5 6H1v4h4zm1 4h4V6H6zm-1 1H1v3.5a.5.5 0 0 0 .5.5H5zm1 0v4h4v-4zm5 0v4h3.5a.5.5 0 0 0 .5-.5V11zm0-1h4V6h-4zm0-5h4V1.5a.5.5 0 0 0-.5-.5H11zm-1 0V1H6v4z"/></svg>"""
        self.grid_action = QAction("Toggle Grid", self, icon = self.svg_to_icon(grid_svg))
        self.insertAction(self.actions()[6], self.grid_action)
        self.grid_action.triggered.connect(self.toggle_grid)

    def add_save_buttons(self):
        csv_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-filetype-csv" viewBox="0 0 16 16"><rect width="100%" height="100%" fill="#f3f2f0" /> <path fill-rule="evenodd" d="M14 4.5V14a2 2 0 0 1-2 2h-1v-1h1a1 1 0 0 0 1-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5zM3.517 14.841a1.13 1.13 0 0 0 .401.823q.195.162.478.252.284.091.665.091.507 0 .859-.158.354-.158.539-.44.187-.284.187-.656 0-.336-.134-.56a1 1 0 0 0-.375-.357 2 2 0 0 0-.566-.21l-.621-.144a1 1 0 0 1-.404-.176.37.37 0 0 1-.144-.299q0-.234.185-.384.188-.152.512-.152.214 0 .37.068a.6.6 0 0 1 .246.181.56.56 0 0 1 .12.258h.75a1.1 1.1 0 0 0-.2-.566 1.2 1.2 0 0 0-.5-.41 1.8 1.8 0 0 0-.78-.152q-.439 0-.776.15-.337.149-.527.421-.19.273-.19.639 0 .302.122.524.124.223.352.367.228.143.539.213l.618.144q.31.073.463.193a.39.39 0 0 1 .152.326.5.5 0 0 1-.085.29.56.56 0 0 1-.255.193q-.167.07-.413.07-.175 0-.32-.04a.8.8 0 0 1-.248-.115.58.58 0 0 1-.255-.384zM.806 13.693q0-.373.102-.633a.87.87 0 0 1 .302-.399.8.8 0 0 1 .475-.137q.225 0 .398.097a.7.7 0 0 1 .272.26.85.85 0 0 1 .12.381h.765v-.072a1.33 1.33 0 0 0-.466-.964 1.4 1.4 0 0 0-.489-.272 1.8 1.8 0 0 0-.606-.097q-.534 0-.911.223-.375.222-.572.632-.195.41-.196.979v.498q0 .568.193.976.197.407.572.626.375.217.914.217.439 0 .785-.164t.55-.454a1.27 1.27 0 0 0 .226-.674v-.076h-.764a.8.8 0 0 1-.118.363.7.7 0 0 1-.272.25.9.9 0 0 1-.401.087.85.85 0 0 1-.478-.132.83.83 0 0 1-.299-.392 1.7 1.7 0 0 1-.102-.627zm8.239 2.238h-.953l-1.338-3.999h.917l.896 3.138h.038l.888-3.138h.879z"/></svg>"""
        self.save_actions[0] = QAction(f"""Save as csv""", self, icon = self.svg_to_icon(csv_svg))
        self.save_actions[0].triggered.connect(self.export_data_to_csv)
        self.insertAction(self.actions()[10], self.save_actions[0])

        excel_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-file-earmark-spreadsheet" viewBox="0 0 16 16"><rect width="100%" height="100%" fill="#f3f2f0" /> <path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2M9.5 3A1.5 1.5 0 0 0 11 4.5h2V9H3V2a1 1 0 0 1 1-1h5.5zM3 12v-2h2v2zm0 1h2v2H4a1 1 0 0 1-1-1zm3 2v-2h3v2zm4 0v-2h3v1a1 1 0 0 1-1 1zm3-3h-3v-2h3zm-7 0v-2h3v2z"/></svg>"""
        self.save_actions[1] = QAction(f"""Save to Excel""", self, icon = self.svg_to_icon(excel_svg))
        self.save_actions[1].triggered.connect(self.export_data_to_excel)
        self.insertAction(self.actions()[11], self.save_actions[1])

        image_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-file-earmark-image" viewBox="0 0 16 16"><rect width="100%" height="100%" fill="#f3f2f0" /> <path d="M6.502 7a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3"/><path d="M14 14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zM4 1a1 1 0 0 0-1 1v10l2.224-2.224a.5.5 0 0 1 .61-.075L8 11l2.157-3.02a.5.5 0 0 1 .76-.063L13 10V4.5h-2A1.5 1.5 0 0 1 9.5 3V1z"/></svg>"""
        self.save_actions[2] = QAction(f"""Save as image""", self, icon = self.svg_to_icon(image_svg))
        self.save_actions[2].triggered.connect(self.actions()[12].trigger)
        self.insertAction(self.actions()[12], self.save_actions[2])


        pdf_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-file-earmark-pdf" viewBox="0 0 16 16"><rect width="100%" height="100%" fill="#f3f2f0" /> <path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2M9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5z"/><path d="M4.603 14.087a.8.8 0 0 1-.438-.42c-.195-.388-.13-.776.08-1.102.198-.307.526-.568.897-.787a7.7 7.7 0 0 1 1.482-.645 20 20 0 0 0 1.062-2.227 7.3 7.3 0 0 1-.43-1.295c-.086-.4-.119-.796-.046-1.136.075-.354.274-.672.65-.823.192-.077.4-.12.602-.077a.7.7 0 0 1 .477.365c.088.164.12.356.127.538.007.188-.012.396-.047.614-.084.51-.27 1.134-.52 1.794a11 11 0 0 0 .98 1.686 5.8 5.8 0 0 1 1.334.05c.364.066.734.195.96.465.12.144.193.32.2.518.007.192-.047.382-.138.563a1.04 1.04 0 0 1-.354.416.86.86 0 0 1-.51.138c-.331-.014-.654-.196-.933-.417a5.7 5.7 0 0 1-.911-.95 11.7 11.7 0 0 0-1.997.406 11.3 11.3 0 0 1-1.02 1.51c-.292.35-.609.656-.927.787a.8.8 0 0 1-.58.029m1.379-1.901q-.25.115-.459.238c-.328.194-.541.383-.647.547-.094.145-.096.25-.04.361q.016.032.026.044l.035-.012c.137-.056.355-.235.635-.572a8 8 0 0 0 .45-.606m1.64-1.33a13 13 0 0 1 1.01-.193 12 12 0 0 1-.51-.858 21 21 0 0 1-.5 1.05zm2.446.45q.226.245.435.41c.24.19.407.253.498.256a.1.1 0 0 0 .07-.015.3.3 0 0 0 .094-.125.44.44 0 0 0 .059-.2.1.1 0 0 0-.026-.063c-.052-.062-.2-.152-.518-.209a4 4 0 0 0-.612-.053zM8.078 7.8a7 7 0 0 0 .2-.828q.046-.282.038-.465a.6.6 0 0 0-.032-.198.5.5 0 0 0-.145.04c-.087.035-.158.106-.196.283-.04.192-.03.469.046.822q.036.167.09.346z"/></svg>"""
        self.save_actions[3] = QAction(f"""Save as pdf""", self, icon = self.svg_to_icon(pdf_svg))
        self.save_actions[3].triggered.connect(self.export_graphs_as_pdf)
        self.insertAction(self.actions()[13], self.save_actions[3])


    def replace_icons(self):
        home_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-arrow-counterclockwise" viewBox="0 0 16 16"><rect width="100%" height="100%" fill="#f3f2f0" /><path fill-rule="evenodd" d="M8 3a5 5 0 1 1-4.546 2.914.5.5 0 0 0-.908-.417A6 6 0 1 0 8 2z"/><path d="M8 4.466V.534a.25.25 0 0 0-.41-.192L5.23 2.308a.25.25 0 0 0 0 .384l2.36 1.966A.25.25 0 0 0 8 4.466"/></svg>"""
        self.actions()[0].setIcon(self.svg_to_icon(home_svg))
        
        back_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-caret-left-fill" viewBox="0 0 16 16"><rect width="100%" height="100%" fill="#f3f2f0" /><path d="m3.86 8.753 5.482 4.796c.646.566 1.658.106 1.658-.753V3.204a1 1 0 0 0-1.659-.753l-5.48 4.796a1 1 0 0 0 0 1.506z"/></svg>"""
        self.actions()[1].setIcon(self.svg_to_icon(back_svg))

        forward_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-caret-right-fill" viewBox="0 0 16 16"><rect width="100%" height="100%" fill="#f3f2f0" /><path d="m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z"/></svg>"""
        self.actions()[2].setIcon(self.svg_to_icon(forward_svg))

        pan_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-arrows-expand" viewBox="0 0 16 16"><rect width="100%" height="100%" fill="#f3f2f0" /><path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13A.5.5 0 0 1 1 8M7.646.146a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 1.707V5.5a.5.5 0 0 1-1 0V1.707L6.354 2.854a.5.5 0 1 1-.708-.708zM8 10a.5.5 0 0 1 .5.5v3.793l1.146-1.147a.5.5 0 0 1 .708.708l-2 2a.5.5 0 0 1-.708 0l-2-2a.5.5 0 0 1 .708-.708L7.5 14.293V10.5A.5.5 0 0 1 8 10"/></svg>"""
        self.actions()[4].setIcon(self.svg_to_icon(pan_svg))

        zoom_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-zoom-in" viewBox="0 0 16 16"><rect width="100%" height="100%" fill="#f3f2f0" /><path fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11M13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0"/><path d="M10.344 11.742q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1 6.5 6.5 0 0 1-1.398 1.4z"/><path fill-rule="evenodd" d="M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5"/></svg>"""
        self.actions()[5].setIcon(self.svg_to_icon(zoom_svg))


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

    def add_unit_button(self):
        
        icon = QIcon.fromTheme(f"{getcwd()}/app/style/grid.svg")

        self.unit_action = QAction('Change Units',self,icon = icon)

        self.insertAction(self.actions()[6],self.unit_action)


        self.unit_action.triggered.connect(self.toggle_units)
    
    def toggle_units(self):
        self.parent.graphs.colours_graph.units = self.getNewUnit(self.parent.graphs.colours_graph.units)
        self.parent.graphs.colours_graph.clearSubplots()
        self.parent.graphs.colours_graph.plotColourData()
        self.parent.graphs.colours_graph.draw_idle()

    def getNewUnit(self, unit):
        return {'%': '.', '.': '%'}.get(unit, '')
    
    def on_mouse_move(self, event):
        # We do not need to display anything on mouse movement
        pass  # Simply do nothing on mouse movement

    def set_message(self, s):
        # Override to do nothing, effectively preventing any message display
        pass  # No operation, so no text will be shown
