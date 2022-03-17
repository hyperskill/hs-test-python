from typing import Any, Dict, Optional

from hstest.testing.plotting.drawing.drawing_data import DrawingData


class Drawing:
    def __init__(self,
                 library: str,
                 plot_type: str,
                 data: Optional[DrawingData],
                 kwargs: Dict[str, Any]):

        self.library: str = library
        self.type: str = plot_type
        self.data: Optional[DrawingData] = data
        self.kwargs: Dict[str, Any] = kwargs
