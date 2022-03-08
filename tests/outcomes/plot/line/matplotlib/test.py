import unittest

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.line.test_line_drawing import test_line_drawing


class TestMatplotlibLine(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [[1, 5], [2, 8]],
            [[1, 5], [2, 8]],
            [[1, 0], [5, 1], [7, 2], [8, 3]]
        ]

        return test_line_drawing(self.all_figures(), 3, correct_data, DrawingLibrary.matplotlib)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlibLine(source_name='main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
