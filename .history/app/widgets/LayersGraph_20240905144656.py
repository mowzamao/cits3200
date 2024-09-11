import numpy as np
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class LayersGraph(FigureCanvasQTAgg):
    """A wrapper class for a Matplotlib plot of the sediment layers"""

    def __init__(self, parent=None, width=5, height=5, dpi=100, df = None):    
        
        height = len(df)
        width = height//10
        core_as_grid = np.empty((width, height, 3))

        for i, row in df.iterrows():
            for j in range(width):
                for k in range(3):
                    core_grid[i][j][k] = df[i,j]


        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = fig.add_subplot(131)
        super(LayersGraph, self).__init__(fig)

        # Red channel
        self.axes.images(core_as_grid)


