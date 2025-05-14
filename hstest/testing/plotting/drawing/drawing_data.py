from __future__ import annotations

import numpy as np


class DrawingData:
    def __init__(self, x: np.ndarray, y: np.ndarray) -> None:
        try:
            if type(x) != list and x is not None:
                x = list(x)
            if type(y) != list and y is not None:
                y = list(y)
        except Exception:
            msg = "The data argument should be an array"
            raise ValueError(msg)

        if x is not None and y is not None and len(x) != len(y):
            msg = "Arrays should be the same length"
            raise ValueError(msg)

        if x is not None:
            x = np.array(x, dtype=object)
        if y is not None:
            y = np.array(y, dtype=object)

        self.x: np.ndarray | None = x
        self.y: np.ndarray | None = y
