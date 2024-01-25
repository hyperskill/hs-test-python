from __future__ import annotations

__all__ = [
    "CheckResult",
    "DjangoTest",
    "FlaskTest",
    "PlottingTest",
    "SQLTest",
    "SimpleTestCase",
    "StageTest",
    "TestCase",
    "TestPassed",
    "TestedProgram",
    "WrongAnswer",
    "correct",
    "dynamic_test",
    "wrong",
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
