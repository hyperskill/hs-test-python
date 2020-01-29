import os
import sys
import traceback
import platform

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


def normalize_line_endings(text: str) -> str:
    return text.replace('\r\n', '\n').replace('\r', '\n')


def get_report():
    name_os = platform.system() + " " + platform.release()
    python = platform.python_version()
    implementation = platform.python_implementation()
    return (
        f'OS {name_os}\n'
        f'{implementation} {python}\n'
        f'Testing library version 2'
    )


def get_stacktrace(user_file: str, ex: BaseException, hide_internals=False) -> str:
    try:
        raise ex
    except BaseException:
        exc_type, exc_obj, exc_tb = sys.exc_info()

        traceback_stack = []

        for line in traceback.TracebackException(
                type(exc_obj), exc_obj, exc_tb, limit=None).format(chain=None):
            traceback_stack += [line]

        if not hide_internals:
            return ''.join(traceback_stack)

        user_dir = ''
        while exc_tb is not None:
            filename = exc_tb.tb_frame.f_code.co_filename
            if filename.endswith(user_file):
                user_dir = os.path.dirname(filename) + os.sep
                break
            exc_tb = exc_tb.tb_next

        cleaned_traceback = []
        for trace in traceback_stack[1:-1]:
            if user_dir in trace:
                cleaned_traceback += [trace.replace(user_dir, '')]

        return traceback_stack[0] + ''.join(cleaned_traceback) + traceback_stack[-1]
