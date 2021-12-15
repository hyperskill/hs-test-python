import unittest

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.hist.test_hist_drawing import test_hist_drawing


class TestMatplotlibHist(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
            [[1, 1], [1.4, 1], [2, 1], [5, 2], [6, 1]],
            [[1, 2], [4, 1], [2, 1]],
            [[1, 1], [2, 1], [5, 1], ['a', 1], ['aa', 1], ['b', 1], ['bb', 1]],
            [[1.1, 2], [5, 2], [2, 1]],
            [[1.1, 1], [1.5, 1], [2.1, 1], [2.5, 1], [3.6, 1]]
        ]

        return test_hist_drawing(self.all_figures(), 6, correct_data, DrawingLibrary.matplotlib)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlibHist('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
