from __future__ import annotations

import contextlib
import os
from pathlib import Path

from hstest.exception.testing import FileDeletionError


def create_files(files: dict[str, str]) -> None:
    for file, content in files.items():
        Path(file).write_text(content, encoding="locale")


def delete_files(files: dict[str, str]) -> None:
    for file in map(Path, files):
        if file.is_file():
            try:
                file.unlink()
            except PermissionError as ex:
                raise FileDeletionError from ex


def safe_delete(filename: str) -> None:
    with contextlib.suppress(BaseException):
        Path(filename).unlink(missing_ok=True)


def walk_user_files(curr_folder: Path) -> tuple[Path, list[str], list[str]]:
    curr_folder = curr_folder.resolve()
    test_folder = curr_folder / "test"

    for folder, dirs, files in os.walk(curr_folder):
        folder_ = Path(folder)
        if folder_.is_relative_to(test_folder):
            continue

        if folder_ == curr_folder:
            for file in ("test.py", "tests.py"):
                if file in files:
                    files.remove(file)

        yield Path(folder_), dirs, files
