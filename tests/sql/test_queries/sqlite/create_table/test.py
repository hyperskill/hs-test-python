import unittest

from hstest import SQLTest, dynamic_test, correct, wrong


class TestSQLProject(SQLTest):
    queries = {
        'create_table': None
    }

    @dynamic_test
    def test_queries(self):
        self.db.execute(self.queries['create_table'])

        result = self.db.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;")

        if 'contacts' not in result.fetchall()[0]:
            return wrong("Can't find 'contacts' table in the database")

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSQLProject().run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
