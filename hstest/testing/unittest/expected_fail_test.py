from inspect import cleandoc
from typing import List, Union

from hstest import StageTest


class ExpectedFailTest(StageTest):
    _base_contain: Union[str, List[str]] = []
    _base_not_contain: Union[str, List[str]] = []

    contain: Union[str, List[str]] = []
    not_contain: Union[str, List[str]] = []

    def __init__(self, args):
        super().__init__(args)

    def test_run_unittest(self):

        if not self.contain and not self.not_contain:
            self.fail("'contain' or 'not_contain' should not be empty")

        result, feedback = self.run_tests()

        self.assertEqual(result, -1)

        if type(self._base_contain) != list:
            self._base_contain = [self._base_contain]
        if type(self._base_not_contain) != list:
            self._base_not_contain = [self._base_not_contain]
        if type(self.contain) != list:
            self.contain = [self.contain]
        if type(self.not_contain) != list:
            self.not_contain = [self.not_contain]

        should_contain = self._base_contain + self.contain
        should_not_contain = self._base_not_contain + self.not_contain

        for item in should_contain:
            self.assertIn(cleandoc(item), feedback)

        for item in should_not_contain:
            self.assertNotIn(cleandoc(item), feedback)
