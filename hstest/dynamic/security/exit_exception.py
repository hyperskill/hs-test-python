from __future__ import annotations

from typing import NoReturn


class ExitException(BaseException):
    @staticmethod
    def throw() -> NoReturn:
        raise ExitException
