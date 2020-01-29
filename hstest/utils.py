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


def get_stacktrace(stage, ex: BaseException):
    try:
        raise ex
    except BaseException:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        trace_frames = []

        inside_user_trace = False
        skipped_traces = []
        curr_trace = 0
        while exc_tb is not None:
            code = exc_tb.tb_frame.f_code
            filename = code.co_filename

            if filename.endswith(stage.file_to_test) and not inside_user_trace:
                inside_user_trace = True
                if len(stage.full_file_to_test) == 0:
                    stage.full_file_to_test = exc_tb.tb_frame.f_code.co_filename

            elif 'hstest' in filename and inside_user_trace:
                inside_user_trace = False

            if inside_user_trace:
                trace_frames += [exc_tb.tb_frame.f_code]
            else:
                skipped_traces += [curr_trace]

            exc_tb = exc_tb.tb_next
            curr_trace += 1

        if not trace_frames:
            return _get_stacktrace(stage, hide_internals=False)

        else:
            return _get_stacktrace(
                stage,
                hide_internals=True,
                skipped_traces=skipped_traces
            )


def _get_stacktrace(stage, hide_internals, skipped_traces=None):

    if skipped_traces is None:
        skipped_traces = []

    if stage.full_file_to_test != '':
        common_prefix = os.path.commonpath([
            stage.full_file_to_test, stage.this_test_file
        ])
    else:
        common_prefix = ''

    exc_type, exc_obj, exc_tb = sys.exc_info()

    if hide_internals and len(skipped_traces) != 0:
        traceback_msg = 'Traceback (most recent call last):\n'
    else:
        traceback_msg = ''

    curr_trace = 0
    for line in traceback.TracebackException(
            type(exc_obj), exc_obj, exc_tb, limit=None).format(chain=None):
        if not hide_internals:
            traceback_msg += line
        elif curr_trace not in skipped_traces and stage.this_test_file not in line:
            traceback_msg += line.replace(common_prefix + os.sep, '')
        curr_trace += 1

    return traceback_msg
