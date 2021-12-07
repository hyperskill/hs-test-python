import unittest

from tests.outcomes.plot.cat.test_cat_drawing import test_cat_drawing
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestSeabornCat(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        return test_cat_drawing(self.all_figures, 1, DrawingLibrary.seaborn)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeabornCat('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
