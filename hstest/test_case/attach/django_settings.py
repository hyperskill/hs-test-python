from typing import List


class DjangoSettings:
    use_database: bool = False
    test_database: str = 'db.test.sqlite3'
    tryout_ports: List[int] = [i for i in range(8000, 8101)]
