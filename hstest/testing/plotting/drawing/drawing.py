import numpy as np


class Drawing:
    def __init__(self, library: str, plot_type: str, data: np.ndarray):
        self.library: str = library
        self.type: str = plot_type
        self.data: np.ndarray = data
