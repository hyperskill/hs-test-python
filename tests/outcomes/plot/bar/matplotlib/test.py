from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.bar.test_bar_drawing import test_bar_drawing


class TestMatplotlibBar(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [[1, 5], [2, 5], [4, 5], [6, 5]],
            [[1, 6], [2, 6], [4, 6], [6, 6]],
            [[1, 7], [2, 7], [4, 7], [6, 7]],
            [[1, 8], [2, 8], [4, 8], [6, 8]],
        ]

        return test_bar_drawing(self.all_figures(), correct_data, DrawingLibrary.matplotlib)
