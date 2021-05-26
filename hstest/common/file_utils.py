import os
from typing import Dict

from hstest.exception.testing import FileDeletionError


def create_files(files: Dict[str, str]):
    for file, content in files.items():
        with open(file, 'w') as f:
            f.write(content)


def delete_files(files: Dict[str, str]):
    for file in files.keys():
        if os.path.isfile(file):
            try:
                os.remove(file)
            except PermissionError:
                raise FileDeletionError()


def safe_delete(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except BaseException:
            pass
