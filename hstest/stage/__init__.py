from __future__ import annotations
from typing import Any, Union

__all__ = [
    "DjangoTest",
    "FlaskTest",
    "SQLTest",
    "StageTest",
]

from hstest.stage.django_test import DjangoTest
from hstest.stage.flask_test import FlaskTest
from hstest.stage.sql_test import SQLTest
from hstest.stage.stage_test import StageTest

# Define PlottingTest as Any before trying to import it
PlottingTest: Any

try:
    from hstest.stage.plotting_test import PlottingTest
    __all__.append("PlottingTest")
except ImportError:
    PlottingTest = None
