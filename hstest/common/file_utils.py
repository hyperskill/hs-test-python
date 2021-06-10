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


def walk_user_files(folder):
    curr_folder = os.path.abspath(folder)
    test_folder = os.path.join(curr_folder, 'test')

    for folder, dirs, files in os.walk(curr_folder):
        if folder.startswith(test_folder):
            continue

        if folder == curr_folder:
            for file in 'test.py', 'tests.py':
                if file in files:
                    files.remove(file)

        yield folder, dirs, files
