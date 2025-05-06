from __future__ import annotations

import contextlib
from copy import deepcopy
from importlib import reload
from typing import Final, TYPE_CHECKING

from hstest.testing.plotting.drawing.drawing_data import DrawingData

with contextlib.suppress(ImportError):
    import pandas as pd

import contextlib

from hstest.testing.plotting.drawing.drawing import Drawing
from hstest.testing.plotting.drawing.drawing_builder import DrawingBuilder
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from hstest.testing.plotting.drawing.drawing_type import DrawingType

if TYPE_CHECKING:
    from hstest.testing.runner.plot_testing_runner import DrawingsStorage

NUM_SHAPES: Final = 2


class MatplotlibHandler:
    _saved = False
    _replaced = False

    _Axes = None
    _hist = None
    _plot = None
    _scatter = None
    _pie = None
    _bar = None
    _barh = None
    _violinplot = None
    _imshow = None
    _boxplot = None
    _show = None
    _backend = None
    _matplotlib = None

    @staticmethod
    def replace_plots(drawings: DrawingsStorage) -> None:
        try:
            import matplotlib as mpl
            import numpy as np
        except ModuleNotFoundError:
            return

        def custom_show_func(*args, **kwargs) -> None:
            pass

        def hist(x: list[float], *args, data: list[float] | None = None, **kw) -> None:
            if data is not None:
                with contextlib.suppress(Exception):
                    x = data[x]

            try:
                if isinstance(x, pd.DataFrame):
                    for col in x.columns:
                        hist(x[col], *args, **kw)
                    return None
                if isinstance(x, pd.Series):
                    return hist(x.to_numpy(), *args, **kw)
            except Exception:  # noqa: BLE001, S110
                pass

            if not isinstance(x, np.ndarray):
                x = np.array(x, dtype=object)
                if len(x.shape) == NUM_SHAPES:
                    from matplotlib import cbook

                    x = np.array(cbook._reshape_2D(x, "x"), dtype=object)  # noqa: SLF001

            if len(x.shape) == NUM_SHAPES:
                for i in range(x.shape[1]):
                    hist(x[:, i], *args, **kw)
                return None

            drawings.append(
                Drawing(
                    DrawingLibrary.matplotlib,
                    DrawingType.hist,
                    DrawingData(x, np.array([1] * len(x), dtype=object)),
                    kw,
                )
            )
            return None

        def bar(
            x: list[float], height: list[float], *args, data: list[float] | None = None, **kw
        ) -> None:
            if data is not None:
                with contextlib.suppress(Exception):
                    x = data[x]
                with contextlib.suppress(Exception):
                    height = data[height]

            try:
                if isinstance(x, pd.DataFrame):
                    for col in x.columns:
                        bar(x[col], *args, **kw)
                    return None
                if isinstance(x, pd.Series):
                    return bar(x.to_numpy(), height, *args, **kw)
                if isinstance(height, pd.Series):
                    return bar(x, height.to_numpy(), *args, **kw)
            except Exception:  # noqa: BLE001, S110
                pass

            if isinstance(height, int | float):
                height = np.full((len(x),), height)

            drawings.append(
                Drawing(DrawingLibrary.matplotlib, DrawingType.bar, DrawingData(x, height), kw)
            )
            return None

        def barh(
            x: list[float], width: list[float], *args, data: list[float] | None = None, **kw
        ) -> None:
            return bar(x, width, *args, data=data, **kw)

        def plot(*args, **kwargs) -> None:
            x = []
            y = []

            if len(args) > 0 and isinstance(args[0], list):
                x = args[0]
            if len(args) > 1:
                if isinstance(args[1], list):
                    y = args[1]
            else:
                y = list(range(len(x)))

            drawings.append(
                DrawingBuilder.get_line_drawing(
                    x,
                    y,
                    DrawingLibrary.matplotlib,
                    kwargs,
                )
            )

        def scatter(x: list[float], y: list[float], *a, **kwargs) -> None:
            drawings.append(
                DrawingBuilder.get_scatter_drawing(
                    x,
                    y,
                    DrawingLibrary.matplotlib,
                    kwargs,
                )
            )

        def pie(x: list[float], *a, **kw) -> None:
            # Normalize with other plot libraries
            y = x

            x = [""] * len(y)

            if "labels" in kw and kw["labels"] is not None:
                x = kw["labels"]

            drawings.append(
                Drawing(DrawingLibrary.matplotlib, DrawingType.pie, DrawingData(x, y), kw)
            )

        def violinplot(dataset: list[float], *, data: list[float] | None = None, **kwargs) -> None:
            if data is not None:
                with contextlib.suppress(Exception):
                    dataset = data[dataset]

            drawing = Drawing(DrawingLibrary.matplotlib, DrawingType.violin, dataset, kwargs)

            drawings.append(drawing)

        def imshow(x: list[float], **kwargs) -> None:
            curr_data = {  # noqa: F841
                "x": np.array(x, dtype=object)
            }

            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.heatmap,
                None,
                kwargs,
            )
            drawings.append(drawing)

        def boxplot(x: list[float], **kwargs) -> None:
            curr_data = {  # noqa: F841
                "x": np.array([None], dtype=object),
                "y": np.array(x, dtype=object),
            }

            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.box,
                None,
                kwargs,
            )
            drawings.append(drawing)

        import matplotlib as mpl

        class CustomMatplotlibAxes(mpl.axes.Axes):
            def hist(self, x: list[float], *a, **kw) -> None:
                hist(x, *a, **kw)

            def bar(self, x: list[float], height: list[float], *a, **kw) -> None:
                bar(x, height, *a, **kw)

            def barh(self, y: list[float], width: list[float], *a, **kw) -> None:
                barh(y, width, *a, **kw)

            def plot(self, *args, **kwargs) -> None:
                plot(*args, *kwargs)

            def scatter(self, x: list[float], y: list[float], *a, **kwargs) -> None:
                scatter(x, y, *a, **kwargs)

            def pie(self, x: list[float], *a, **kw) -> None:
                pie(x, *a, **kw)

            def violinplot(self, dataset: list[float], **kwargs) -> None:
                violinplot(dataset, **kwargs)

            def imshow(self, x: list[float], **kwargs) -> None:
                imshow(x, **kwargs)

            def boxplot(self, x: list[float], **kwargs) -> None:
                boxplot(x, **kwargs)

        import matplotlib as mpl

        if not MatplotlibHandler._saved:
            MatplotlibHandler._Axes = deepcopy(mpl.axes.Axes)

        # should be replaced before import matplotlib.pyplot as plt
        mpl.axes.Axes = CustomMatplotlibAxes

        from matplotlib.projections import projection_registry

        projection_registry.register(mpl.axes.Axes)

        import matplotlib.pyplot as plt

        if not MatplotlibHandler._saved:
            MatplotlibHandler._saved = True
            MatplotlibHandler._hist = plt.hist
            MatplotlibHandler._plot = plt.plot
            MatplotlibHandler._scatter = plt.scatter
            MatplotlibHandler._pie = plt.pie
            MatplotlibHandler._bar = plt.bar
            MatplotlibHandler._barh = plt.barh
            MatplotlibHandler._violinplot = plt.violinplot
            MatplotlibHandler._imshow = plt.imshow
            MatplotlibHandler._boxplot = plt.boxplot
            MatplotlibHandler._show = plt.show
            MatplotlibHandler._backend = mpl.get_backend()

        plt.hist = hist
        plt.plot = plot
        plt.scatter = scatter
        plt.pie = pie
        plt.bar = bar
        plt.barh = barh
        plt.violinplot = violinplot
        plt.imshow = imshow
        plt.boxplot = boxplot
        plt.show = custom_show_func

        mpl.use("Agg")

        MatplotlibHandler._replaced = True

    @staticmethod
    def revert_plots() -> None:
        if not MatplotlibHandler._replaced:
            return

        import matplotlib.axes
        import matplotlib.figure
        import matplotlib.pyplot as plt

        matplotlib.axes.Axes = MatplotlibHandler._Axes
        plt.hist = MatplotlibHandler._hist
        plt.plot = MatplotlibHandler._plot
        plt.scatter = MatplotlibHandler._scatter
        plt.pie = MatplotlibHandler._pie
        plt.bar = MatplotlibHandler._bar
        plt.barh = MatplotlibHandler._barh
        plt.violinplot = MatplotlibHandler._violinplot
        plt.imshow = MatplotlibHandler._imshow
        plt.boxplot = MatplotlibHandler._boxplot
        plt.show = MatplotlibHandler._show

        from matplotlib.projections import projection_registry

        projection_registry.register(MatplotlibHandler._Axes)
        matplotlib.use(MatplotlibHandler._backend)

        reload(matplotlib.figure)
        reload(matplotlib.pyplot)

        MatplotlibHandler._replaced = False
