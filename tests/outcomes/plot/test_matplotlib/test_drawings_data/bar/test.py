import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestSeaborn(PlottingTest):
    @dynamic_test
    def test(self):

        import matplotlib
        import pandas as pd
        import numpy as np

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 4:
            return wrong(f'Expected 4 plots to be plotted using pandas library, found {len(self.all_figures)}')

        correct_x = np.array([1, 2, 4, 6])
        correct_y = np.array([])

        for i in range(len(self.all_figures)):
            bar = self.all_figures[i]
            if bar.type != 'bar':
                return wrong(f'Wrong drawing type {bar.type}. Expected bar')

            if 'x' not in bar.data or 'y' not in bar.data:
                return wrong(f"Expected 'x', 'y' keys in the data dict of the bar drawing")

            if not isinstance(bar.data['x'], np.ndarray) or not isinstance(bar.data['y'], np.ndarray):
                return wrong("The 'x', 'y' values should be a ndarray")

            drawing_x = bar.data['x']
            drawing_y = bar.data['y']

            if i == 2:
                correct_x, correct_y = correct_y, correct_x

            if not np.array_equal(correct_x, drawing_x) or not np.array_equal(correct_y, drawing_y):
                return wrong('Wrong data of the bar graph')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeaborn('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
