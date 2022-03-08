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
        wrong_lines = [f'A {i} line' for i in range(0, 1)]

        status, feedback = TestWrongOutputWithTooLongOutput(source_name='main').run_tests()

        for correct_line in correct_lines:
            self.assertIn(correct_line, feedback)

        for wrong_line in wrong_lines:
            self.assertNotIn(wrong_line, feedback)

        expected_line_in_feedback = '[last 250 lines of output are shown, 1 skipped]'
        self.assertIn(expected_line_in_feedback, feedback)

        self.assertEqual(status, -1)


if __name__ == '__main__':
    Test().test()
