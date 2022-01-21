import unittest

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.hist.test_hist_drawing import test_hist_drawing


class TestPandasHist(PlottingTest):

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [1, 2, 3, 4, 5],
            [2, 9, 6, 6, 6],
            [1, 2, 3, 4, 5],
            [2, 9, 6, 6, 6],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5]
        ]

        return test_hist_drawing(self.all_figures(), 7, correct_data, DrawingLibrary.pandas)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPandasHist('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
