import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QScrollArea
)
from PyQt6.QtGui import QPixmap
import pandas as pd

from app.widgets.Menu import Menu
from app.widgets.ImagePanel import ImagePanel
from app.widgets.Toolbar import Toolbar
from app.widgets.GraphPanel import GraphPanel


class MainWindow(QMainWindow):
    """Main window handling the display of images and graphs, with comparison options."""
    def __init__(self):
        """Initialize the main window and setup UI components."""
        super().__init__()

        # State to track images and graphs (store only 2 sets at a time)
        self.image_history = []  # Track pairs of images and graph panels
        self.max_images = 2  # Limit to two images at a time

        # Set window properties
        self.set_window_properties()

        # Create scroll area for horizontal scrolling
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)  # Allow widget resizing within the scroll area

        # Create a widget to hold the actual layout and panels
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)

        # Main layout for side-by-side images and graphs
        self.main_layout = QHBoxLayout(self.scroll_widget)

        # Set the scroll area as the central widget of the main window
        self.setCentralWidget(self.scroll_area)

        # Initialize toolbar and menu
        self.toolbar = Toolbar(self)
        self.menu = Menu(self)

        # Add toolbar and menu
        self.addToolBar(self.toolbar)
        self.setMenuBar(self.menu)

        # Add placeholder panels for image and graph at initialization
        self.image_panel_1 = ImagePanel(self)
        self.graph_panel_1 = GraphPanel(self)

        # Add the placeholder panels to the layout
        self.main_layout.addWidget(self.image_panel_1, stretch=5)
        self.main_layout.addWidget(self.graph_panel_1, stretch=5)

    def add_image_and_graph_panel(self, image_path, df):
        """Handle image and graph upload, replacing placeholders and adding them side by side."""
        if len(self.image_history) < self.max_images:
            # First or second image being uploaded, add it to the layout
            self.replace_placeholder(image_path, df)
        else:
            # More than two images, replace the oldest one
            self.replace_oldest_image_and_graph(image_path, df)

    def replace_placeholder(self, image_path, df):
        """Replace the placeholders with actual image and graph."""
        # Create and display the image panel
        image_panel = ImagePanel(self)
        pixmap = QPixmap(image_path)
        image_panel.set_image(pixmap)

        # Create and display the graph panel for the image
        graph_panel = GraphPanel(self, df)
        graph_panel.init_ui()

        # Replace the placeholders if it's the first image being uploaded
        if len(self.image_history) == 0:
            # Replace the first placeholder panels with actual panels
            self.main_layout.replaceWidget(self.image_panel_1, image_panel)
            self.main_layout.replaceWidget(self.graph_panel_1, graph_panel)

            # Delete the placeholders
            self.image_panel_1.deleteLater()
            self.graph_panel_1.deleteLater()
        else:
            # Add the second set of image/graph side by side
            self.main_layout.addWidget(image_panel, stretch=5)
            self.main_layout.addWidget(graph_panel, stretch=5)

        # Store the image and graph panels in history
        self.image_history.append((image_panel, graph_panel))

    def replace_oldest_image_and_graph(self, image_path, df):
        """Replace the oldest image and graph when a third or more images are uploaded."""
        # Remove the oldest image and graph
        old_image, old_graph = self.image_history.pop(0)
        self.main_layout.removeWidget(old_image)
        self.main_layout.removeWidget(old_graph)
        old_image.deleteLater()
        old_graph.deleteLater()

        # Create and display the new image and graph
        image_panel = ImagePanel(self)
        pixmap = QPixmap(image_path)
        image_panel.set_image(pixmap)

        graph_panel = GraphPanel(self, df)
        graph_panel.init_ui()

        # Add the new image and graph back into the layout
        self.main_layout.addWidget(image_panel, stretch=5)
        self.main_layout.addWidget(graph_panel, stretch=5)

        # Store the new image and graph
        self.image_history.append((image_panel, graph_panel))

    def set_window_properties(self):
        """Set properties for the main window."""
        self.setWindowTitle("Image Analysis Tool")
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
