import os
import subprocess
import sys
from typing import Optional

from hstest.common.file_utils import safe_delete
from hstest.common.process_utils import is_port_in_use
from hstest.exception.outcomes import ErrorWithFeedback, TestPassed, WrongAnswer
from hstest.test_case.attach.django_settings import DjangoSettings
from hstest.test_case.check_result import CheckResult
from hstest.test_case.test_case import TestCase
from hstest.testing.runner.test_runner import TestRunner
from hstest.testing.test_run import TestRun


class DjangoApplicationRunner(TestRunner):

    tryout_ports = [i for i in range(8000, 8101)]
    TEST_DATABASE = 'db.test.sqlite3'

    process: Optional[subprocess.Popen] = None
    port: Optional[int] = None
    full_path: Optional[str] = None

    def launch_django_application(self, test_case: TestCase):
        source = test_case.source_name

        if source is None:
            source = 'manage'

        full_source = source.replace('.', os.sep) + '.py'
        full_path = os.path.abspath(full_source)

        if not os.path.exists(full_path):
            raise ErrorWithFeedback(
                f'Cannot find file named "{os.path.dirname(full_path)}" '
                f'in folder "{os.path.dirname(full_path)}". '
                f'Check if you deleted it.')

        self.full_path = full_path
        self.port = self.__find_free_port()

        if isinstance(test_case.attach, DjangoSettings):
            if test_case.attach.use_database:
                self.__prepare_database()

        self.process = subprocess.Popen(
            [sys.executable, self.full_path, 'runserver', str(self.port), '--noreload'],
            stdout=subprocess.STDOUT,
            stderr=subprocess.STDOUT
        )

    def __find_free_port(self) -> int:
        for port in self.tryout_ports:
            if not is_port_in_use(port):
                return port
        raise ErrorWithFeedback(
            'Cannot find a port to start Django application '
            f'(tried ports form {self.tryout_ports[0]} to {self.tryout_ports[-1]})')

    def __prepare_database(self):
        os.environ['HYPERSKILL_TEST_DATABASE'] = self.TEST_DATABASE
        with open(self.TEST_DATABASE, 'w'):
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
        safe_delete(self.TEST_DATABASE)
        if self.process:
            self.process.terminate()

    def test(self, test_run: TestRun) -> Optional[CheckResult]:
        test_case = test_run.test_case

        try:
            return test_case.dynamic_testing()
        except BaseException as ex:
            test_run.set_error_in_test(ex)

        error = test_run.error_in_test

        if isinstance(error, TestPassed):
            return CheckResult.correct()
        elif isinstance(error, WrongAnswer):
            return CheckResult.wrong(error.feedback)
        else:
            return None
