import unittest

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.hist.test_hist_drawing import test_hist_drawing


class TestSeabornHist(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [5, 2, 1, 4, 5, 3],
            [5, 2, 1, 4, 5, 3],
        ]

        return test_hist_drawing(self.all_figures(), correct_data, DrawingLibrary.seaborn)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeabornHist('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
