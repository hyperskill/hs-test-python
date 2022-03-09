import unittest

from hstest import StageTest, dynamic_test, correct, wrong, TestedProgram


class TestWrongOutputWithTooLongOutput(StageTest):

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start("-arg", "test")
        return wrong('')


class Test(unittest.TestCase):

    def test(self):
        expected_line_in_feedback = "Arguments: -arg test\n\n[last 250 lines of output are shown, 1 skipped]"

        status, feedback = TestWrongOutputWithTooLongOutput().run_tests()
        self.assertIn(expected_line_in_feedback, feedback)
        self.assertEqual(status, -1)


if __name__ == '__main__':
    Test().test()
