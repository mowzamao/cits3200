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
from app.widgets.ColoursGraph import ColoursGraph
from app.widgets.ThumbnailPanel import ThumbnailPanel
from app.widgets.Thumbnail import Thumbnail
from matplotlib.backends.backend_pdf import PdfPages


class MainWindow(QMainWindow):
    """Main window handling the display of images and graphs, with comparison options."""
    def __init__(self):
        """Initialize the main window and setup UI components."""
        super().__init__()

        # State to track images, graphs, and thumbnails
        self.image_history = []  # Track triples of image panels, graph panels, and thumbnails
        self.num_images = 0  # The number of active images i.e. 0, 1,..., or more

        # Initialising panel references
        self.panel_left = None 
        self.panel_right = None 
        self.thumbnail_panel = None

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

        # Render the default empty panels
        self.set_empty_panels()



    def reset_central_widget(self):
        """Reset the existing central widget."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QGridLayout()

    def add_image_and_graph_panel(self, image_path, df, image):
        """Handle image and graph upload."""

        # Setting the self.thumbnail_panel before rendering
        thumbnail = self.create_thumbnail(image_path)
        self.thumbnail_panel = self.create_thumbnail_panel() 
                                                             
        image_panel = self.create_image_panel(image_path)
        graph_panel = self.create_graph_panel(df, image)
        self.image_history.append([image_panel, graph_panel, thumbnail])

        self.render_panels()
        self.num_images += 1

        # Update the central widget layout with new thumbnails and panels

    def create_image_panel(self, image_path):
        """Create an instance of the image panel."""
        image_panel = ImagePanel(self)
        pixmap = QPixmap(image_path)
        image_panel.set_image(pixmap)
        image_panel.image_path = image_path
        return image_panel

    def create_graph_panel(self, df, image):
        """Create an instance of the graph panel."""
        graph_panel = GraphPanel(self, df, image)
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


    def render_panels(self):
        """Draw the image, graph, and thumbnail panels."""
        self.reset_central_widget()

        if self.panel_left is None:
            self.panel_left = GraphPanel(self)
        if self.panel_right is None:
            self.panel_right = GraphPanel(self)

        self.thumbnail_panel = self.create_thumbnail_panel()

        new_layout = QGridLayout()
        # Always add left and right panels (whether image or graph)
        new_layout.addWidget(self.panel_left, 0, 0, 1, 1)
        new_layout.addWidget(self.panel_right, 0, 1, 1, 1)
    
        # Thumbnails at the bottom
        new_layout.addWidget(self.thumbnail_panel, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)
    
        new_layout.setColumnStretch(0, 1)
        new_layout.setColumnStretch(1, 1)
        new_layout.setRowStretch(0, 5)
        new_layout.setRowStretch(1, 1)

        new_layout.setContentsMargins(0, 0, 0, 0)
        new_layout.setSpacing(3)   

        self.central_widget.setLayout(new_layout)

        self.showMaximized() # Fixes issue with window going out of bounds 


    def set_empty_panels(self):
        """Set the initial empty placeholder panels."""
        self.panel_left = ImagePanel(self)
        self.panel_right = GraphPanel(self)
        self.thumbnail_panel = self.create_thumbnail_panel()
        self.render_panels()


    def update_graph_panel(self, image_path, panel_side):
        """Update the panels based on the selected option."""
    
        # Handle Single Image Analysis
        if panel_side == "single":
        # Create an image panel for the left
            self.panel_left = self.create_image_panel(image_path)
        
            # Find the corresponding graph panel for the image and assign it to the right
            for _, graph_panel, thumbnail in self.image_history:
                if thumbnail.image_path == image_path:
                    self.panel_right = self.create_graph_panel(graph_panel.df, graph_panel.image)
                    break

            # Re-render the panels with the new layout
            self.render_panels()

            # Mark the mode as Single Image Analysis
            self.is_single_image_analysis = True
            return  # Exit early since this is single image analysis


        # Find the `df` (dataframe) for the selected image based on the thumbnail
        for _, graph_panel, thumbnail in self.image_history:
            if thumbnail.image_path == image_path:
                df = graph_panel.df  # Retrieve the dataframe from the graph panel
                image = graph_panel.image
                break

        # Existing logic for left or right panel
        if panel_side == "left":
            self.panel_left = self.create_graph_panel(df, image)  # Use the retrieved `df`
            self.thumbnail_panel = self.create_thumbnail_panel()

        elif panel_side == "right":
            self.panel_right = self.create_graph_panel(df, image)  # Use the retrieved `df`
            self.thumbnail_panel = self.create_thumbnail_panel()
    

        # Re-render the panels
        self.render_panels()


    def reset_data(self, image_path, new_df, image):
        index = 0
        for image_panel, _, _ in self.image_history:
            if (image_panel.image_path == image_path):

                self.image_history[index][1] = GraphPanel(self, new_df, image)
                self.panel_right = self.image_history[index][1]
                break

            index += 1



    def clear_indicator_for_existing_panel(self, panel_side):
        # # Clear the indicator for the thumbnail in the left panel
        # if panel_side == "left":
        #     if self.graph_panel_left is not None:
        #         for _, other_graph_panel, other_thumbnail in self.image_history:
        #             if other_graph_panel == self.graph_panel_left:
        #                 other_thumbnail.reset_indicator()  # Clear the indicator
        #                 break

        # # Clear the indicator for the thumbnail in the right panel
        # elif panel_side == "right":
        #     if self.graph_panel_right is not None:
        #         for _, other_graph_panel, other_thumbnail in self.image_history:
        #             if other_graph_panel == self.graph_panel_right:
        #                 other_thumbnail.reset_indicator()  # Clear the indicator
        #                 break
        pass


    def set_window_properties(self):
        """Set properties for the main window."""
        self.setWindowTitle("Sediment Core Analysis Tool")
        self.setGeometry(100, 100, 800, 600) 
        self.showMaximized()
        self.setStyleSheet("""
QMainWindow {background-color: #eaeaea;}

QMenuBar {
  color: #f3f2f0;
  padding: 3px;
  font-weight: 650;
  background-color: #8a4c57;
}

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
  color: #FAF7F7;
  background-color: #B2737F;
}
""")    

    def analysis_swap(self):
        for panel in [self.panel_left,self.panel_right]:
            if isinstance(panel,GraphPanel) and panel.graphs is not None:
                panel.graphs.colours_graph.setNewAnalysisType()
                panel.graphs.colours_graph.clearSubplots()
                panel.graphs.colours_graph.plotColourData()
                panel.graphs.colours_graph.draw_idle()
    

 
