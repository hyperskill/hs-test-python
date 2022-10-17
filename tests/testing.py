import io
import re
import sys
import unittest
from importlib import import_module
from inspect import getmembers, isclass
from os import listdir
from os.path import abspath, dirname, isdir, isfile
from typing import List

content_path = dirname(
    dirname(abspath(__file__))
)
sys.path.insert(0, content_path)

from hstest.common import utils as hs  # noqa: E402
from hstest.dynamic.output.colored_output import GREEN_BOLD, RED_BOLD, RESET  # noqa: E402


class OutputForTest:
    def __init__(self, real_out: io.TextIOWrapper):
        self.original: io.TextIOWrapper = real_out

    def write(self, text):
        text = re.sub(r'(?<!\\)\\n', '\n', text)
        text = re.sub(r'(?<!\\)\\\'', '\'', text)
        text = re.sub(r'\\\\', r'\\', text)
        if 'FAIL' in text or 'Traceback' in text or 'failures' in text or 'ERROR' in text:
            self.original.write(RED_BOLD)
        else:
            self.original.write(GREEN_BOLD)
        self.original.write(text)
        self.original.write(RESET)

    def flush(self):
        self.original.flush()

    def close(self):
        self.original.close()


class UnitTesting:

    @staticmethod
    def test_all() -> bool:
        old_run = unittest.TestCase.run

        def run(self, result=None, repeats=0):
            failures_before = 0 if result is None else len(result.failures)
            test_result = old_run(self, result=result)
            is_project_test = 'tests.projects.' in str(self)
            if repeats == 5:  # max 5 times
                return test_result
            if is_project_test and test_result and failures_before < len(test_result.failures):
                print('Rerun project test')
                test_result.failures.pop()
                return run(self, result=test_result, repeats=repeats + 1)
            return test_result

        unittest.TestCase.run = run

        hs.failed_msg_start = ''
        hs.failed_msg_continue = ''
        hs.success_msg = ''

        tests_suite = []
        loader = unittest.TestLoader()

        for module in UnitTesting.find_modules(dirname(__file__)):
            if 'outcomes' in module and not module.endswith('.test') or \
                    'projects' in module and not module.endswith('.tests'):
                continue
            try:
                imported = import_module(f'tests.{module}')
            except ImportError:
                continue
            for name, obj in getmembers(imported):
                if isclass(obj) and issubclass(obj, unittest.TestCase):
                    tests_suite += [loader.loadTestsFromTestCase(obj)]

        suite = unittest.TestSuite(tests_suite[::-1])
        runner = unittest.TextTestRunner(stream=OutputForTest(sys.stdout), verbosity=2)
        result = runner.run(suite)
        return result.wasSuccessful()

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
                        modules += [curr_location[len(curr_dir) + 1:-3].replace('/', '.')]
                elif isdir(curr_location):
                    catalogs += [curr_location]

        return modules


if __name__ == '__main__':
    exit(0 if UnitTesting.test_all() else -1)
