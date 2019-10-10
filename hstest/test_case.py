from typing import List, Dict, Any, Tuple


class TestCase:

    def __init__(self, *, stdin='', args=None,
                 attach=None, files=None, copy_to_attach=False):
        self.input: str = stdin
        self.args: List[str] = [] if args is None else args
        self.attach: Any = attach
        self.files: Dict[str, str] = {} if files is None else files
        if copy_to_attach:
            self.attach = stdin

    @staticmethod
    def from_stepik(stepik_tests: List[Tuple[str, Any]]) -> List['TestCase']:
        hs_tests = []
        for test in stepik_tests:
            hs_test = TestCase()
            if type(test) in (list, tuple):
                hs_test.input = test[0]
                hs_test.attach = test[1]
            elif type(test) is str:
                hs_test.input = test
            else:
                raise ValueError("Bad test: " + str(test))
            hs_tests += [hs_test]
        return hs_tests
