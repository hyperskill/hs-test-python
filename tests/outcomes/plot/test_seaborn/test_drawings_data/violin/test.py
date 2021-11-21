import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestSeabornViolin(PlottingTest):
    @dynamic_test
    def test(self):

        import matplotlib
        import pandas as pd
        import numpy as np

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 5:
            return wrong(f'Expected 5 plots to be plotted using seaborn library, found {len(self.all_figures)}')

        correct_x = [[], [2, 6], ['length'], ['width'], ['test']]
        correct_y = [[2, 6], [], [1, 2], [2, 6], [3, 4]]

        for i in range(len(self.all_figures)):
            violin = self.all_figures[i]

            if violin.type != 'violin':
                return wrong(f'Wrong drawing type {violin.type}. Expected violin')

            if 'x' not in violin.data or 'y' not in violin.data:
                return wrong(f"Expected 'x', 'y' keys in the data dict of the violin drawing")

            if not isinstance(violin.data['x'], np.ndarray):
                return wrong("The 'x' value should be a ndarray")

            if not isinstance(violin.data['y'], np.ndarray):
                return wrong("The 'y' value should be a ndarray")

            drawing_x_data = violin.data['x']
            drawing_y_data = violin.data['y']

            if not np.array_equal(correct_x[i], drawing_x_data) or not np.array_equal(correct_y[i], drawing_y_data):
                return wrong('Wrong data of the violin graph')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeabornViolin('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
