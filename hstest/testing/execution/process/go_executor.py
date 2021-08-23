import os

from hstest.common.os_utils import is_windows
from hstest.testing.execution.process_executor import ProcessExecutor
from hstest.testing.execution.searcher.go_searcher import GoSearcher


class GoExecutor(ProcessExecutor):
    def __init__(self, source_name: str = None):
        super().__init__(GoSearcher().find(source_name))

        self.without_go = self.runnable.file[:-3]

        if is_windows():
            self.executable = self.without_go
            self.file_name = self.executable + '.exe'
        else:
            self.executable = f'./{self.without_go}'
            self.file_name = self.executable

    def _compilation_command(self):
        return ['go', 'build', self.runnable.file]

    def _execution_command(self, *args: str):
        return [self.executable] + list(args)

    def _cleanup(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
