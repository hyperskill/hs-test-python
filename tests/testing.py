import io
import re
import sys
import time
import unittest
from importlib import import_module
from inspect import getmembers, isclass
from os import listdir
from os.path import dirname, isdir, isfile
from typing import List
from unittest import TestLoader, TestSuite, TextTestRunner

import hstest.common.utils as hs
from hstest.dynamic.output.colored_output import GREEN_BOLD, RED_BOLD, RESET


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


class TestSuiteWithDelay(TestSuite):
    def run(self, result, debug=False):
        def _isnotsuite(test):
            "A crude way to tell apart testcases and suites with duck-typing"
            try:
                iter(test)
            except TypeError:
                return True
            return False

        topLevel = False
        if getattr(result, '_testRunEntered', False) is False:
            result._testRunEntered = topLevel = True

        for index, test in enumerate(self):
            if result.shouldStop:
                break

            if _isnotsuite(test):
                self._tearDownPreviousClass(test, result)
                self._handleModuleFixture(test, result)
                self._handleClassSetUp(test, result)
                result._previousTestClass = test.__class__

                if (getattr(test.__class__, '_classSetupFailed', False) or
                    getattr(result, '_moduleSetUpFailed', False)):
                    continue

            if not debug:
                test(result)
            else:
                test.debug()

            time.sleep(1 / 100)

            if self._cleanup:
                self._removeTestAtIndex(index)

        if topLevel:
            self._tearDownPreviousClass(None, result)
            self._handleModuleTearDown(result)
            result._testRunEntered = False
        return


class UnitTesting:

    @staticmethod
    def test_all() -> bool:

        hs.failed_msg_start = ''
        hs.failed_msg_continue = ''
        hs.success_msg = ''

        tests_suite = []
        loader = TestLoader()

        for module in UnitTesting.find_modules(dirname(__file__)):
            if 'outcomes' in module and not module.endswith('.test') or \
                    'projects' in module and not module.endswith('.tests'):
                continue
            try:
                imported = import_module(f'tests.{module}')
            except ImportError as e:
                continue
            for name, obj in getmembers(imported):
                if isclass(obj) and issubclass(obj, unittest.TestCase):
                    tests_suite += [loader.loadTestsFromTestCase(obj)]

        suite = TestSuiteWithDelay(tests_suite[::-1])
        runner = TextTestRunner(stream=OutputForTest(sys.stdout), verbosity=2)
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
