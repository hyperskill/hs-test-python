from __future__ import annotations

from inspect import cleandoc
import re
from typing import Any

from hstest.stage.stage_test import StageTest


class ExpectedFailTest(StageTest):
    _base_contain: str | list[str] = []
    _base_not_contain: str | list[str] = []

    contain: str | list[str] = []
    not_contain: str | list[str] = []

    def __init__(self, args) -> None:
        super().__init__(args)

    def normalize_error_message(self, message: str) -> str:
        # Remove error pointer markers added in Python 3.11+
        message = re.sub(r'\s+[~^]+\s*', ' ', message)
        # Normalize whitespace and line breaks
        message = ' '.join(message.split())
        return message

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

        normalized_feedback = self.normalize_error_message(feedback)

        for item in should_contain:
            normalized_item = self.normalize_error_message(cleandoc(item))
            self.assertIn(normalized_item, normalized_feedback,
                         f"Expected to find:\n{normalized_item}\nin:\n{normalized_feedback}")

        for item in should_not_contain:
            normalized_item = self.normalize_error_message(cleandoc(item))
            self.assertNotIn(normalized_item, normalized_feedback,
                           f"Expected NOT to find:\n{normalized_item}\nin:\n{normalized_feedback}")
