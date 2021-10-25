import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import MatplotlibTest
from hstest import TestedProgram


class TestMatplotlib(MatplotlibTest):
    @dynamic_test
    def test(self):
        try:
            import matplotlib
        except ModuleNotFoundError:
            return correct()

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 18:
            return wrong('Expected 18 plots to be plotted using matplotlib library')

        for drawing in self.all_figures:
            if drawing.library != 'matplotlib':
                return wrong('Drawings plotted using wrong library!')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlib('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
