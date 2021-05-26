import os
import runpy
import sys
from concurrent.futures import Future
from typing import Optional

from hstest.common.process_utils import DaemonThreadPoolExecutor
from hstest.dynamic.file_searcher import runnable_searcher
from hstest.dynamic.input.input_handler import InputHandler
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.security.exit_exception import ExitException
from hstest.exception.outcomes import ExceptionWithFeedback
from hstest.testing.execution.program_executor import ProgramExecutor, ProgramState


class MainModuleExecutor(ProgramExecutor):
    def __init__(self, source_name: str = None):
        super().__init__()

        if source_name is None:
            from hstest.stage_test import StageTest
            source_name = StageTest.curr_test_run.test_case.source_name

        if source_name is None:
            self._init_by_nothing()
        else:
            self._init_by_source_name(source_name)

        self.__module_name: str = source_name
        self.__run_module = None
        self.__executor: Optional[DaemonThreadPoolExecutor] = None
        self.__task: Optional[Future] = None

    def _init_by_source_name(self, source: str):
        path_to_test = source.replace('.', os.sep) + '.py'
        if not os.path.exists(path_to_test):
            self._init_by_nothing()
            return

        path, sep, module = source.rpartition('.')
        module_abs_path = os.path.abspath(path.replace('.', os.sep))
        self._init_by_module(module_abs_path, module)

    def _init_by_module(self, module_abs_path: str, module_name: str):
        self.module_to_test = module_name
        self.file_to_test = module_name + '.py'
        self.folder_to_test = module_abs_path

    def _init_by_nothing(self):
        folder, file = runnable_searcher()
        without_py = file[:-3]
        self._init_by_module(os.path.abspath(folder), without_py)

    def _invoke_method(self, *args: str):
        modules_before = [k for k in sys.modules.keys()]
        working_directory_before = os.path.abspath(os.getcwd())

        from hstest.stage_test import StageTest
        try:
            self._machine.set_state(ProgramState.RUNNING)

            sys.argv = [self.file_to_test] + list(args)
            sys.path.insert(0, self.folder_to_test)

            runpy.run_module(
                self.module_to_test,
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
            sys.path.remove(self.folder_to_test)
            os.chdir(working_directory_before)

    def _launch(self, *args: str):
        from hstest.stage_test import StageTest
        test_num = StageTest.curr_test_run.test_num

        InputHandler.set_dynamic_input_func(lambda: self._request_input())
        self.__executor = DaemonThreadPoolExecutor(name=f"MainModuleExecutor test #{test_num}")
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

    def get_output(self) -> str:
        return OutputHandler.get_partial_output()

    def __str__(self) -> str:
        return self.file_to_test
