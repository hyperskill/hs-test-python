import unittest

from hstest import SQLTest, dynamic_test, correct


class TestSQLProject(SQLTest):
    queries = {
        'create_table': None,
        'insert_data': None
    }

    @dynamic_test
    def test_create_table(self):
        self.execute('create_table')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSQLProject().run_tests()
        self.assertEqual(status, -1)
        self.assertIn('Wrong answer in test #1', feedback)
        self.assertIn('near "CRE": syntax error', feedback)


if __name__ == '__main__':
    Test().test()
