from hstest.exception.outcomes import WrongAnswer
from hstest.stage.stage_test import StageTest
from hstest.testing.runner.sql_runner import SQLRunner


class SQLTest(StageTest):
    queries: dict[str, str] = dict()
    db: any = None

    def __init__(self, args='', *, source: str = ''):
        self.runner = SQLRunner(self)
        super().__init__(args, source=source)

    def execute(self, query_name: str):
        query = self.queries[query_name] if query_name in self.queries else query_name
        cursor = self.db.cursor()
        try:
            return cursor.execute(query)
        except Exception as ex:
            raise WrongAnswer(str(ex))

    def executeAndFetchAll(self, query_name: str):
        return self.execute(query_name).fetchall()
