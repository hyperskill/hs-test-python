import unittest

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.line.test_line_drawing import test_line_drawing


class TestPandasLine(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [[0, 1], [1, 3], [2, 2]],
            [[0, 1], [1, 3], [2, 2]],
            [[2, 1], [4, 3], [6, 2]],
            [[2, 1], [4, 3], [6, 2]]
        ]

        return test_line_drawing(self.all_figures(), 4, correct_data, DrawingLibrary.pandas)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPandasLine(source_name='main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
