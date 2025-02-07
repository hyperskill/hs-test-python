import unittest

from hstest import SQLTest, correct, dynamic_test


@unittest.skip(
    "This class should inherit UserErrorTest, but can't since it "
    "inherits StageTest, not SQLTest"
)
class TestSQLProject(SQLTest):
    queries = {"create_table": None}

    @dynamic_test
    def test_queries(self):
        self.execute(
            """CRE TABLE contacts (
            contact_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE
        );"""
        )

        return correct()


class Test(unittest.TestCase):

    def test(self):
        result, feedback = TestSQLProject().run_tests()
        self.assertEqual(result, -1)
        self.assertIn("Unexpected error in test #1", feedback)
        self.assertIn('near "CRE": syntax error', feedback)
