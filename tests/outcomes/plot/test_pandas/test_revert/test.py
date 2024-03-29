from hstest import TestedProgram
from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.pandas_handler import PandasHandler


class TestSeaborn(PlottingTest):
    @dynamic_test
    def test(self):
        import matplotlib

        PandasHandler.revert_plots()
        backend = matplotlib.get_backend()
        matplotlib.use('Agg')

        program = TestedProgram()
        program.start()

        matplotlib.use(backend)

        if len(self.all_figures()) != 0:
            return wrong(
                f'Expected 0 plots to be plotted using matplotlib library, '
                f'found {len(self.all_figures())}'
            )

        return correct()
