import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestSeabornScatter(PlottingTest):
    @dynamic_test
    def test(self):

        import matplotlib
        import pandas as pd
        import numpy as np

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 4:
            return wrong(f'Expected 4 plots to be plotted using seaborn library, found {len(self.all_figures)}')

        correct_x = [1, 2]
        correct_y = [2, 6]

        for scatter in self.all_figures[:1]:
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

        correct_y = [[1, 2], [2, 6], [3, 4]]
        correct_x = [0, 1]

        for i in range(1, len(self.all_figures)):
            scatter = self.all_figures[i]

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

            if not np.array_equal(correct_x, drawing_x_data) or not np.array_equal(correct_y[i - 1], drawing_y_data):
                return wrong('Wrong data of the scatter graph')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeabornScatter('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
