import unittest

from hstest import StageTest, dynamic_test, correct, wrong, TestedProgram


class TestWrongOutputWithTooLongOutput(StageTest):

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()
        return wrong('')


class Test(unittest.TestCase):

    def test(self):
        correct_lines = [f'A {i} line' for i in range(1, 250)]

        status, feedback = TestWrongOutputWithTooLongOutput(source_name='main').run_tests()

        for correct_line in correct_lines:
            self.assertIn(correct_line, feedback)

        not_expected_line_in_feedback = '[last 250 lines of output are shown, 1 skipped]'
        self.assertNotIn(not_expected_line_in_feedback, feedback)

        self.assertEqual(status, -1)


if __name__ == '__main__':
    Test().test()
