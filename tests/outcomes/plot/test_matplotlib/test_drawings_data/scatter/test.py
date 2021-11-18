import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestMatplotlibScatter(PlottingTest):
    @dynamic_test
    def test(self):

        import matplotlib
        import pandas as pd
        import numpy as np

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 2:
            return wrong(f'Expected 2 plots to be plotted using matplotlib library, found {len(self.all_figures)}')

        correct_x = [1, 2]
        correct_y = [2, 6]

        for scatter in self.all_figures:
            if scatter.type != 'scatter':
                return wrong(f'Wrong drawing type {scatter.type}. Expected scatter')

            if 'x' not in scatter.data or 'y' not in scatter.data:
                return wrong(f"Expected 'x', 'y' keys in the data dict of the scatter drawing")

            if not isinstance(scatter.data['x'], np.ndarray):
                return wrong("The 'x' value should be a ndarray")

            if not isinstance(scatter.data['y'], np.ndarray):
                return wrong("The 'y' value should be a ndarray")

            drawing_x_data = scatter.data['x']
            drawing_y_data = scatter.data['y']

            if not np.array_equal(correct_x, drawing_x_data) or not np.array_equal(correct_y, drawing_y_data):
                return wrong('Wrong data of the scatter graph')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlibScatter('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
