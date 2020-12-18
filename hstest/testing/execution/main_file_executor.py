import os
import re
import runpy
import sys
from concurrent.futures import Future
from typing import Optional

from hstest.common.process_utils import DaemonThreadPoolExecutor
from hstest.dynamic.input.input_handler import InputHandler
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.security.exit_exception import ExitException
from hstest.exception.outcomes import ErrorWithFeedback, ExceptionWithFeedback
from hstest.testing.execution.program_executor import ProgramExecutor, ProgramState


class MainModuleExecutor(ProgramExecutor):
    _contents_cached = {}

    def __init__(self, source_name: str = None):
        super().__init__()

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
        self.path_to_test = os.path.join(self.folder_to_test, self.file_to_test)
        self.init_file = self.folder_to_test + os.sep + "__init__.py"

    def _init_by_nothing(self):
        for where, dirs, files in os.walk('.'):
            if where.startswith(f'.{os.sep}test{os.sep}'):
                continue

            if where == '.':
                for file in 'test.py', 'tests.py', '__init__.py':
                    if file in files:
                        files.remove(file)

            files = [f for f in files if f.endswith('.py')]

            if len(files) == 0:
                continue

            if len(files) == 1:
                without_py = files[0][:-3]
                self._init_by_module(os.path.abspath(where), without_py)
                return

            contents = {}

            for file in files:
                path = os.path.abspath(os.path.join(where, file))
                if path in self._contents_cached:
                    contents[file] = self._contents_cached[path]
                elif os.path.exists(path):
                    with open(path) as f:
                        c = f.read()
                        contents[file] = [
                            c,
                            re.compile(rf'(^|\n)import +[\w., ]*\b{file[:-3]}\b[\w., ]*', re.M),
                            re.compile(rf'(^|\n)from +\.? *\b{file[:-3]}\b +import +', re.M)
                        ]
                        self._contents_cached[path] = c

            is_imported = {f: False for f in files}
            has_name_main = {f: False for f in files}

            for file in files:
                source = contents[file][0]
                if '__name__' in source and '__main__' in source:
                    has_name_main[file] = True

                for f, (s, r1, r2) in contents.items():
                    if r1.search(source) is not None or r2.search(source) is not None:
                        is_imported[f] = True

            candidates_by_import = [f for f in files if not is_imported[f]]

            if len(candidates_by_import) == 1:
                without_py = candidates_by_import[0][:-3]
                self._init_by_module(os.path.abspath(where), without_py)
                return

            candidates_by_name_main = [f for f in files if has_name_main[f]]

            if len(candidates_by_name_main) == 1:
                without_py = candidates_by_name_main[0][:-3]
                self._init_by_module(os.path.abspath(where), without_py)
                return

            candidates_import_main = [f for f in candidates_by_import if has_name_main[f]]

            if len(candidates_import_main) == 1:
                without_py = candidates_import_main[0][:-3]
                self._init_by_module(os.path.abspath(where), without_py)
                return

            if len(candidates_import_main) > 1:
                str_files = ', '.join(f'"{f}"' for f in candidates_import_main)
                raise ErrorWithFeedback(
                    'Cannot decide which file to run out of the following: ' + str_files + '\n'
                    'They all have "if __name__ == \'__main__\'". Leave one file with this line.')

            str_files = ', '.join(f'"{f}"' for f in
                                  (candidates_by_import if len(candidates_by_import) else files))
            raise ErrorWithFeedback(
                'Cannot decide which file to run out of the following: ' + str_files + '\n'
                'Write "if __name__ == \'__main__\'" in one of them to mark it as an entry point.')

        raise ErrorWithFeedback(
            'Cannot find a file to import and run your code.\n'
            'Are your project files located at \"' + os.path.abspath('.') + '\"?')

    def _invoke_method(self, *args: str):
        modules_before = [k for k in sys.modules.keys()]

        from hstest.stage_test import StageTest
        try:
            self._machine.set_state(ProgramState.RUNNING)

            sys.argv = [self.file_to_test] + list(args)
            sys.path.append(self.folder_to_test)

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

    def _launch(self, *args: str):
        from hstest.stage_test import StageTest
        test_num = StageTest.curr_test_run.test_num

        InputHandler.set_dynamic_input_func(lambda: self._request_input())
        self.__executor = DaemonThreadPoolExecutor(name=f"MainModuleExecutor test #{test_num}")
        self.__task = self.__executor.submit(lambda: self._invoke_method(*args))

    def stop(self):
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
