from typing import List, Tuple


class FlaskSettings:
    sources: List[Tuple[str, int]] = []
    tryout_ports: List[int] = [i for i in range(8000, 8101)]
