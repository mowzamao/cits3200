import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QGridLayout, QHBoxLayout, QWidget, QFileDialog, QScrollArea
)
from PyQt6.QtGui import QPixmap
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

        # State to track images, graphs and thumbnails 
        self.image_history = []  # Track triples of images panels, graph panels and thumbnails
        self.max_images = 2  # Limit to two images at a time
        self.num_images = 0  # The number of active images i.e. 0, 1,..., or max_images
                        
        unit = 10  # main panel height - used as a refernce unit
        self.unit = unit

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
        self.graph_panel_left = None
        self.graph_panel_right = None
        self.thumbnail_panel = None

        ## Rendering the default empty panels
        self.set_empty_panels()

    # Resets the existing central widget 
    # Used prior to re-rendering the panels
    def reset_central_widget(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QGridLayout()

    # Called by Menu when an image is loaded
    # creates the two panels (image and graph) and the thumbnail
    # Adds these to the image history and resets the central panels
    def add_image_and_graph_panel(self, image_path, df):
        """Handle image and graph upload."""
        image_panel = self.create_image_panel(image_path)
        graph_panel = self.create_graph_panel(df)
        thumbnail = self.create_thumbnail(image_path)

        self.image_history.append([image_panel, graph_panel, thumbnail])

        self.reset_central_widget()
        self.load_panels()
        self.num_images += 1


    # Creates an instance of the image panel
    def create_image_panel(self, image_path):
        image_panel = ImagePanel(self)
        pixmap = QPixmap(image_path)
        image_panel.set_image(pixmap)
        return image_panel

    # Creates an instance of the graph panel
    def create_graph_panel(self, df):
        graph_panel = GraphPanel(self, df)
        graph_panel.init_ui()
        return graph_panel

    # Creates an instance of a thumbnail
    def create_thumbnail(self, image_path):
        thumbnail = Thumbnail(image_path)
        return thumbnail
    
    # Creates a thumbnail panel using the existing thumbnails 
    # stored in the image_history
    def create_thumbnail_panel(self):
        thumbnail_panel = ThumbnailPanel(self)
        for image_panel, graph_panel, thumbnail in self.image_history:
            thumbnail_panel.add_thumbnail(thumbnail)
        thumbnail_panel.setStyleSheet("color: #f3f2f0; border-radius: 5px; padding: 20px;")
        return thumbnail_panel
    
    # Draws the image, graph and thumbnail panels
    def render_panels(self, left_panel, right_panel, thumbnail_panel):
        unit = self.unit
        new_layout = QGridLayout()
        new_layout.addWidget(left_panel, 0, 0, unit, unit)
        new_layout.addWidget(right_panel, 0, unit, unit, unit)
        new_layout.addWidget(thumbnail_panel, unit, 0, 2, 2*unit)
        self.central_widget.setLayout(new_layout)

    # Sets the initial empty placeholder panels
    def set_empty_panels(self):
        image_panel = ImagePanel(self)
        graph_panel = GraphPanel(self)
        thumbnail_panel = self.create_thumbnail_panel()
        self.render_panels(image_panel, graph_panel, thumbnail_panel)


    # Loads panels based on the state of the image history and the 
    # num_images state variable
    def load_panels(self):
        match self.num_images:
            case 0:
                image_panel, graph_panel, thumbnail = self.image_history[0]
                thumbnail_panel = self.create_thumbnail_panel()
                self.render_panels(image_panel, graph_panel, thumbnail_panel)
            case _:
                graph_panel_1 = self.image_history[0][1]
                graph_panel_2 = self.image_history[1][1]
                thumbnail_panel = self.create_thumbnail_panel()
                self.render_panels(graph_panel_1, graph_panel_2, thumbnail_panel)

    

    def set_window_properties(self):
        """Set properties for the main window."""
        self.setWindowTitle("Image Analysis Tool")
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
