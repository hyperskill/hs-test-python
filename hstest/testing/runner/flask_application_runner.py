from __future__ import annotations

import os
import sys
from time import sleep
from typing import TYPE_CHECKING

from hstest.common.process_utils import is_port_in_use
from hstest.exception.outcomes import ErrorWithFeedback, UnexpectedError
from hstest.test_case.attach.flask_settings import FlaskSettings
from hstest.test_case.check_result import CheckResult
from hstest.testing.process_wrapper import ProcessWrapper
from hstest.testing.runner.test_runner import TestRunner

if TYPE_CHECKING:
    from hstest.test_case.test_case import TestCase
    from hstest.testing.test_run import TestRun


class FlaskApplicationRunner(TestRunner):
    processes: list[tuple[str, ProcessWrapper]] = []

    def launch_flask_applications(self, test_case: TestCase) -> None:
        if not isinstance(test_case.attach, FlaskSettings):
            msg = (
                f"Flask tests should have FlaskSettings class as an attach, "
                f"found {type(test_case.attach)}"
            )
            raise UnexpectedError(msg)

        sources = test_case.attach.sources

        if len(sources) == 0:
            msg = "Cannot find Flask applications to run, no sources were defined in tests"
            raise UnexpectedError(msg)

        new_sources = []

        for source in sources:
            filename, port = source

            full_source = filename.replace(".", os.sep) + ".py"
            full_path = os.path.abspath(full_source)

            if not os.path.exists(full_path):
                msg = (
                    f'Cannot find file named "{os.path.basename(full_path)}" '
                    f'in folder "{os.path.dirname(full_path)}". '
                    f"Check if you deleted it."
                )
                raise ErrorWithFeedback(msg)

            if port is None:
                port = self.__find_free_port(test_case.attach.tryout_ports)

            process = ProcessWrapper(
                sys.executable, full_path, f"localhost:{port}", register_io_handler=True
            ).start()
            self.processes += [(full_source, process)]

            i: int = 100
            search_phrase = "Press CTRL+C to quit"
            while i:
                if search_phrase in process.stderr:
                    break
                i -= 1

                if process.is_error_happened():
                    i = 0
                else:
                    sleep(0.1)
            else:
                stdout = process.stdout.strip()
                stderr = process.stderr.strip()

                error_info = (
                    f"Cannot start Flask server {full_source} "
                    f'because cannot find "{search_phrase}" in process\' output'
                )

                if len(stdout):
                    error_info += "\n\nstdout:\n" + stdout
                if len(stderr):
                    error_info += "\n\nstderr:\n" + stderr

                raise ErrorWithFeedback(error_info)

            new_sources += [(filename, port)]

        test_case.attach.sources = new_sources

    def __find_free_port(self, ports: list[int]) -> int:
        for port in ports:
            if not is_port_in_use(port):
                return port
        msg = (
            "Cannot find a port to start Flask application "
            f"(tried ports form {ports[0]} to {ports[-1]})"
        )
        raise ErrorWithFeedback(msg)

    def set_up(self, test_case: TestCase) -> None:
        self.launch_flask_applications(test_case)

    def tear_down(self, test_case: TestCase) -> None:
        for process_item in self.processes:
            _filename, process = process_item
            process.terminate()

    def _check_errors(self) -> None:
        for process_item in self.processes:
            filename, process = process_item
            if process.is_error_happened():
                msg = f'Error running "{filename}"\n\n{process.stderr}'
                raise ErrorWithFeedback(msg)

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
