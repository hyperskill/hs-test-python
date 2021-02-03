import os
import subprocess
import sys
from time import sleep
from typing import List, Optional

from hstest.common.file_utils import safe_delete
from hstest.common.process_utils import is_port_in_use
from hstest.exception.outcomes import ErrorWithFeedback, TestPassed, UnexpectedError, WrongAnswer
from hstest.test_case.attach.django_settings import DjangoSettings
from hstest.test_case.check_result import CheckResult
from hstest.test_case.test_case import TestCase
from hstest.testing.popen_wrapper import PopenWrapper
from hstest.testing.runner.test_runner import TestRunner
from hstest.testing.test_run import TestRun


class DjangoApplicationRunner(TestRunner):
    process: PopenWrapper = None
    port: Optional[int] = None
    full_path: Optional[str] = None

    def launch_django_application(self, test_case: TestCase):
        if not isinstance(test_case.attach, DjangoSettings):
            raise UnexpectedError(
                f'Django tests should have DjangoSettings class as an attach, '
                f'found {type(test_case.attach)}')

        source = test_case.source_name

        if source is None:
            source = 'manage'

        full_source = source.replace('.', os.sep) + '.py'
        full_path = os.path.abspath(full_source)

        if not os.path.exists(full_path):
            raise ErrorWithFeedback(
                f'Cannot find file named "{os.path.basename(full_path)}" '
                f'in folder "{os.path.dirname(full_path)}". '
                f'Check if you deleted it.')

        self.full_path = full_path
        self.port = self.__find_free_port(test_case.attach.tryout_ports)

        if test_case.attach.use_database:
            self.__prepare_database(test_case.attach.test_database)

        self.process = PopenWrapper(
            sys.executable, self.full_path, 'runserver', self.port, '--noreload')

        i: int = 100
        search_phrase = 'Starting development server at'
        while i:
            if search_phrase in self.process.stdout:
                test_case.attach.port = self.port
                break
            i -= 1

            if self.process.is_error_happened():
                i = 0
            else:
                sleep(0.1)
        else:
            stdout = self.process.stdout.strip()
            stderr = self.process.stderr.strip()

            error_info = f'Cannot start Django server because cannot find "{search_phrase}" in process\' output'
            if len(stdout):
                error_info += '\n\nstdout:\n' + stdout
            if len(stderr):
                error_info += '\n\nstderr:\n' + stderr

            raise ErrorWithFeedback(error_info)

    def __find_free_port(self, ports: List[int]) -> int:
        for port in ports:
            if not is_port_in_use(port):
                return port
        raise ErrorWithFeedback(
            'Cannot find a port to start Django application '
            f'(tried ports form {ports[0]} to {ports[-1]})')

    def __prepare_database(self, test_database: str):
        os.environ['HYPERSKILL_TEST_DATABASE'] = test_database
        with open(test_database, 'w'):
            pass
        migrate = subprocess.Popen(
            [sys.executable, self.full_path, 'migrate'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        exit_code = migrate.wait()
        if exit_code != 0:
            stdout = migrate.stdout.read().decode().strip()
            stderr = migrate.stderr.read().decode().strip()

            error_info = 'Cannot apply migrations to an empty database.'
            if len(stdout):
                error_info += '\n\nstdout:\n' + stdout.strip()
            if len(stderr):
                error_info += '\n\nstderr:\n' + stderr.strip()

            raise ErrorWithFeedback(error_info)

    def set_up(self, test_case: TestCase):
        self.launch_django_application(test_case)

    def tear_down(self, test_case: TestCase):
        if isinstance(test_case.attach, DjangoSettings):
            safe_delete(test_case.attach.test_database)
        if self.process:
            self.process.terminate()

    def _check_errors(self):
        if self.process.is_error_happened():
            self.process.terminate()
            raise ErrorWithFeedback(self.process.stderr)

    def test(self, test_run: TestRun) -> Optional[CheckResult]:
        self._check_errors()

        test_case = test_run.test_case

        try:
            result = test_case.dynamic_testing()
            self._check_errors()
            return result
        except BaseException as ex:
            test_run.set_error_in_test(ex)

        error = test_run.error_in_test

        if isinstance(error, TestPassed):
            return CheckResult.correct()
        elif isinstance(error, WrongAnswer):
            return CheckResult.wrong(error.feedback)
        else:
            return None
