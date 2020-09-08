from typing import Optional


class TestRun:
    curr_test_run: Optional['TestRun'] = None

    def __init__(self, test_num: int, test_case):
        self.test_num: int = test_num
        self.test_case = test_case
        self.input_used: bool = False
        self._error_in_test: Optional[BaseException] = None

    def set_error_in_test(self, err: Optional[BaseException]):
        if self._error_in_test is None or err is None:
            self._error_in_test = err

    def get_error_in_test(self) -> Optional[BaseException]:
        return self._error_in_test
