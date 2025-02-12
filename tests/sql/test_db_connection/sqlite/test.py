from sqlite3 import Connection

from hstest import SQLTest, correct, dynamic_test, wrong


class TestSQLProject(SQLTest):
    @dynamic_test
    def test_queries(self):
        if type(self.db) is not Connection:
            return wrong("SQLite should be used by default")

        return correct()
