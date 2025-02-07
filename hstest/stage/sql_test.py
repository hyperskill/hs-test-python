from __future__ import annotations

from typing import Any, ClassVar

from hstest.exception.outcomes import WrongAnswer
from hstest.stage.stage_test import StageTest
from hstest.testing.runner.sql_runner import SQLRunner


class SQLTest(StageTest):
    queries: ClassVar[dict[str, str]] = {}
    db: Any = None

    def __init__(self, source: str = "") -> None:
        super().__init__(source)
        self.runner = SQLRunner(self)

    def execute(self, query_name: str) -> Any:
        cursor = self.db.cursor()

        if query_name not in self.queries:
            return cursor.execute(query_name)

        try:
            return cursor.execute(self.queries[query_name])
        except Exception as ex:
            msg = f"Error while running '{query_name}': \n\n{ex}"
            raise WrongAnswer(msg) from ex

    def execute_and_fetch_all(self, query_name: str) -> list[tuple]:
        return self.execute(query_name).fetchall()
