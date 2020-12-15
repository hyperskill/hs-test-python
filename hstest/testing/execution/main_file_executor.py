import os
import runpy
import sys
from concurrent.futures import Future
from typing import Optional

from hstest.common.process_utils import DaemonThreadPoolExecutor
from hstest.common.utils import get_stacktrace
from hstest.dynamic.input.input_handler import InputHandler
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.security.exit_exception import ExitException
from hstest.exception.outcomes import ErrorWithFeedback, ExceptionWithFeedback
from hstest.testing.execution.program_executor import ProgramExecutor, ProgramState


class MainModuleExecutor(ProgramExecutor):
    def __init__(self, source_name: str = None):
        super().__init__()
        self.__module_name: str = source_name
        self.__run_module = None
        self.__executor: Optional[DaemonThreadPoolExecutor] = None
        self.__task: Optional[Future] = None

        self.source_name = source_name
        self.module_to_test = source_name
        self.path_to_test = source_name.replace('.', os.sep) + '.py'
        self.folder_to_test = os.path.dirname(self.path_to_test)
        self.init_file = self.folder_to_test + os.sep + "__init__.py"
        self.full_file_to_test = ''
        self.need_reload = False

    def _invoke_method(self, *args: str):
        from hstest.stage_test import StageTest
        try:
            self._machine.set_state(ProgramState.RUNNING)

            sys.argv = [self.path_to_test] + list(args)
            sys.path += [self.folder_to_test]
            if os.path.exists(self.folder_to_test):
                open(self.init_file, 'a').close()
            runpy.run_module(
                self.module_to_test,
                run_name="__main__"
            )

            self._machine.set_state(ProgramState.FINISHED)

        except ImportError as ex:
            error_text = get_stacktrace(self.path_to_test, ex, hide_internals=True)
            StageTest.curr_test_run.set_error_in_test(ErrorWithFeedback(error_text))
            self._machine.set_state(ProgramState.EXCEPTION_THROWN)

        except BaseException as ex:
            if StageTest.curr_test_run.error_in_test is None:
                # ExitException is thrown in case of exit() or quit()
                # consider them like normal exit
                if isinstance(ex, ExitException):
                    self._machine.set_state(ProgramState.FINISHED)
                    return

                StageTest.curr_test_run.set_error_in_test(ExceptionWithFeedback('', ex))

            self._machine.set_state(ProgramState.EXCEPTION_THROWN)

        finally:
            try:
                os.remove(self.init_file)
            except OSError:
                pass
            sys.path.pop()

    def _launch(self, *args: str):
        InputHandler.set_dynamic_input_func(lambda: self._request_input())
        self.__executor = DaemonThreadPoolExecutor()
        self.__task = self.__executor.submit(lambda: self._invoke_method(*args))

    def stop(self):
        self.__executor.shutdown()
        self.__task.cancel()
        with self._machine.cv:
            while not self.is_finished():
                self._input = None
                self._machine.wait_not_state(ProgramState.RUNNING)
                if self.is_waiting_input():
                    self._machine.set_state(ProgramState.RUNNING)

    def get_output(self) -> str:
        return OutputHandler.get_partial_output()

    def __str__(self) -> str:
        return self.__module_name
