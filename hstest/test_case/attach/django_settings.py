from __future__ import annotations

from typing import ClassVar


class DjangoSettings:
    port: int = None
    use_database: bool = False
    test_database: str = "db.test.sqlite3"
    tryout_ports: ClassVar[list[int]] = list(range(8000, 8101))
