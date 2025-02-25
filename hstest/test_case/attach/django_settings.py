from __future__ import annotations


class DjangoSettings:
    port: int = None
    use_database: bool = False
    test_database: str = "db.test.sqlite3"
    tryout_ports: list[int] = list(range(8000, 8101))
