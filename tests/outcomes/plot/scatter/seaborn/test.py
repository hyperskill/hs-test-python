import unittest

from tests.outcomes.plot.scatter.test_scatter_drawing import test_scatter_drawing
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestSeabornScatter(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [[1, 2], [2, 6]],
            [[0, 1], [1, 2]],
            [[0, 2], [1, 6]],
            [[0, 3], [1, 4]]
        ]

        return test_scatter_drawing(self.all_figures, 4, correct_data, DrawingLibrary.seaborn)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeabornScatter('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
