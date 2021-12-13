import platform
import traceback

from hstest.testing.execution_options import inside_docker


def get_report():
    if not inside_docker:
        name_os = platform.system() + " " + platform.release()
        python = platform.python_version()
        implementation = platform.python_implementation()
        return (
            'Submitted via IDE\n'
            '\n'
            f'OS {name_os}\n'
            f'{implementation} {python}\n'
            f'Testing library version 6.1'
        )
    else:
        return 'Submitted via web'


def get_exception_text(ex: BaseException) -> str:
    exc_tb = ex.__traceback__
    traceback_stack = traceback.format_exception(etype=type(ex), value=ex, tb=exc_tb)
    return ''.join(traceback_stack)
