from __future__ import annotations

import contextlib
import os

from hstest.exception.testing import FileDeletionError


def create_files(files: dict[str, str]) -> None:
    for file, content in files.items():
        with open(file, "w", encoding="locale") as f:
            f.write(content)


def delete_files(files: dict[str, str]) -> None:
    for file in files:
        if os.path.isfile(file):
            try:
                os.remove(file)
            except PermissionError:
                raise FileDeletionError


def safe_delete(filename) -> None:
    if os.path.exists(filename):
        with contextlib.suppress(BaseException):
            os.remove(filename)


def walk_user_files(folder):
    curr_folder = os.path.abspath(folder)
    test_folder = os.path.join(curr_folder, "test")

    for folder, dirs, files in os.walk(curr_folder):
        if folder.startswith(test_folder):
            continue

        if folder == curr_folder:
            for file in "test.py", "tests.py":
                if file in files:
                    files.remove(file)

        yield folder, dirs, files
