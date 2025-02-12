from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from hstest.testing.plotting.drawing.drawing_data import DrawingData


class Drawing:
    def __init__(
        self,
        library: str,
        plot_type: str,
        data: DrawingData | None,
        kwargs: dict[str, Any],
    ) -> None:
        self.library: str = library
        self.type: str = plot_type
        self.data: DrawingData | None = data
        self.kwargs: dict[str, Any] = kwargs
