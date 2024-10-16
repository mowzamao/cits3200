from os import getcwd
from PyQt6.QtWidgets import QApplication, QToolBar, QPushButton, QInputDialog, QLineEdit
from PyQt6.QtGui import QPixmap, QAction,QTransform, QIcon
from app.widgets.GraphPanel import GraphPanel
import numpy as np
from app.utils.ProcessSedimentCore import process_core_image

from os import getcwd
from PyQt6.QtGui import QAction
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtGui import QAction, QIcon, QPixmap, QPainter
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QByteArray
from matplotlib.backends.backend_pdf import PdfPages
from app.widgets.ColoursGraph import ColoursGraph


class ImageToolbar(QToolBar):

    layers_graph_top_axes_label = 'Top'
    layers_graph_bottom_axes_label = 'Bottom'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create the controls panel for images."""

        flip_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-hr" viewBox="0 0 16 16"><rect width="100%" height="100%" fill="#f3f2f0" /><path d="M12 3H4a1 1 0 0 0-1 1v2.5H2V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v2.5h-1V4a1 1 0 0 0-1-1M2 9.5h1V12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V9.5h1V12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2zm-1.5-2a.5.5 0 0 0 0 1h15a.5.5 0 0 0 0-1z"/></svg>"""
        self.flip = QAction("Flip image", self, icon=self.svg_to_icon(flip_svg))
        self.flip.triggered.connect(self.flip_image)
        self.addAction(self.flip)

        calibrate_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-gear" viewBox="0 0 16 16"><rect width="100%" height="100%" fill="#f3f2f0" /><path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492M5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0"/><path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115z"/></svg>"""
        self.calibrate = QAction("Change width measurement", self, icon=self.svg_to_icon(calibrate_svg))
        self.calibrate.triggered.connect(self.calibrate_image)
        self.addAction(self.calibrate)


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
    

    def flip_image(self):
        # Flipping the image in the image panel
        transform = QTransform().rotate(180) 
        img = self.parent().image
        if img != None:
            img_flipped = img.transformed(transform)
            self.parent().set_image(img_flipped)

            # Inverting the dataframe and re-showing the graphs
            graph_panel = self.parent().parent().findChild(GraphPanel)
            
            max_depth = max(graph_panel.df['Depth (mm)'])
            new_depths = graph_panel.df['Depth (mm)'].apply(lambda x: max_depth - x)
            
            graph_panel.df['Depth (mm)'] = new_depths
            
            graph_panel.init_ui()

            self.flipTopBottomLabels()

            graph_panel.graphs.layers_graph.layers_axes.set_xlabel(self.layers_graph_bottom_axes_label)
            graph_panel.graphs.layers_graph.layers_axes_top.set_xlabel(self.layers_graph_top_axes_label)  

    def flipTopBottomLabels(self):
        """
        Function to flip the location of the top and bottom labels on the layers graph.
        """
        self.layers_graph_top_axes_label = self.getNewLabel(self.layers_graph_top_axes_label)
        self.layers_graph_bottom_axes_label = self.getNewLabel(self.layers_graph_bottom_axes_label)

    def getNewLabel(self, label):
        return {'Top': 'Bottom', 'Bottom': 'Top'}.get(label, '')

    def calibrate_image(self):
        """
        Creates PyQt6 QInputDialog to prompt user for width of sediment core, then reloads graph display with the new width
        """
        main_window = self.parent().parent().parent()
        image_path = main_window.panel_left.image_path
        image = main_window.panel_right.image

        if image_path:
            text, ok = QInputDialog.getText(self, "Sediment Core Analysis", "Please input the width of the core in the image (in mm):")
            if text and ok:
                if text.isdigit():
                    new_data = process_core_image(image, int(text), df=True)
                    if new_data != 0:
                        new_df = new_data["Colours"] 

                        # Resets the graph_panel object/s correpsonding to the file_path/s 
                        self.parent().parent().parent().reset_data(image_path, new_df, image)
                        self.parent().parent().parent().update_graph_panel(image_path, "single")