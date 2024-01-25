from __future__ import annotations

import os
import sys
from time import sleep
from typing import TYPE_CHECKING

from hstest.common.file_utils import safe_delete
from hstest.common.process_utils import is_port_in_use
from hstest.exception.outcomes import ErrorWithFeedback, ExceptionWithFeedback, UnexpectedError
from hstest.test_case.attach.django_settings import DjangoSettings
from hstest.test_case.check_result import CheckResult
from hstest.testing.execution.filtering.file_filter import FileFilter
from hstest.testing.execution.searcher.python_searcher import PythonSearcher
from hstest.testing.process_wrapper import ProcessWrapper
from hstest.testing.runner.test_runner import TestRunner

if TYPE_CHECKING:
    from hstest.test_case.test_case import TestCase
    from hstest.testing.test_run import TestRun


class DjangoApplicationRunner(TestRunner):
    process: ProcessWrapper = None
    port: int | None = None
    full_path: str | None = None

    def launch_django_application(self, test_case: TestCase) -> None:
        if not isinstance(test_case.attach, DjangoSettings):
            msg = (
                f"Django tests should have DjangoSettings class as an attach, "
                f"found {type(test_case.attach)}"
            )
            raise UnexpectedError(msg)

        source = test_case.source_name

        if source is None or not len(source):
            source = "manage"

        full_source = source.replace(".", os.sep) + ".py"
        full_path = os.path.abspath(full_source)

        if not os.path.exists(full_path):
            filename = os.path.basename(full_source)
            runnable = PythonSearcher().search(file_filter=FileFilter(file=lambda f: f == filename))
            full_path = os.path.abspath(runnable.folder + os.sep + runnable.file)

        self.full_path = full_path
        self.port = self.__find_free_port(test_case.attach.tryout_ports)

        if test_case.attach.use_database:
            self.__prepare_database(test_case.attach.test_database)

        self.process = ProcessWrapper(
            sys.executable,
            self.full_path,
            "runserver",
            self.port,
            "--noreload",
            register_io_handler=True,
        ).start()

        i: int = 100
        search_phrase = "Starting development server at"
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

            error_info = (
                f"Cannot start Django server because cannot find "
                f'"{search_phrase}" in process\' output'
            )
            if len(stdout):
                error_info += "\n\nstdout:\n" + stdout
            if len(stderr):
                error_info += "\n\nstderr:\n" + stderr

            raise ErrorWithFeedback(error_info)

    def __find_free_port(self, ports: list[int]) -> int:
        for port in ports:
            if not is_port_in_use(port):
                return port
        msg = (
            "Cannot find a port to start Django application "
            f"(tried ports form {ports[0]} to {ports[-1]})"
        )
        raise ErrorWithFeedback(msg)

    def __prepare_database(self, test_database: str) -> None:
        os.environ["HYPERSKILL_TEST_DATABASE"] = test_database
        with open(test_database, "w", encoding="locale"):
            pass

        migrate = ProcessWrapper(sys.executable, self.full_path, "migrate", check_early_finish=True)
        migrate.start()

        while not migrate.is_finished() and len(migrate.stderr) == 0:
            sleep(0.01)

        if len(migrate.stderr) != 0:
            migrate.wait_output()

            if (
                "ModuleNotFoundError" in migrate.stderr
                or "ImportError" in migrate.stderr
                or "SyntaxError" in migrate.stderr
            ):
                raise ExceptionWithFeedback(migrate.stderr, None)

            # stdout and stderr is collected and will be shown to the user
            msg = "Cannot apply migrations to an empty database."
            raise ErrorWithFeedback(msg)

    def set_up(self, test_case: TestCase) -> None:
        self.launch_django_application(test_case)

    def tear_down(self, test_case: TestCase) -> None:
        self._check_errors()

        if isinstance(test_case.attach, DjangoSettings):
            safe_delete(test_case.attach.test_database)
        if self.process:
            self.process.terminate()

    def _check_errors(self) -> None:
        if self.process.is_error_happened():
            self.process.terminate()
            raise ErrorWithFeedback(self.process.stderr)

    def test(self, test_run: TestRun) -> CheckResult | None:
        self._check_errors()

        test_case = test_run.test_case

        try:
            result = test_case.dynamic_testing()
            self._check_errors()
            return result
        except BaseException as ex:
            test_run.set_error_in_test(ex)

        return CheckResult.from_error(test_run.error_in_test)
