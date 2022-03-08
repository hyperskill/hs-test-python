import unittest

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.violinplot.test_violin_drawing import test_violin_drawing


class TestSeabornViolin(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        return test_violin_drawing(self.all_figures(), 1, DrawingLibrary.seaborn)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeabornViolin(source_name='main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
