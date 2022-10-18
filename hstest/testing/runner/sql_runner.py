import os
import re
import sqlite3
import typing

from hstest.exceptions import WrongAnswer
from hstest.test_case.check_result import CheckResult
from hstest.testing.execution.searcher.sql_searcher import SQLSearcher
from hstest.testing.runner.test_runner import TestRunner

if typing.TYPE_CHECKING:
    from hstest.testing.test_run import TestCase, TestRun


class SQLRunner(TestRunner):

    def __init__(self, sql_test_cls):
        self.sql_test_cls = sql_test_cls
        super(SQLRunner, self).__init__()

    def test(self, test_run: 'TestRun'):
        test_case = test_run.test_case

        try:
            result = test_case.dynamic_testing()
            return result
        except BaseException as ex:
            test_run.set_error_in_test(ex)

        return CheckResult.from_error(test_run.error_in_test)

    def set_up(self, test_case: 'TestCase'):
        self.parse_sql_file()
        self.set_up_database()

    def set_up_database(self):
        if self.sql_test_cls.db is not None:
            return

        self.sql_test_cls.db = sqlite3.connect(':memory:')

    def parse_sql_file(self) -> None:
        sql_file = SQLSearcher().search()
        file_path = os.path.join(sql_file.folder, sql_file.file)

        with open(file_path, 'r') as file:
            lines = file.readlines()
            sql_content = " ".join(lines).replace("\n", "")
            commands = re.findall(r'(\w+)\s+?=\s+?"(.*?)"', sql_content)

            for (name, query) in commands:
                if not query:
                    raise WrongAnswer(f"The '{name}' query shouldn't be empty!")
                if name in self.sql_test_cls.queries:
                    self.sql_test_cls.queries[name] = query

            for name in self.sql_test_cls.queries:
                if self.sql_test_cls.queries[name] is None:
                    raise WrongAnswer(f"Can't find '{name}' query from SQL files!")

    def tear_down(self, test_case: 'TestCase'):
        try:
            self.sql_test_cls.db.close()
        except Exception:
            pass
