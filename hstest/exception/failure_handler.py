import platform
import sys
import traceback
from typing import List

import hstest
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
            f'Testing library version {hstest.__version__}'
        )
    else:
        return 'Submitted via web'


def get_traceback_stack(ex: BaseException) -> List[str]:
    if sys.version_info >= (3, 10):
        return traceback.format_exception(ex)
    else:
        exc_tb = ex.__traceback__
        return traceback.format_exception(etype=type(ex), value=ex, tb=exc_tb)


def get_exception_text(ex: BaseException) -> str:
    return ''.join(get_traceback_stack(ex))
