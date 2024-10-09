import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QGridLayout, QHBoxLayout, QWidget, QFileDialog, QScrollArea, QDialog, QPushButton, QLabel
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import pandas as pd
from time import sleep

from app.widgets.Menu import Menu
from app.widgets.ImagePanel import ImagePanel
from app.widgets.Toolbar import Toolbar
from app.widgets.GraphPanel import GraphPanel
from app.widgets.ThumbnailPanel import ThumbnailPanel
from app.widgets.Thumbnail import Thumbnail


class MainWindow(QMainWindow):
    """Main window handling the display of images and graphs, with comparison options."""
    def __init__(self):
        """Initialize the main window and setup UI components."""
        super().__init__()

        # State to track images, graphs, and thumbnails
        self.image_history = []  # Track triples of image panels, graph panels, and thumbnails
        self.num_images = 0  # The number of active images i.e. 0, 1,..., or more

        # Initialize graph panel references
        self.graph_panel_left = None  # Initialize left graph panel
        self.graph_panel_right = None  # Initialize right graph panel

        # Set window properties
        self.set_window_properties()

        # Main layout
        self.reset_central_widget()

        # Initialize toolbar and menu
        self.toolbar = Toolbar(self)
        self.menu = Menu(self)
        self.thumbnail_panel = ThumbnailPanel(self)

        # Add toolbar and menu
        self.addToolBar(self.toolbar)
        self.setMenuBar(self.menu)

        # References to panel objects
        self.image_panel = None
        self.graph_panel = None
        self.thumbnail_panel = None

        # Track the currently assigned thumbnails for the left and right panels
        self.thumbnail_left = None
        self.thumbnail_right = None

        # Render the default empty panels
        self.set_empty_panels()

    def reset_central_widget(self):
        """Reset the existing central widget."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QGridLayout()

    def add_image_and_graph_panel(self, image_path, df):
        """Handle image and graph upload."""
        image_panel = self.create_image_panel(image_path)
        graph_panel = self.create_graph_panel(df)
        thumbnail = self.create_thumbnail(image_path)

        self.image_history.append([image_panel, graph_panel, thumbnail])

        self.num_images += 1

        # Update the central widget layout with new thumbnails and panels
        self.reset_central_widget()
        self.load_panels()

    def create_image_panel(self, image_path):
        """Create an instance of the image panel."""
        image_panel = ImagePanel(self)
        pixmap = QPixmap(image_path)
        image_panel.set_image(pixmap)
        return image_panel

    def create_graph_panel(self, df):
        """Create an instance of the graph panel."""
        graph_panel = GraphPanel(self, df)
        graph_panel.init_ui()
        return graph_panel

    def create_thumbnail(self, image_path):
        """Create an instance of a thumbnail."""
        thumbnail = Thumbnail(image_path, main_window=self)  # Pass main window reference
        return thumbnail

    def create_thumbnail_panel(self):
        """Create a thumbnail panel using the existing thumbnails."""
        thumbnail_panel = ThumbnailPanel(self)
        for _, _, thumbnail in self.image_history:
            thumbnail_panel.add_thumbnail(thumbnail)
        return thumbnail_panel

    def render_panels(self, left_panel, right_panel, thumbnail_panel):
        """Draw the image, graph, and thumbnail panels."""
        new_layout = QGridLayout()
        new_layout.addWidget(left_panel, 0, 0, 1, 1)
        new_layout.addWidget(right_panel, 0, 1, 1, 1)
        new_layout.addWidget(thumbnail_panel, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        new_layout.setColumnStretch(0, 1)
        new_layout.setColumnStretch(1, 1)
        new_layout.setRowStretch(0, 5)
        new_layout.setRowStretch(1, 1)

        self.central_widget.setLayout(new_layout)

    def set_empty_panels(self):
        """Set the initial empty placeholder panels."""
        image_panel = ImagePanel(self)
        graph_panel = GraphPanel(self)
        thumbnail_panel = self.create_thumbnail_panel()
        self.render_panels(image_panel, graph_panel, thumbnail_panel)

    def load_panels(self):
        """Load panels based on the current state of the image history."""
        # Reload thumbnails and graph panels
        thumbnail_panel = self.create_thumbnail_panel()

        if self.graph_panel_left is None:
            self.graph_panel_left = GraphPanel(self)
        if self.graph_panel_right is None:
            self.graph_panel_right = GraphPanel(self)

        # Render the panels with left and right graphs and thumbnails
        self.render_panels(self.graph_panel_left, self.graph_panel_right, thumbnail_panel)

    def update_graph_panel(self, image_path, panel_side):
        

        # Clear the current thumbnail indicator for the selected panel before assigning the new one
        if panel_side == "left" and self.thumbnail_left is not None:
            self.thumbnail_left.reset_indicator()  # Clear indicator for the previously assigned left thumbnail

        if panel_side == "right" and self.thumbnail_right is not None:
            self.thumbnail_right.reset_indicator()  # Clear indicator for the previously assigned right thumbnail

        # Find the corresponding graph panel for the new thumbnail
        for image_panel, graph_panel, thumbnail in self.image_history:
            if thumbnail.image_path == image_path:

                # Assign the new graph to the appropriate panel and update the indicator
                if panel_side == "left":
                    self.graph_panel_left = self.create_graph_panel(graph_panel.df)
                    thumbnail.set_indicator("left")  # Set the new indicator for the new thumbnail
                    self.thumbnail_left = thumbnail  # Track the thumbnail assigned to the left panel

                elif panel_side == "right":
                    self.graph_panel_right = self.create_graph_panel(graph_panel.df)
                    thumbnail.set_indicator("right")  # Set the new indicator for the new thumbnail
                    self.thumbnail_right = thumbnail  # Track the thumbnail assigned to the right panel

                break  # Break after updating the selected panel

        # Re-render the panels with updated graphs
        self.reset_central_widget()  # Clear the central widget
        self.load_panels()  # Redraw panels with updated graphs

    def clear_indicator_for_existing_panel(self, panel_side):

        # Clear the indicator for the thumbnail in the left panel
        if panel_side == "left":
            if self.graph_panel_left is not None:
                for _, other_graph_panel, other_thumbnail in self.image_history:
                    if other_graph_panel == self.graph_panel_left:
                        other_thumbnail.reset_indicator()  # Clear the indicator
                        break

        # Clear the indicator for the thumbnail in the right panel
        elif panel_side == "right":
            if self.graph_panel_right is not None:
                for _, other_graph_panel, other_thumbnail in self.image_history:
                    if other_graph_panel == self.graph_panel_right:
                        other_thumbnail.reset_indicator()  # Clear the indicator
                        break

    def set_window_properties(self):
        """Set properties for the main window."""
        self.setWindowTitle("Sediment Core Analysis Tool")
        self.setGeometry(100, 100, 800, 600) 
        self.showMaximized()
        self.setStyleSheet(open('./app/style/style.css').read())


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
            graphs_widget = self.graph_panel.layout.itemAt(1).widget()
            colours_graph = graphs_widget.findChild(ColoursGraph)

            with PdfPages(file_name) as pdf:
                if colours_graph:
                    pdf.savefig(colours_graph.fig)

            self.statusBar().showMessage(f"Graphs saved to: {file_name}")

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

            df = self.graph_panel.df
            if df is not None:
                df.to_csv(file_name, index=False)
                self.statusBar().showMessage(f"Raw data saved to: {file_name}")
            else:
                self.statusBar().showMessage("No data available to export.")

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

            df = self.graph_panel.df
            if df is not None:
                df.to_excel(file_name, index=False)
                self.statusBar().showMessage(f"Raw data saved to: {file_name}")
            else:
                self.statusBar().showMessage("No data available to export.")

    def run_ceilab_analysis(self):
        if hasattr(self.graph_panel_left,'graphs'):
            self.redraw_graph(self.graph_panel_left.graphs.colours_graph,'lab')
        if hasattr(self.graph_panel_right,'graphs'):
            self.redraw_graph(self.graph_panel_right.graphs.colours_graph,'lab')

    def run_rgb_analysis(self):
        if hasattr(self.graph_panel_left,'graphs'):
            self.redraw_graph(self.graph_panel_left.graphs.colours_graph,'rgb')
        if hasattr(self.graph_panel_right,'graphs'):
            self.redraw_graph(self.graph_panel_right.graphs.colours_graph,'rgb')

    def redraw_graph(self,graph_panel,analysis_type):
        graph_panel.analysis_type = analysis_type
        graph_panel.clearSubplots()
        graph_panel.plotColourData()
        graph_panel.draw_idle()

 
