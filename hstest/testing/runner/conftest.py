import pytest
from hstest.testing.test_run import TestRun
from hstest.test_case.test_case import TestCase
from hstest.testing.runner.test_runner import TestRunner


@pytest.fixture
def test_run():
    """Return a test run instance for testing"""
    test_case = TestCase()
    test_runner = TestRunner()
    return TestRun(test_num=1, test_count=1, test_case=test_case, test_rummer=test_runner)
