from __future__ import annotations

import pytest

from hstest.test_case.test_case import TestCase
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from hstest.testing.test_run import TestRun


@pytest.fixture
def test_run():
    """Return a test run instance for testing."""
    test_case = TestCase()
    return TestRun(test_case)


@pytest.fixture
def figures(request):
    """Return figures from the test class instance."""
    return request.instance.all_figures() if hasattr(request.instance, "all_figures") else []


@pytest.fixture
def correct_plot_count() -> int:
    """Return expected number of plots."""
    return 1


@pytest.fixture
def library_type():
    """Return the library type being tested."""
    return DrawingLibrary.pandas


@pytest.fixture
def correct_data():
    """Return correct data for comparison."""
    return [10, 20, 30, 40, 50]  # Sample data for histogram
