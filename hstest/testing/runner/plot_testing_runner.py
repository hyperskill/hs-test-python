from typing import List, TYPE_CHECKING

from hstest.testing.plotting.drawing.drawing import Drawing
from hstest.testing.plotting.matplotlib_handler import MatplotlibHandler
from hstest.testing.plotting.pandas_handler import PandasHandler
from hstest.testing.plotting.seaborn_handler import SeabornHandler
from hstest.testing.runner.async_dynamic_testing_runner import AsyncDynamicTestingRunner

if TYPE_CHECKING:
    from hstest import TestCase


class DrawingsStorage:
    def __init__(self,
                 all_drawings: List[Drawing],
                 new_drawings: List[Drawing]):
        self.all_drawings: List[Drawing] = all_drawings
        self.new_drawings: List[Drawing] = new_drawings

    def append(self, drawing: Drawing):
        self.all_drawings.append(drawing)
        self.new_drawings.append(drawing)

    def extend(self, drawings: List[Drawing]):
        self.all_drawings.extend(drawings)
        self.new_drawings.extend(drawings)


class PlottingTestingRunner(AsyncDynamicTestingRunner):

    def __init__(self,
                 all_drawings: List[Drawing],
                 new_drawings: List[Drawing]):
        super().__init__()
        self.drawings_storage: DrawingsStorage = DrawingsStorage(
            all_drawings, new_drawings)

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
