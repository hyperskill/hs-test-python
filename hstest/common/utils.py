import os
import platform
import traceback
from typing import List

failed_msg_start = '#educational_plugin FAILED + '
failed_msg_continue = '#educational_plugin '
success_msg = '#educational_plugin test OK'


def failed(message: str):
    """ Reports failure """
    lines = message.splitlines()
    print('\n' + failed_msg_start + lines[0])
    for line in lines[1:]:
        print(failed_msg_continue + line)
    return -1, message


def passed():
    """ Reports success """
    print('\n' + success_msg)
    return 0, 'test OK'


def clean_text(text: str) -> str:
    return text.replace('\r\n', '\n').replace('\r', '\n').replace('\u00a0', '\u0020')


def get_report():
    name_os = platform.system() + " " + platform.release()
    python = platform.python_version()
    implementation = platform.python_implementation()
    return (
        f'OS {name_os}\n'
        f'{implementation} {python}\n'
        f'Testing library version 3.0.3'
    )


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
