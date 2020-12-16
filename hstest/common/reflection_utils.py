import inspect
import os
import traceback
from typing import List


def get_main(filename: str = 'main') -> str:
    file = inspect.stack()[1].filename
    file = file.replace(os.sep, '.')[:-3]
    file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + filename
    return file


def get_stacktrace(user_file: str, ex: BaseException, hide_internals=False) -> str:
    exc_tb = ex.__traceback__
    traceback_stack = traceback.format_exception(etype=type(ex), value=ex, tb=exc_tb)

    if not hide_internals:
        return ''.join(traceback_stack)

    if isinstance(ex, SyntaxError):
        if ex.filename.startswith('<'):  # "<string>", or "<module>"
            user_dir = ex.filename
        else:
            user_dir = os.path.dirname(ex.filename) + os.sep
    else:
        user_dir = ''

    user_traceback = []
    for tr in traceback_stack[::-1][1:-1]:
        if f'{os.sep}lib{os.sep}runpy.py"' in tr:
            break
        user_traceback += [tr]

    user_traceback = [tr for tr in user_traceback
                      if f'{os.sep}hstest{os.sep}' not in tr]

    user_traceback: List[str] = user_traceback[::-1]
    dir_names = []
    for tr in user_traceback:
        try:
            start_index = tr.index('"') + 1
            end_index = tr.index('"', start_index)
        except ValueError:
            continue

        user_file = tr[start_index: end_index]

        if user_file.startswith('<'):
            continue

        dir_name = os.path.dirname(tr[start_index: end_index])
        if os.path.isdir(dir_name):
            dir_names += [os.path.abspath(dir_name)]

    if dir_names:
        user_dir = os.path.commonpath(dir_names) + os.sep

    if not user_dir:
        return 'File "' + user_file + '" not found. Check if you deleted it.\n\n' + traceback_stack[-1]

    cleaned_traceback = []
    for trace in traceback_stack[1:-1]:
        if trace.startswith(' ' * 4):
            # Trace line that starts with 4 is a line with SyntaxError
            cleaned_traceback += [trace]
        elif user_dir in trace or ('<' in trace and '>' in trace and '<frozen ' not in trace):
            # avoid including <frozen importlib...> lines that are always in the stacktrace
            # but include <string>, <module> because it's definitely user's code
            if not user_dir.startswith('<'):
                if user_dir in trace:
                    trace = trace.replace(user_dir, '')
                else:
                    folder_name = os.path.basename(user_dir[:-1])
                    if folder_name in trace:
                        index = trace.index(folder_name)
                        trace = '  File "' + trace[index + len(folder_name + os.sep):]

            cleaned_traceback += [trace]

    return traceback_stack[0] + ''.join(cleaned_traceback) + traceback_stack[-1]
