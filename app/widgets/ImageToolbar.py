from os import getcwd
from PyQt6.QtWidgets import QApplication, QToolBar, QPushButton
from PyQt6.QtGui import QPixmap, QAction,QTransform, QIcon
from app.widgets.GraphPanel import GraphPanel

class ImageToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Create the controls panel for images."""

      # Fullscreen button for toggling view
        icon = QIcon.fromTheme(f"{getcwd()}/app/style/rotate.svg")

        self.rotate = QAction("Rotate Image", self, icon=icon)
        self.rotate.triggered.connect(self.rotate_image)
        self.addAction(self.rotate)

    def rotate_image(self):

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
            graph_panel.graphs.layers_graph.flipTopBottomLabels() #flip the top and bottom labels on the layers graph around
    
