import unittest
from sqlite3 import Connection

from hstest import SQLTest, dynamic_test, correct, wrong


class TestSQLProject(SQLTest):
    @dynamic_test
    def test_queries(self):
        if type(self.db) is not Connection:
            return wrong('SQLite should be used by default')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSQLProject().run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
