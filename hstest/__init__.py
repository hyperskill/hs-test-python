from __future__ import annotations
from typing import Any, Union

__all__ = [
    "CheckResult",
    "DjangoTest",
    "FlaskTest",
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

# Define PlottingTest as Any before trying to import it
PlottingTest: Any

try:
    from hstest.stage import PlottingTest
    __all__.append("PlottingTest")
except ImportError:
    PlottingTest = None
