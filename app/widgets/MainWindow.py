import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QWidget, QFileDialog, QStatusBar, QMenuBar, QMenu
)
from PyQt6.QtGui import QPixmap, QAction  
from PyQt6.QtCore import Qt, QSize
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

from app.widgets.Menu import Menu
from app.widgets.ImagePanel import ImagePanel
from app.widgets.Toolbar import Toolbar
from app.widgets.GraphPanel import GraphPanel
from app.widgets.ColoursGraph import ColoursGraph
from app.widgets.LayersGraph import LayersGraph

class MainWindow(QMainWindow):
    """ A class defining the structure and actions of the outermost window in the application
        Args:
            QMainWindow (): A child class of QtWidgets that inherits from QWidget.
    """
    def __init__(self):
        """Initialize the main window and setup UI components."""
        super().__init__()

        self.set_window_properties()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)


        self.image_panel = ImagePanel(self)
        self.graph_panel = GraphPanel(self)
        self.toolbar = Toolbar(self)
        self.menu = Menu(self)


        self.addToolBar(self.toolbar)
        self.setMenuBar(self.menu)
        self.main_layout.addWidget(self.image_panel, stretch =5)
        self.main_layout.addWidget(self.graph_panel, stretch =5)


    def set_window_properties(self):
        """Set properties for the main window."""
        self.setWindowTitle("Sediment Core Analysis Tool")
        self.setGeometry(100, 100, 800, 600) 
        self.showMaximized()
        self.setStyleSheet(open('./app/style/style.css').read())
        
    def export_graphs_as_pdf(self): 
        """Export the graphs displayed in the graph panel as a PDF file."""
        # Open file dialog to specify where to save the PDF
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Graphs as PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if file_name:
            if not file_name.endswith('.pdf'):
                file_name += '.pdf'

            # Get the graphs (ColoursGraph and LayersGraph) from the GraphPanel
            graphs_widget = self.graph_panel.layout.itemAt(1).widget()  # This should be the Graphs widget
            
            # Assuming ColoursGraph is the first child in Graphs widget
            colours_graph = graphs_widget.findChild(ColoursGraph)
           

            # Export both figures to a PDF using PdfPages
            with PdfPages(file_name) as pdf:
                if colours_graph:
                    pdf.savefig(colours_graph.fig)  # Save ColoursGraph as a page in the PDF
             

            # Optional: Show message in status bar
            self.statusBar().showMessage(f"Graphs saved to: {file_name}")
    
    # Function to export raw data to CSV
    def export_data_to_csv(self):
        # Open a file dialog for the user to select a location to save the CSV
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Raw Data as CSV",
            "",
            "CSV Files (*.csv)"  # Filter for CSV files
        )

        if file_name:
            if not file_name.endswith('.csv'):
                file_name += '.csv'

            # Get the DataFrame from the graph panel
            df = self.graph_panel.df  # Assuming df contains your raw data
            
            if df is not None:
                # Export the DataFrame to CSV
                df.to_csv(file_name, index=False)
                self.statusBar().showMessage(f"Raw data saved to: {file_name}")
            else:
                self.statusBar().showMessage("No data available to export.")

    # Function to export raw data to Excel
    def export_data_to_excel(self):
        # Open a file dialog to specify where to save the Excel file
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Raw Data as Excel",
            "",
            "Excel Files (*.xlsx)"
        )

        if file_name:
            if not file_name.endswith('.xlsx'):
                file_name += '.xlsx'

            # Get the DataFrame from the graph panel (assuming df is stored there)
            df = self.graph_panel.df  # Make sure this is where your data is stored
            
            if df is not None:
                # Export the DataFrame to Excel
                df.to_excel(file_name, index=False)
                self.statusBar().showMessage(f"Raw data saved to: {file_name}")
            else:
                self.statusBar().showMessage("No data available to export.")

 
