import os
import runpy
import sys
from concurrent.futures import Future
from typing import Optional

from hstest.common.process_utils import DaemonThreadPoolExecutor
from hstest.dynamic.security.exit_exception import ExitException
from hstest.dynamic.security.thread_group import ThreadGroup
from hstest.dynamic.system_handler import SystemHandler
from hstest.exception.outcomes import ExceptionWithFeedback
from hstest.testing.execution.program_executor import ProgramExecutor, ProgramState
from hstest.testing.execution.searcher.python_searcher import PythonSearcher


class MainModuleExecutor(ProgramExecutor):
    def __init__(self, source_name: str = None):
        super().__init__()
        self.runnable = PythonSearcher().find(source_name)
        self.__executor: Optional[DaemonThreadPoolExecutor] = None
        self.__task: Optional[Future] = None
        self.__group = None

    def _invoke_method(self, *args: str):
        modules_before = [k for k in sys.modules.keys()]
        working_directory_before = os.path.abspath(os.getcwd())

        from hstest.stage_test import StageTest
        try:
            self._machine.set_state(ProgramState.RUNNING)

            sys.argv = [self.runnable.file] + list(args)
            sys.path.insert(0, self.runnable.folder)

            runpy.run_module(
                self.runnable.module,
                run_name="__main__"
            )

            self._machine.set_state(ProgramState.FINISHED)

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
            modules_to_delete = []
            for m in sys.modules:
                if m not in modules_before:
                    modules_to_delete += [m]
            for m in modules_to_delete:
                del sys.modules[m]
            sys.path.remove(self.runnable.folder)
            os.chdir(working_directory_before)

    def _launch(self, *args: str):
        from hstest.stage_test import StageTest
        test_num = StageTest.curr_test_run.test_num

        self.__group = ThreadGroup()

        SystemHandler.install_handler(
            self,
            lambda: ThreadGroup.curr_group() == self.__group,
            lambda: self.request_input()
        )

        self.__executor = DaemonThreadPoolExecutor(
            name=f"MainModuleExecutor test #{test_num}", group=self.__group)

        self.__task = self.__executor.submit(lambda: self._invoke_method(*args))

    def _terminate(self):
        self.__executor.shutdown(wait=False)
        self.__task.cancel()
        with self._machine.cv:
            while not self.is_finished():
                self._input = None
                self._machine.wait_not_state(ProgramState.RUNNING)
                if self.is_waiting_input():
                    self._machine.set_state(ProgramState.RUNNING)

    def __str__(self) -> str:
        return self.runnable.file
