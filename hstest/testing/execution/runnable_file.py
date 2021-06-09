
file_contents_cached = {}


class RunnableFile:
    def __init__(self, file: str, folder: str):
        self.file = file
        self.folder = folder
