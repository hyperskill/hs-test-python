from hstest.testing.execution.filtering.file_filter import File, Folder


class RunnableFile:
    def __init__(self, folder: Folder, file: File):
        self.folder = folder
        self.file = file
