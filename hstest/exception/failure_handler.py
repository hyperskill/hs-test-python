from __future__ import annotations

import platform
import traceback

from hstest.testing.execution_options import inside_docker


def get_report() -> str:
    if not inside_docker:
        name_os = platform.system() + " " + platform.release()
        python = platform.python_version()
        implementation = platform.python_implementation()
        return (
            "Submitted via IDE\n"
            "\n"
            f"OS {name_os}\n"
            f"{implementation} {python}\n"
            f"Testing library version 8"
        )
    return "Submitted via web"


def get_traceback_stack(ex: BaseException) -> list[str]:
    return traceback.format_exception(ex)


def get_exception_text(ex: BaseException) -> str:
    return "".join(get_traceback_stack(ex))
