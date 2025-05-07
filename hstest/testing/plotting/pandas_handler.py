from __future__ import annotations

import contextlib
from typing import ClassVar, Final, TYPE_CHECKING

from hstest.testing.plotting.drawing.drawing_data import DrawingData

with contextlib.suppress(ImportError):
    import numpy as np

try:
    import pandas as pd
    from pandas.api.types import is_numeric_dtype
except ImportError:
    pass

import contextlib

from hstest.testing.plotting.drawing.drawing import Drawing
from hstest.testing.plotting.drawing.drawing_builder import DrawingBuilder
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from hstest.testing.plotting.drawing.drawing_type import DrawingType
from hstest.testing.plotting.matplotlib_handler import MatplotlibHandler

if TYPE_CHECKING:
    from collections.abc import Callable

    from hstest.testing.runner.plot_testing_runner import DrawingsStorage

NUM_SHAPES: Final = 2


def get_line_drawings_with_normalized_data(
    data: pd.DataFrame, x: str | None, y: str | None
) -> list[Drawing]:
    if type(data) is pd.Series:
        return [DrawingBuilder.get_line_drawing(data.index, data, DrawingLibrary.pandas, {})]

    return [
        DrawingBuilder.get_line_drawing(data.index, data[column], DrawingLibrary.pandas, {})
        for column in data.columns
    ]


def get_hexbin_drawings_with_normalized_data(
    data: pd.DataFrame, x: str | None, y: str | None
) -> list[Drawing]:
    drawings = []
    drawing = Drawing(DrawingLibrary.pandas, DrawingType.hexbin, None, {})
    drawings.append(drawing)
    return drawings


def get_area_drawings_with_normalized_data(
    data: pd.DataFrame, x: str | None, y: str | None
) -> list[Drawing]:
    drawings = []
    drawing = Drawing(DrawingLibrary.pandas, DrawingType.area, None, {})
    drawings.append(drawing)
    return drawings


def get_dis_drawings_with_normalized_data(
    data: pd.DataFrame, x: str | None, y: str | None
) -> list[Drawing]:
    drawings = []

    if isinstance(data, pd.Series):
        curr_data = {"x": data.to_numpy()}

        drawing = Drawing(DrawingLibrary.pandas, DrawingType.dis, None, {})
        drawings.append(drawing)
        return drawings

    if x:
        curr_data = {
            "x": np.array(data[x], dtype=object),
        }

        drawing = Drawing(DrawingLibrary.pandas, DrawingType.dis, None, {})
        drawings.append(drawing)
    if y:
        curr_data = {
            "x": np.array(data[y], dtype=object),
        }

        drawing = Drawing(DrawingLibrary.pandas, DrawingType.dis, None, {})
        drawings.append(drawing)

    if not x and not y:
        for column in data.columns:
            if not is_numeric_dtype(data[column]):
                continue

            curr_data = {  # noqa: F841
                "x": data[column].to_numpy()
            }

            drawing = Drawing(DrawingLibrary.pandas, DrawingType.dis, None, {})
            drawings.append(drawing)
    return drawings


def get_box_drawings_with_normalized_data(
    data: pd.DataFrame, x: str | None, y: str | None
) -> list[Drawing]:
    drawings = []

    # Columns are not specified
    if x is None:
        for column in data.columns:
            if not is_numeric_dtype(data[column]):
                continue

            curr_data = {"x": np.array([column], dtype=object), "y": data[column].to_numpy()}

            drawing = Drawing(DrawingLibrary.pandas, DrawingType.box, None, {})
            drawings.append(drawing)
        return drawings

    for column in x:
        if not is_numeric_dtype(data[column]):
            continue

        curr_data = {  # noqa: F841
            "x": np.array([column], dtype=object),
            "y": data[column].to_numpy(),
        }

        drawing = Drawing(DrawingLibrary.pandas, DrawingType.box, None, {})
        drawings.append(drawing)
    return drawings


def get_bar_drawings_with_normalized_data(
    data: pd.DataFrame, x: str | None, y: str | None
) -> list[Drawing]:
    drawings = []

    x_arr = data[x].to_numpy() if x is not None else data.index.to_numpy()

    if y is not None:
        drawing = DrawingBuilder.get_bar_drawing(x_arr, data[y], DrawingLibrary.pandas, {})
        drawings.append(drawing)
        return drawings

    for column in data.columns:
        if not is_numeric_dtype(data[column]):
            continue
        drawing = DrawingBuilder.get_bar_drawing(x_arr, data[column], DrawingLibrary.pandas, {})
        drawings.append(drawing)
    return drawings


def get_pie_drawings_with_normalized_data(
    data: pd.DataFrame, x: str | None, y: str | None
) -> list[Drawing]:
    if isinstance(data, pd.Series):
        return [
            Drawing(
                DrawingLibrary.pandas,
                DrawingType.pie,
                DrawingData(data.index.to_numpy(), data.to_numpy()),
                {},
            )
        ]

    if y is not None:
        return [
            Drawing(
                DrawingLibrary.pandas,
                DrawingType.pie,
                DrawingData(data.index.to_numpy(), data[y].to_numpy()),
                {},
            )
        ]

    drawings = []

    for column in data.columns:
        if not is_numeric_dtype(data[column]):
            continue
        drawings.append(
            Drawing(
                DrawingLibrary.pandas,
                DrawingType.pie,
                DrawingData(data.index.to_numpy(), data[column].to_numpy()),
                {},
            )
        )
    return drawings


def get_scatter_drawings_with_normalized_data(
    data: pd.DataFrame, x: str | None, y: str | None
) -> list[Drawing]:
    return [DrawingBuilder.get_scatter_drawing(data[x], data[y], DrawingLibrary.pandas, {})]


class PandasHandler:
    _saved = False
    _replaced = False

    _PlotAccessor = None

    _series_plot = None
    _dframe_plot = None

    _series_hist = None
    _dframe_hist = None

    _series_bar = None
    _dframe_bar = None

    _series_boxplot = None
    _dframe_boxplot = None

    plot_name_to_basic_name: ClassVar[dict[str, DrawingType]] = {
        # 'barh': DrawingType.bar,  # noqa: ERA001
        "density": DrawingType.dis,
        "kde": DrawingType.dis,
    }

    graph_type_to_normalized_data: ClassVar[
        dict[str, Callable[[pd.DataFrame, str | None, str | None], list[Drawing]]]
    ] = {
        "scatter": get_scatter_drawings_with_normalized_data,
        "line": get_line_drawings_with_normalized_data,
        "pie": get_pie_drawings_with_normalized_data,
        # "bar": get_bar_drawings_with_normalized_data,  # noqa: ERA001
        "box": get_box_drawings_with_normalized_data,
        "dis": get_dis_drawings_with_normalized_data,
    }

    @staticmethod
    def revert_plots() -> None:
        if not PandasHandler._replaced:
            return

        MatplotlibHandler.revert_plots()

        import pandas.plotting
        from pandas.core.accessor import CachedAccessor

        pandas.Series.plot = CachedAccessor("plot", pandas.plotting.PlotAccessor)
        pandas.DataFrame.plot = CachedAccessor("plot", pandas.plotting.PlotAccessor)

        pandas.Series.hist = PandasHandler._series_hist
        pandas.DataFrame.hist = PandasHandler._dframe_hist

        pandas.DataFrame.boxplot = PandasHandler._dframe_boxplot

        PandasHandler._replaced = False

    @staticmethod
    def replace_plots(drawings: DrawingsStorage) -> None:
        try:
            import pandas.plotting
            from pandas.core.accessor import CachedAccessor
        except ModuleNotFoundError:
            return

        class CustomPlotAccessor(pandas.plotting.PlotAccessor):
            def __call__(self, *args, **kw) -> None:
                from pandas.plotting._core import _get_plot_backend  # noqa: PLC2701

                plot_backend = _get_plot_backend(kw.pop("backend", None))

                x, y, kind, kwargs = self._get_call_args(
                    plot_backend.__name__, self._parent, args, kw
                )

                if kind not in self._all_kinds:
                    msg = f"{kind} is not a valid plot kind"
                    raise ValueError(msg)

                data = self._parent.copy()

                plot_name = PandasHandler.plot_name_to_basic_name.get(kind, kind)

                # For boxplot from plot accessor
                if plot_name == DrawingType.box and "columns" in kwargs:
                    x = kwargs["columns"]

                plot_to_func = {
                    "hist": hist,
                    "bar": bar,
                    "barh": barh,
                }

                if plot_name in PandasHandler.graph_type_to_normalized_data:
                    all_drawings = PandasHandler.graph_type_to_normalized_data[plot_name](
                        data, x, y
                    )
                    drawings.extend(all_drawings)
                elif plot_name in plot_to_func:
                    plot_to_func[plot_name](data, **kw)
                else:
                    curr_data = {  # noqa: F841
                        "data": data,
                        "x": x,
                        "y": y,
                        "kwargs": kwargs,
                    }

                    drawing = Drawing(DrawingLibrary.pandas, plot_name, None, {})
                    drawings.append(drawing)

        import pandas.plotting._core

        def boxplot(self: pandas.DataFrame, column: str | None = None, **kwargs) -> None:
            all_drawings = get_box_drawings_with_normalized_data(self, column, None)
            drawings.extend(all_drawings)

        def hist(
            data: pandas.DataFrame | pandas.Series | np.ndarray,
            column: str | None = None,
            *,
            _process_by: bool = True,
            **kw,
        ) -> None:
            for k in list(kw.keys()):
                if kw[k] is None:
                    kw.pop(k)

            if _process_by and "by" in kw and isinstance(kw["by"], str):
                with contextlib.suppress(Exception):
                    kw["by"] = data[kw["by"]]

            if "y" in kw:
                with contextlib.suppress(Exception):
                    data = data[kw.pop("y")]

            if "x" in kw:
                with contextlib.suppress(Exception):
                    data = data[kw.pop("x")]

            if isinstance(data, pandas.DataFrame):
                if column is not None:
                    return hist(data[column].to_numpy(), **kw)
                for col in data.columns:
                    hist(data[col].to_numpy(), **kw)
                return None

            if isinstance(data, pandas.Series):
                return hist(data.to_numpy(), **kw)

            if not isinstance(data, np.ndarray):
                data = np.array(data, dtype=object)
                if len(data.shape) == NUM_SHAPES:
                    from matplotlib import cbook

                    data = np.array(cbook._reshape_2D(data, "x"), dtype=object)  # noqa: SLF001

            if len(data.shape) == NUM_SHAPES:
                for i in range(data.shape[1]):
                    hist(data[:, i], **kw)
                return None

            if _process_by and "by" in kw:
                by = kw["by"]
                pictures = sorted(set(by), key=str)
                for pic in pictures:
                    subplot = [i for i, j in zip(data, by, strict=False) if j == pic]
                    hist(np.array(subplot, dtype=object), _process_by=False, **kw)
                return None

            drawings.append(
                Drawing(
                    DrawingLibrary.pandas,
                    DrawingType.hist,
                    DrawingData(data, np.array([1] * len(data), dtype=object)),
                    kw,
                )
            )
            return None

        def bar(data: pandas.DataFrame, x: str | None = None, y: str | None = None, **kw) -> None:
            for k in list(kw.keys()):
                if kw[k] is None:
                    kw.pop(k)

            if isinstance(data, pandas.DataFrame):
                if y is not None and x is not None:
                    if isinstance(y, str):
                        y = [y]
                    for col in y:
                        bar(None, data[x].array.to_numpy(), data[col].array.to_numpy(), **kw)
                    return None

                if x is not None:
                    for col in data.columns:
                        if col != x:
                            bar(None, data[x].array.to_numpy(), data[col].array.to_numpy(), **kw)
                    return None

                if y is not None:
                    if isinstance(y, str):
                        y = [y]
                    for col in y:
                        bar(None, data[col].index.to_numpy(), data[col].array.to_numpy(), **kw)
                    return None

                for col in data.columns:
                    bar(None, data[col].index.to_numpy(), data[col].array.to_numpy(), **kw)
                return None

            if isinstance(data, pandas.Series):
                return bar(None, data.index.to_numpy(), data.array.to_numpy(), **kw)

            drawings.append(Drawing(DrawingLibrary.pandas, DrawingType.bar, DrawingData(x, y), kw))
            return None

        def barh(
            self: pandas.Series,
        ) -> None:
            pass

        if not PandasHandler._saved:
            PandasHandler._saved = True

            PandasHandler._series_plot = pandas.Series.plot
            PandasHandler._dframe_plot = pandas.DataFrame.plot

            PandasHandler._series_hist = pandas.Series.hist
            PandasHandler._dframe_hist = pandas.DataFrame.hist

            # PandasHandler._series_bar = pandas.Series.bar  # noqa: ERA001

            PandasHandler._dframe_boxplot = pandas.DataFrame.boxplot

        pandas.Series.plot = CachedAccessor("plot", CustomPlotAccessor)
        pandas.DataFrame.plot = CachedAccessor("plot", CustomPlotAccessor)

        pandas.Series.hist = hist
        pandas.DataFrame.hist = hist

        pandas.DataFrame.boxplot = boxplot

        PandasHandler._replaced = True
