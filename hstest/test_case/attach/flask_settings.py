from __future__ import annotations


class FlaskSettings:
    sources: list[tuple[str, int]] = []
    tryout_ports: list[int] = list(range(8000, 8101))
