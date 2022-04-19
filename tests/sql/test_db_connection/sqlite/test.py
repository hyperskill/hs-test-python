from hstest import SQLTest, dynamic_test, correct, wrong
from sqlite3 import Connection


class TestSQLProject(SQLTest):
    @dynamic_test
    def test_queries(self):
        if type(self.db) is not Connection:
            return wrong('SQLite should be used by default')

        return correct()
