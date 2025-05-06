from __future__ import annotations

from typing import ClassVar


class FlaskSettings:
    sources: ClassVar[list[tuple[str, int]]] = []
    tryout_ports: ClassVar[list[int]] = list(range(8000, 8101))
