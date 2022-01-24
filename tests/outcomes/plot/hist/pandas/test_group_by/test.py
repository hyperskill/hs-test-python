import unittest

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.hist.test_hist_drawing import test_hist_drawing


class TestGroupBy(PlottingTest):

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [14.55, 11.13, 16.17, 19.14, 13.72, 8.94, 21.87, 15.44],
            [15.2, 13.85, 11.55, 17.37, 12.9, 13.53, 18.22, 24.93, 17.93, 18.6],
        ]

        return test_hist_drawing(self.all_figures(), correct_data, DrawingLibrary.pandas)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestGroupBy('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
