import unittest

from tests.outcomes.plot.hist.test_hist_drawing import test_hist_drawing
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestPandasHist(PlottingTest):

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
            [[2, 1], [6, 3], [9, 1]],
            [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
            [[2, 1], [6, 3], [9, 1]],
            [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
            [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
            [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1]]
        ]

        return test_hist_drawing(self.all_figures, 7, correct_data, DrawingLibrary.pandas)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPandasHist('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
