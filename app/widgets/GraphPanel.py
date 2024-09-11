
#importing classes for PyQT formatting 
from PyQt6.QtWidgets import QWidget,  QHBoxLayout
from PyQt6.QtCore import Qt

#import packages for generation of test data
from app.utils.RandomDataGenerator import RandomDataGenerator

#import scripts to generate instances of the graphs to be displayed in the main window 
from app.widgets.ColoursGraph import ColoursGraph
from app.widgets.LayersGraph import LayersGraph

class GraphPanel(QWidget):
    """
    The PyQt class that defines the panel showing the colour graphs

    Parameters:
        QWidget(Class): A base/parent class making GraphPanel a PyQT widget.
    """

    def __init__(self, parent=None):
        """
        The initialisation function for the GraphPanel class/PyQt widget.

        Parameters:
            parent(Class): paramater to optionally add a base/parent class upon initialisation. 
        """

        #Initialise instance of the GraphPanel class by using the QWidget initialisation function
        super().__init__(parent)

        #Create and set the graphs for this instance of the GraphPanel class
        self.init_ui()

    def init_ui(self):
        """
        Function to generate and define plots for the GraphPanel Widget.
        """

        ##################################################### 
        # Testing with random data, remove for MVP 
        source = RandomDataGenerator()
        df = source.get_random_dataset()
        ######################################################

        #Create QHBoxLayout instance as a container for both colour and layer plots
        #layout = QHBoxLayout()

        #Create instances of the colours and graphs plots. 
        colours_graph = ColoursGraph(self, width=5, height=5, dpi=100, df = df)
        layers_graph  = LayersGraph(self, width=20, height=20, dpi=100, df = df)

        #Add graphs to the GHBoxLayout widget
        # layout.addWidget(layers_graph,stretch=2)  
        # layout.addWidget(colours_graph, stretch=8)

        colours_layout = QHBoxLayout()
        colours_layout.addWidget(colours_graph)

        layers_layout = QHBoxLayout()
        layers_layout.addWidget(layers_graph)

        main_layout = QHBoxLayout()
        main_layout.addLayout(layers_layout,stretch=2)
        main_layout.addLayout(colours_layout,stretch=8)


        #Set the layout of this instance of the Graph Panel class to the new QHBoxLayout widget
        self.setLayout(main_layout)