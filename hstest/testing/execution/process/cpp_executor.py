import os

from hstest.common.os_utils import is_windows
from hstest.testing.execution.process_executor import ProcessExecutor
from hstest.testing.execution.searcher.cpp_searcher import CppSearcher


class CppExecutor(ProcessExecutor):
    def __init__(self, source_name: str = None):
        super().__init__(CppSearcher().find(source_name))

        self.without_extension = os.path.splitext(self.runnable.file)[0]

        if is_windows():
            self.executable = self.without_extension
            self.file_name = self.executable + '.exe'
        else:
            self.executable = f'./{self.without_extension}'
            self.file_name = self.without_extension

    def _compilation_command(self):
        return ['g++', '-std', 'c++20', '-pipe', '-O2', '-static', '-o', self.file_name, self.runnable.file]

    def _filter_compilation_error(self, error: str) -> str:
        return error

    def _execution_command(self, *args: str):
        return [self.executable] + list(args)

    def _cleanup(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
