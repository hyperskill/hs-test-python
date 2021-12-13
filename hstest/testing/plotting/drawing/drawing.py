from typing import Any, Dict, Optional

import numpy as np


class Drawing:
    def __init__(self,
                 library: str,
                 plot_type: str,
                 data: Optional[np.ndarray],
                 kwargs: Dict[str, Any]):

        self.library: str = library
        self.type: str = plot_type
        self.data: Optional[np.ndarray] = data
        self.kwargs: Dict[str, Any] = kwargs
