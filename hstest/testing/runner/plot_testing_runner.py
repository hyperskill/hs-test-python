import typing

from hstest.testing.runner.async_dynamic_testing_runner import AsyncDynamicTestingRunner

from hstest.testing.plotting.matplotlib_handler import MatplotlibHandler
from hstest.testing.plotting.pandas_handler import PandasHandler
from hstest.testing.plotting.seaborn_handler import SeabornHandler

if typing.TYPE_CHECKING:
    from hstest import TestCase


class PlottingTestingRunner(AsyncDynamicTestingRunner):

    def __init__(self, drawings):
        super().__init__()
        self.drawings_storage = drawings

    def set_up(self, test_case: 'TestCase'):
        super().set_up(test_case)
        self.replace_plots()

    def tear_down(self, test_case: 'TestCase'):
        super().tear_down(test_case)
        self.revert_plots()

    def replace_plots(self):
        MatplotlibHandler.replace_plots(self.drawings_storage)
        PandasHandler.replace_plots(self.drawings_storage)
        SeabornHandler.replace_plots(self.drawings_storage)

    def revert_plots(self):
        MatplotlibHandler.revert_plots()
        PandasHandler.revert_plots()
        SeabornHandler.revert_plots()
