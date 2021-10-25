import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import MatplotlibTest
from hstest import TestedProgram


class TestSeaborn(MatplotlibTest):
    @dynamic_test
    def test(self):
        try:
            import matplotlib
            import pandas as pd
        except ModuleNotFoundError:
            return correct()

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 22:
            return wrong(f'Expected 22 plots to be plotted using matplotlib library, found {len(self.all_figures)}')

        for drawing in self.all_figures:
            if drawing.library != 'pandas':
                return wrong('Drawings plotted using wrong library!')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeaborn('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
