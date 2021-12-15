import unittest

import numpy as np

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.bar.test_bar_drawing import test_bar_drawing


class TestPandasBar(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = np.array([
            [[0, 10], [1, 30], [2, 20]],
            [[0, 5], [1, 10], [2, 15]],
            [['A', 10], ['B', 30], ['C', 20]]
        ], dtype=object)

        return test_bar_drawing(self.all_figures(), 3, correct_data, DrawingLibrary.pandas)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPandasBar('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
