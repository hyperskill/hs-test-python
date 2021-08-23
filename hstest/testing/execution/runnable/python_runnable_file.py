from hstest.testing.execution.runnable.runnable_file import RunnableFile


class PythonRunnableFile(RunnableFile):
    def __init__(self, folder: str, file: str, module: str):
        super().__init__(folder, file)
        self.module = module
