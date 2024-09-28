from PyQt6.QtGui import QPixmap 
from app.utils.ImageTransforming import * 
from app.utils.ProcessSedimentCore import *   

from time import time, sleep
from PyQt6.QtCore import  Qt, QTimer, pyqtSignal,QObject, QObject, QThread, QThreadPool, pyqtSignal, pyqtSlot

class DataExtractor(QObject):
    
    data = pyqtSignal(dict)
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def run(self, image):
        #Format the image and display it in ImagePanel
        oriented_image = orient_array(image)

        self.progress.emit(30)
        sleep(1)
        self.progress.emit(30)
        sleep(1)
        self.progress.emit(30)
        sleep(1)
        self.progress.emit(30)
        sleep(1)

        #Process the core image to get the data (df)
        data_dict = process_core_image(oriented_image, 77, True)  # Use 77mm as core width

        self.data.emit(data_dict)
        self.finished.emit() 
