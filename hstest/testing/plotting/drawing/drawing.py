from typing import Optional

import numpy as np


class Drawing:
    def __init__(self,
                 library: str,
                 plot_type: str,
                 data: Optional[np.ndarray]):
        self.library: str = library
        self.type: str = plot_type
        self.data: Optional[np.ndarray] = data
