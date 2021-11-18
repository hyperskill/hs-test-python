import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestMatplotlibPie(PlottingTest):
    @dynamic_test
    def test(self):

        import matplotlib
        import pandas as pd
        import numpy as np

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 2:
            return wrong(f'Expected 2 plots to be plotted using pandas library, found {len(self.all_figures)}')

        correct_x = ['Mercury', 'Venus', 'Earth']
        correct_y = [0.330, 4.87, 5.97]

        for i in range(len(self.all_figures)):

            if i == 1:
                correct_y = [2439.7, 6051.8, 6378.1]

            pie = self.all_figures[i]

            if pie.type != 'pie':
                return wrong(f'Wrong drawing type {pie.type}. Expected pie')

            if 'x' not in pie.data or 'y' not in pie.data:
                return wrong(f"Expected 'x', 'y' keys in the data dict of the pie drawing")

            if not isinstance(pie.data['x'], np.ndarray):
                return wrong("The 'x' value should be a ndarray")

            if not isinstance(pie.data['y'], np.ndarray):
                return wrong("The 'y' value should be a ndarray")

            drawing_x_data = pie.data['x']
            drawing_y_data = pie.data['y']

            if not np.array_equal(correct_x, drawing_x_data) or not np.array_equal(correct_y, drawing_y_data):
                return wrong('Wrong data of the pie graph')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlibPie('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
