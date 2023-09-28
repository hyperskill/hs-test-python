import os
from typing import List

from hstest.testing.execution.process_executor import ProcessExecutor
from hstest.testing.execution.runnable.runnable_file import RunnableFile


class CppExecutor(ProcessExecutor):
    def __init__(self, runnable: RunnableFile, executable_name: str):
        super().__init__(runnable)
        self.executable_name = executable_name

    def _compilation_command(self, *args: str) -> List[str]:
        return ["g++", self.runnable.file, "-o", self.executable_name]

    def _execution_command(self, *args: str) -> List[str]:
        return [os.path.join(self.runnable.folder, self.executable_name)] + list(args)

    def _cleanup(self):
        os.remove(os.path.join(self.runnable.folder, self.executable_name))
