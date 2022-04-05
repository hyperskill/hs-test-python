from hstest.stage.stage_test import StageTest
from hstest.testing.runner.sql_runner import SQLRunner


class SQLTest(StageTest):
    queries = dict()

    def __init__(self, args='', *, source: str = ''):
        self.runner = SQLRunner(self)
        super().__init__(args, source=source)
