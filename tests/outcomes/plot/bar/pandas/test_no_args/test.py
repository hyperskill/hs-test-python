from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.bar.test_bar_drawing import test_bar_drawing


class TestSeabornBar(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]],
            [[0, 3], [1, 4], [2, 5], [3, 6], [4, 7]],
        ]

        return test_bar_drawing(self.all_figures(), correct_data, DrawingLibrary.pandas)
