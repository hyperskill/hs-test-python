import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram
from hstest.testing.plotting.matplotlib_handler import MatplotlibHandler


class TestMatplotlib(PlottingTest):
    @dynamic_test
    def test(self):
        import matplotlib

        MatplotlibHandler.revert_plots()
        backend = matplotlib.get_backend()
        matplotlib.use('Agg')

        program = TestedProgram()
        program.start()

        matplotlib.use(backend)

        if len(self.all_figures) != 0:
            return wrong(f'Expected 0 plots to be plotted using matplotlib library, found {len(self.all_figures)}')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlib('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
