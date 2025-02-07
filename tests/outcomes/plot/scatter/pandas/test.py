from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.scatter.test_scatter_drawing import \
    test_scatter_drawing


class TestPandasScatter(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [[[1, 2], [2, 6]], [[1, 2], [2, 6]]]

        return test_scatter_drawing(
            self.all_figures(), 2, correct_data, DrawingLibrary.pandas
        )
