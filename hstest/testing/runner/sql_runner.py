from __future__ import annotations

import contextlib
import re
import sqlite3
import typing

from hstest.exceptions import WrongAnswer
from hstest.test_case.check_result import CheckResult
from hstest.testing.execution.searcher.sql_searcher import SQLSearcher
from hstest.testing.runner.test_runner import TestRunner

if typing.TYPE_CHECKING:
    from hstest import SQLTest
    from hstest.testing.test_run import TestCase, TestRun


class SQLRunner(TestRunner):
    def __init__(self, sql_test_cls: type[SQLTest]) -> None:
        self.sql_test_cls = sql_test_cls
        super().__init__()

    def test(self, test_run: TestRun) -> CheckResult | None:
        test_case = test_run.test_case

        try:
            return test_case.dynamic_testing()
        except BaseException as ex:
            test_run.set_error_in_test(ex)

        return CheckResult.from_error(test_run.error_in_test)

    def set_up(self, test_case: TestCase) -> None:
        self.parse_sql_file()
        self.set_up_database()

    def set_up_database(self) -> None:
        if self.sql_test_cls.db is not None:
            return

        self.sql_test_cls.db = sqlite3.connect(":memory:")

    def parse_sql_file(self) -> None:
        file_path = SQLSearcher().search().path()
        lines = file_path.read_text(encoding="locale").splitlines()

        sql_content = " ".join(lines).replace("\n", "")
        commands = re.findall(r'(\w+)\s+?=\s+?"(.*?)"', sql_content)

        for name, query in commands:
            if not query:
                msg = f"The '{name}' query shouldn't be empty!"
                raise WrongAnswer(msg)
            if name in self.sql_test_cls.queries:
                self.sql_test_cls.queries[name] = query

        for name in self.sql_test_cls.queries:
            if self.sql_test_cls.queries[name] is None:
                msg = f"Can't find '{name}' query from SQL files!"
                raise WrongAnswer(msg)

    def tear_down(self, test_case: TestCase) -> None:
        with contextlib.suppress(Exception):
            self.sql_test_cls.db.close()
