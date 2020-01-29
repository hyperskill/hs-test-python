import sys
import io
import re
from typing import List
from unittest import TestLoader, TextTestRunner, TestSuite, TestCase
from inspect import getmembers, isclass
from importlib import import_module
from os.path import dirname, isfile, isdir
from os import listdir
import hstest.utils as hs


class OutputForTest:
    def __init__(self, real_out: io.TextIOWrapper):
        self.original: io.TextIOWrapper = real_out

    def write(self, text):
        text = re.sub(r'(?<!\\)\\n', '\n', text)
        text = re.sub(r'(?<!\\)\\t', '\t', text)
        text = re.sub(r'(?<!\\)\\\'', '\'', text)
        text = re.sub(r'\\\\', r'\\', text)
        if 'FAIL' in text or 'Traceback' in text or 'failures' in text:
            self.original.write("\033[1;31m")
        else:
            self.original.write("\033[1;32m")
        self.original.write(text)
        self.original.write("\033[0m")

    def flush(self):
        self.original.flush()

    def close(self):
        self.original.close()


class UnitTesting:

    @staticmethod
    def test_all() -> bool:

        hs.failed_msg_start = ''
        hs.failed_msg_continue = ''
        hs.success_msg = ''

        tests_suite = []
        loader = TestLoader()

        for module in UnitTesting.find_modules(dirname(__file__)):
            if module.endswith('.program'):
                continue
            imported = import_module(f'tests.{module}')
            for name, obj in getmembers(imported):
                if isclass(obj) and issubclass(obj, TestCase):
                    tests_suite += [loader.loadTestsFromTestCase(obj)]

        suite = TestSuite(tests_suite)
        runner = TextTestRunner(stream=OutputForTest(sys.stdout), verbosity=2)
        return runner.run(suite).wasSuccessful()

    @staticmethod
    def find_modules(from_directory: str) -> List[str]:

        catalogs = [from_directory]
        curr_dir = from_directory

        modules = []

        while catalogs:
            curr_catalog = catalogs.pop()
            for file in listdir(curr_catalog):
                curr_location = curr_catalog + '/' + file
                if file.startswith('__'):
                    continue
                if isfile(curr_location):
                    if file.endswith('.py'):
                        modules += [curr_location[len(curr_dir)+1:-3].replace('/', '.')]
                elif isdir(curr_location):
                    catalogs += [curr_location]

        return modules


if __name__ == '__main__':
    exit(0 if UnitTesting.test_all() else -1)
