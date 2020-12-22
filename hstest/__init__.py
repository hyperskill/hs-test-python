__all__ = [
    'StageTest',
    'TestCase',
    'SimpleTestCase',
    'CheckResult',
    'correct',
    'wrong',
    'dynamic_test',
    'TestedProgram',
]

from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.test_case import CheckResult, SimpleTestCase, TestCase, correct, wrong
from hstest.testing.tested_program import TestedProgram
