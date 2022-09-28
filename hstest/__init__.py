__all__ = [
    'StageTest',
    'DjangoTest',
    'FlaskTest',
    'PlottingTest',
    'SQLTest',

    'TestCase',
    'SimpleTestCase',

    'CheckResult',
    'correct',
    'wrong',

    'WrongAnswer',
    'TestPassed',

    'dynamic_test',
    'TestedProgram',
]

from hstest.dynamic.dynamic_test import dynamic_test
from hstest.exception.outcomes import TestPassed, WrongAnswer
from hstest.stage import DjangoTest, FlaskTest, SQLTest, StageTest
from hstest.test_case import CheckResult, correct, SimpleTestCase, TestCase, wrong
from hstest.testing.tested_program import TestedProgram

try:
    from hstest.stage import PlottingTest
except ImportError:
    PlottingTest = None
