from __future__ import annotations

import inspect
import itertools
import os

from hstest.exception.failure_handler import get_traceback_stack


def is_tests(stage):
    package = inspect.getmodule(stage).__package__
    file = inspect.getmodule(stage).__file__
    return (
        (package and package.startswith("tests.outcomes."))
        or (package and package.startswith("tests.projects."))
        or (file and f"{os.sep}hs-test-python{os.sep}tests{os.sep}outcomes{os.sep}" in file)
        or (file and f"{os.sep}hs-test-python{os.sep}tests{os.sep}projects{os.sep}" in file)
        or (file and f"{os.sep}hs-test-python{os.sep}tests{os.sep}sql{os.sep}" in file)
    )


def setup_cwd(stage) -> None:
    if stage.is_tests:
        test_file = inspect.getmodule(stage).__file__
        test_folder = os.path.dirname(test_file)
        os.chdir(test_folder)

    if os.path.basename(os.getcwd()) == "test":
        os.chdir(os.path.dirname(os.getcwd()))


def get_stacktrace(ex: BaseException, hide_internals=False) -> str:
    traceback_stack = get_traceback_stack(ex)

    if not hide_internals:
        return "".join(traceback_stack)

    if isinstance(ex, SyntaxError):
        if ex.filename.startswith("<"):  # "<string>", or "<module>"
            user_dir = ex.filename
        else:
            user_dir = os.path.dirname(ex.filename) + os.sep
    else:
        user_dir = ""

    user_traceback = []
    for tr in traceback_stack[::-1][1:-1]:
        if f'{os.sep}runpy.py"' in tr:
            break
        user_traceback += [tr]

    user_traceback = [tr for tr in user_traceback if f"{os.sep}hstest{os.sep}" not in tr]

    return clean_stacktrace(traceback_stack, user_traceback[::-1], user_dir)


def _fix_python_syntax_error(str_trace: str) -> str:
    python_traceback_initial_phrase = "Traceback (most recent call last):"
    python_traceback_start = '  File "'

    is_python_syntax_error = "SyntaxError" in str_trace and (
        f"\n{python_traceback_start}" in str_trace or str_trace.startswith(python_traceback_start)
    )

    if is_python_syntax_error and python_traceback_initial_phrase not in str_trace:
        str_trace = python_traceback_initial_phrase + "\n" + str_trace

    return str_trace


def str_to_stacktrace(str_trace: str) -> str:
    str_trace = _fix_python_syntax_error(str_trace)

    lines = str_trace.splitlines()
    traceback_lines = [i for i, line in enumerate(lines) if line.startswith("  File ")]

    if len(traceback_lines) < 1:
        return str_trace

    traceback_stack = []

    for line_from, line_to in itertools.pairwise(traceback_lines):
        actual_lines = lines[line_from:line_to]
        needed_lines = [line for line in actual_lines if line.startswith("  ")]
        traceback_stack += ["\n".join(needed_lines) + "\n"]

    last_traceback = ""
    before = "\n".join(lines[: traceback_lines[0]]) + "\n"
    after = ""

    for line in lines[traceback_lines[-1] :]:
        if not after and line.startswith("  "):
            last_traceback += line + "\n"
        else:
            after += line + "\n"

    traceback_stack += [last_traceback]

    user_traceback = []
    for trace in traceback_stack:
        r"""
        Avoid traceback elements such as:

        File "C:\Users\**\JetBrains\**\plugins\python\helpers\pydev\pydevd.py", line 1477, in _exec
          pydev_imports.execfile(file, globals, locals)  # execute the script
        File "C:\Users\**\JetBrains\**\plugins\python\helpers\pydev\_pydev_imps\_pydev_execfile.py", line 18, in execfile
          exec(compile(contents+"\n", file, 'exec'), glob, loc)

        Which will appear when testing locally inside PyCharm.
        """  # noqa: E501
        if f"{os.sep}JetBrains{os.sep}" in trace:
            continue

        r"""
        Avoid traceback elements such as:

        File "C:\\Python39\\lib\\importlib\\__init__.py", line 127, in import_module
          return _bootstrap._gcd_import(name[level:], package, level)
        """
        if f"{os.sep}importlib{os.sep}" in trace:
            continue

        user_traceback += [trace]

    return clean_stacktrace([before, *user_traceback, after], user_traceback)


def clean_stacktrace(
    full_traceback: list[str], user_traceback: list[str], user_dir: str = ""
) -> str:
    dir_names = []
    for tr in user_traceback:
        try:
            start_index = tr.index('"') + 1
            end_index = tr.index('"', start_index)
        except ValueError:
            continue

        user_file = tr[start_index:end_index]

        if user_file.startswith("<"):
            continue

        dir_name = os.path.dirname(tr[start_index:end_index])
        if os.path.isdir(dir_name):
            dir_names += [os.path.abspath(dir_name)]

    if dir_names:
        from hstest.common.os_utils import is_windows

        if is_windows():
            drives = {}
            for dir_name in dir_names:
                drive = dir_name[0]
                drives[drive] = drives.get(drive, 0) + 1

            if len(drives) > 1:
                max_drive = max(drives.values())
                drive_to_leave = next(d for d in drives if drives[d] == max_drive)
                dir_names = [d for d in dir_names if d.startswith(drive_to_leave)]

        user_dir = os.path.commonpath(dir_names) + os.sep

    cleaned_traceback = []
    for trace in full_traceback[1:-1]:
        if trace.startswith(" " * 4):
            # Trace line that starts with 4 is a line with SyntaxError
            cleaned_traceback += [trace]
        elif user_dir in trace or ("<" in trace and ">" in trace and "<frozen " not in trace):
            # avoid including <frozen importlib...> lines that are always in the stacktrace
            # but include <string>, <module> because it's definitely user's code
            if not user_dir.startswith("<"):
                if user_dir in trace:
                    trace = trace.replace(user_dir, "")
                else:
                    folder_name = os.path.basename(user_dir[:-1])
                    if folder_name in trace:
                        index = trace.index(folder_name)
                        trace = '  File "' + trace[index + len(folder_name + os.sep) :]

            cleaned_traceback += [trace]

    return full_traceback[0] + "".join(cleaned_traceback) + full_traceback[-1]
