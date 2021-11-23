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

        correct_x = [[], [2, 4], ['Col1'], ['Col2'], [1, 3]]
        correct_y = [[1, 3], [], [1, 3], [2, 4], [2, 4]]

        for i, dis in enumerate(self.all_figures):
            if dis.type != 'dis':
                return wrong(f'Wrong drawing type {dis.type}. Expected dis')

            if 'x' not in dis.data or 'y' not in dis.data:
                return wrong(f"Expected 'x', 'y' keys in the data dict of the dis drawing")

            if not isinstance(dis.data['x'], np.ndarray):
                return wrong("The 'x' value should be a ndarray")

            if not isinstance(dis.data['y'], np.ndarray):
                return wrong("The 'y' value should be a ndarray")

            drawing_x_data = dis.data['x']
            drawing_y_data = dis.data['y']

            if not np.array_equal(correct_x[i], drawing_x_data) or not np.array_equal(correct_y[i], drawing_y_data):
                return wrong('Wrong data of the dis graph')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeabornViolin('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
