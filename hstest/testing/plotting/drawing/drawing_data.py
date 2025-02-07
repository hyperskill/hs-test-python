from __future__ import annotations

import numpy as np


class DrawingData:
    def __init__(self, x: np.ndarray, y: np.ndarray) -> None:
        try:
            if not isinstance(x, list | None):
                x = list(x)
            if not isinstance(y, list | None):
                y = list(y)
        except Exception as e:
            msg = "The data argument should be an array"
            raise ValueError(msg) from e

        if x is not None and y is not None and len(x) != len(y):
            msg = "Arrays should be the same length"
            raise ValueError(msg)

        if x is not None:
            x = np.array(x, dtype=object)
        if y is not None:
            y = np.array(y, dtype=object)

        self.x: np.ndarray | None = x
        self.y: np.ndarray | None = y
