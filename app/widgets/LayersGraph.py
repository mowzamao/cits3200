import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class LayersGraph(FigureCanvasQTAgg):
    """A wrapper class for a Matplotlib plot of the sediment layers"""

    def __init__(self, parent=None, width=5, height=5, dpi=100, df = None):    
        
        height = len(df)
        width = max(1, height//10)
        core_as_grid = np.zeros((height, width, 3), dtype=int)

        for row in range(height):
            for col in range(width):
                for channel in range(3):
                    core_as_grid[row][col][channel] = int(df.loc[row, df.columns[channel+1]])

        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = fig.add_subplot(111)
        self.axes.get_xaxis().set_ticks([])
        self.axes.get_yaxis().set_ticks([])
        super(LayersGraph, self).__init__(fig)

        self.axes.imshow(core_as_grid)



