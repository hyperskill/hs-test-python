import inspect
import os


def get_main(filename: str = 'main') -> str:
    file = inspect.stack()[1].filename
    file = file.replace(os.sep, '.')[:-3]
    file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + filename
    return file
