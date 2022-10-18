import unittest

from hstest import correct, dynamic_test, SQLTest


@unittest.skip("This class should inherit UserErrorTest, but can't since it "
               "inherits StageTest, not SQLTest")
class TestSQLProject(SQLTest):
    queries = {
        'create_book_table': None,
        'create_student_table': None,
        'create_staff_table': None,
        'create_operation_table': None,
        'insert_book_table': None,
        'insert_student_table': None,
        'insert_staff_table': None,
        'insert_operation_table': None
    }

    @dynamic_test
    def test(self):
        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSQLProject().run_tests()
        self.assertEqual(status, -1)
        self.assertIn("The 'insert_student_table' query shouldn't be empty!", feedback)


if __name__ == '__main__':
    Test().test()
