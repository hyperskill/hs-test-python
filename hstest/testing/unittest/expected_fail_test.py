from __future__ import annotations

from inspect import cleandoc

from hstest import StageTest


class ExpectedFailTest(StageTest):
    _base_contain: str | list[str] = []
    _base_not_contain: str | list[str] = []

    contain: str | list[str] = []
    not_contain: str | list[str] = []

    def __init__(self, args) -> None:
        super().__init__(args)

    def test_run_unittest(self) -> None:
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
