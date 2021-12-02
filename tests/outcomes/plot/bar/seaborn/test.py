import unittest

import numpy as np

from tests.outcomes.plot.bar.test_bar_drawing import test_bar_drawing
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestSeabornBar(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = np.array([
            [['A', 10], ['B', 30], ['C', 20]],
            [['', 10], ['', 30], ['', 20]],
            [[10, ''], [30, ''], [20, '']],
        ], dtype=object)

        return test_bar_drawing(self.all_figures, 3, correct_data, DrawingLibrary.seaborn)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeabornBar('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
