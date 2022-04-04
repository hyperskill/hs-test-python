import os
import re
import sqlite3

from exception.outcomes import ErrorWithFeedback
from hstest.stage.stage_test import StageTest
from hstest.testing.runner.sql_runner import SQLRunner


class SQLTest(StageTest):
    runner = SQLRunner()
    queries = dict()

    def __init__(self, args='', *, source: str = ''):
        self.find_sql_files()
        self.db = sqlite3.connect(':memory:')
        super().__init__(args, source=source)

    def find_sql_files(self):
        root_folder = os.getcwd()
        is_sql_file_found: bool = False

        for file in os.listdir(root_folder):
            if file.endswith('.sql'):
                is_sql_file_found = True
                self.parse_sql_file(file)

        if not is_sql_file_found:
            raise ErrorWithFeedback("Can't find any SQL file!")

    def parse_sql_file(self, file_name: str) -> None:
        file_path = os.path.join(os.getcwd(), file_name)

        with open(file_path, 'r') as file:
            lines = file.readlines()
            sql_content = " ".join(lines).replace("\n", "")
            commands = re.findall("(\\w+)\\s+?=\\s+?\"(.+?)\"", sql_content)

            for (name, query) in commands:
                if name in self.queries:
                    self.queries[name] = query
