import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram, WrongAnswer


class TestSeaborn(PlottingTest):
    @dynamic_test
    def test(self):

        import matplotlib
        import pandas as pd
        import numpy as np

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 5:
            return wrong(f'Expected 5 plots to be plotted using pandas library, found {len(self.all_figures)}')

        labels = np.array(['A', 'B', 'C'])
        indexes = np.array([0, 1, 2])

        val1 = np.array([10, 30, 20])
        val2 = np.array([5, 10, 15])

        for bar in self.all_figures:
            if bar.type != 'bar':
                return wrong(f'Wrong drawing type {bar.type}. Expected bar')

            if 'x' not in bar.data or 'y' not in bar.data:
                return wrong(f"Expected 'x', 'y' keys in the data dict of the bar drawing")

            if not isinstance(bar.data['x'], np.ndarray) or not isinstance(bar.data['y'], np.ndarray):
                return wrong("The 'x' value should be a ndarray")

        self.test_data(self.all_figures[0], labels, val1)
        self.test_data(self.all_figures[1], labels, val2)
        self.test_data(self.all_figures[2], indexes, val1)
        self.test_data(self.all_figures[3], indexes, val1)
        self.test_data(self.all_figures[4], indexes, val2)

        return correct()

    def test_data(self, drawing, correct_x, correct_y):

        import numpy as np

        drawing_x = drawing.data['x']
        drawing_y = drawing.data['y']

        if not np.array_equal(drawing_x, correct_x) or not np.array_equal(drawing_y, correct_y):
            raise WrongAnswer('Wrong data of the hist graph')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeaborn('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
