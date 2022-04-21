from typing import Optional

import numpy as np


class DrawingData:
    def __init__(self, x: np.ndarray, y: np.ndarray):
        try:
            if type(x) != list and x is not None:
                x = list(x)
            if type(y) != list and y is not None:
                y = list(y)
        except Exception as _:
            raise ValueError('The data argument should be an array')

        if x is not None and y is not None and len(x) != len(y):
            raise ValueError('Arrays should be the same length')

        if x is not None:
            x = np.array(x, dtype=object)
        if y is not None:
            y = np.array(y, dtype=object)

        self.x: Optional[np.ndarray] = x
        self.y: Optional[np.ndarray] = y
