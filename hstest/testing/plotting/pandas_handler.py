from typing import TYPE_CHECKING

from hstest.testing.plotting.drawing.drawing_data import DrawingData

try:
    import numpy as np
except ImportError:
    pass

try:
    import pandas as pd
    from pandas.api.types import is_numeric_dtype
except ImportError:
    pass

from hstest.testing.plotting.drawing.drawing import Drawing
from hstest.testing.plotting.drawing.drawing_builder import DrawingBuilder
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from hstest.testing.plotting.drawing.drawing_type import DrawingType
from hstest.testing.plotting.matplotlib_handler import MatplotlibHandler

if TYPE_CHECKING:
    from hstest.testing.runner.plot_testing_runner import DrawingsStorage


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

    plot_name_to_basic_name = {
        # 'barh': DrawingType.bar,
        'density': DrawingType.dis,
        'kde': DrawingType.dis,
    }

    graph_type_to_normalized_data = {
        'scatter': lambda data, x, y: PandasHandler.get_scatter_drawings_with_normalized_data(
            data, x, y
        ),
        'line': lambda data, x, y: PandasHandler.get_line_drawings_with_normalized_data(data, x, y),
        'pie': lambda data, x, y: PandasHandler.get_pie_drawings_with_normalized_data(data, x, y),
        # 'bar': lambda data, x, y: PandasHandler.get_bar_drawings_with_normalized_data(data, x, y),
        'box': lambda data, x, y: PandasHandler.get_box_drawings_with_normalized_data(data, x, y),
        'dis': lambda data, x, y: PandasHandler.get_dis_drawings_with_normalized_data(data, x, y),
    }

    @staticmethod
    def get_line_drawings_with_normalized_data(data, x, y):
        drawings = list()

        if type(data) is pd.Series:
            drawings.append(
                DrawingBuilder.get_line_drawing(
                    data.index,
                    data,
                    DrawingLibrary.pandas,
                    {}
                )
            )
            return drawings

        for column in data.columns:
            drawings.append(
                DrawingBuilder.get_line_drawing(
                    data.index,
                    data[column],
                    DrawingLibrary.pandas,
                    {}
                )
            )

        return drawings

    @staticmethod
    def get_scatter_drawings_with_normalized_data(data, x, y):
        return [
            DrawingBuilder.get_scatter_drawing(
                data[x], data[y],
                DrawingLibrary.pandas,
                {}
            )
        ]

    @staticmethod
    def get_pie_drawings_with_normalized_data(data: 'pd.DataFrame', x, y):
        if type(data) == pd.Series:
            return [
                Drawing(
                    DrawingLibrary.pandas,
                    DrawingType.pie,
                    DrawingData(data.index.to_numpy(), data.to_numpy()),
                    {}
                )
            ]

        if y is not None:
            return [
                Drawing(
                    DrawingLibrary.pandas,
                    DrawingType.pie,
                    DrawingData(data.index.to_numpy(), data[y].to_numpy()),
                    {}
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
                    {}
                )
            )
        return drawings

    @staticmethod
    def get_bar_drawings_with_normalized_data(data: 'pd.DataFrame', x, y):
        drawings = []

        if x is not None:
            x_arr = data[x].to_numpy()
        else:
            x_arr = data.index.to_numpy()

        if y is not None:
            drawing = DrawingBuilder.get_bar_drawing(
                x_arr, data[y],
                DrawingLibrary.pandas,
                {}
            )
            drawings.append(drawing)
            return drawings

        for column in data.columns:
            if not is_numeric_dtype(data[column]):
                continue
            drawing = DrawingBuilder.get_bar_drawing(
                x_arr, data[column],
                DrawingLibrary.pandas,
                {}
            )
            drawings.append(drawing)
        return drawings

    @staticmethod
    def get_box_drawings_with_normalized_data(data: 'pd.DataFrame', x, y):

        drawings = []

        # Columns are not specified
        if x is None:
            for column in data.columns:
                if not is_numeric_dtype(data[column]):
                    continue

                curr_data = {  # noqa: F841
                    'x': np.array([column]),
                    'y': data[column].to_numpy()
                }

                drawing = Drawing(
                    DrawingLibrary.pandas,
                    DrawingType.box,
                    None,
                    {}
                )
                drawings.append(drawing)
            return drawings

        for column in x:
            if not is_numeric_dtype(data[column]):
                continue

            curr_data = {  # noqa: F841
                'x': np.array([column]),
                'y': data[column].to_numpy()
            }

            drawing = Drawing(
                DrawingLibrary.pandas,
                DrawingType.box,
                None,
                {}
            )
            drawings.append(drawing)
        return drawings

    @staticmethod
    def get_dis_drawings_with_normalized_data(data, x, y):
        drawings = []

        if type(data) == pd.Series:
            curr_data = {
                'x': data.to_numpy()
            }

            drawing = Drawing(
                DrawingLibrary.pandas,
                DrawingType.dis,
                None,
                {}
            )
            drawings.append(drawing)
            return drawings

        if x:
            curr_data = {
                'x': np.array(data[x]),
            }

            drawing = Drawing(
                DrawingLibrary.pandas,
                DrawingType.dis,
                None,
                {}
            )
            drawings.append(drawing)
        if y:
            curr_data = {
                'x': np.array(data[y]),
            }

            drawing = Drawing(
                DrawingLibrary.pandas,
                DrawingType.dis,
                None,
                {}
            )
            drawings.append(drawing)

        if not x and not y:
            for column in data.columns:
                if not is_numeric_dtype(data[column]):
                    continue

                curr_data = {  # noqa: F841
                    'x': data[column].to_numpy()
                }

                drawing = Drawing(
                    DrawingLibrary.pandas,
                    DrawingType.dis,
                    None,
                    {}
                )
                drawings.append(drawing)
        return drawings

    @staticmethod
    def get_area_drawings_with_normalized_data(data, x, y):
        drawings = []
        drawing = Drawing(
            DrawingLibrary.pandas,
            DrawingType.area,
            None,
            {}
        )
        drawings.append(drawing)
        return drawings

    @staticmethod
    def get_hexbin_drawings_with_normalized_data(data, x, y):
        drawings = []
        drawing = Drawing(
            DrawingLibrary.pandas,
            DrawingType.hexbin,
            None,
            {}
        )
        drawings.append(drawing)
        return drawings

    @staticmethod
    def replace_plots(drawings: 'DrawingsStorage'):
        try:
            import pandas.plotting
            from pandas.core.accessor import CachedAccessor
        except ModuleNotFoundError:
            return

        class CustomPlotAccessor(pandas.plotting.PlotAccessor):
            def __call__(self, *args, **kw):
                from pandas.plotting._core import _get_plot_backend

                plot_backend = _get_plot_backend(kw.pop("backend", None))

                x, y, kind, kwargs = self._get_call_args(
                    plot_backend.__name__, self._parent, args, kw
                )

                if kind not in self._all_kinds:
                    raise ValueError(f"{kind} is not a valid plot kind")

                data = self._parent.copy()

                plot_name = kind if kind not in PandasHandler.plot_name_to_basic_name \
                    else PandasHandler.plot_name_to_basic_name[kind]

                # For boxplot from plot accessor
                if plot_name == DrawingType.box:
                    if 'columns' in kwargs:
                        x = kwargs['columns']

                plot_to_func = {
                    'hist': hist,
                    'bar': bar,
                    'barh': barh,
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
                        'data': data,
                        'x': x,
                        'y': y,
                        'kwargs': kwargs
                    }

                    drawing = Drawing(
                        DrawingLibrary.pandas,
                        plot_name,
                        None,
                        {}
                    )
                    drawings.append(drawing)

        import pandas.plotting._core

        def boxplot(
            self,
            column=None,
            **kwargs
        ):
            all_drawings = PandasHandler.get_box_drawings_with_normalized_data(self, column, None)
            drawings.extend(all_drawings)

        def hist(
            data,
            column=None,
            _process_by=True,
            **kw
        ):
            for k in list(kw.keys()):
                if kw[k] is None:
                    kw.pop(k)

            if _process_by and 'by' in kw and type(kw['by']) == str:
                try:
                    kw['by'] = data[kw['by']]
                except Exception:
                    pass

            if 'y' in kw:
                try:
                    data = data[kw.pop('y')]
                except Exception:
                    pass

            if 'x' in kw:
                try:
                    data = data[kw.pop('x')]
                except Exception:
                    pass

            if type(data) == pandas.DataFrame:
                if column is not None:
                    return hist(data[column].to_numpy(), **kw)
                for col in data.columns:
                    hist(data[col].to_numpy(), **kw)
                return

            elif type(data) == pandas.Series:
                return hist(data.to_numpy(), **kw)

            elif type(data) != np.ndarray:
                data = np.array(data, dtype=object)
                if len(data.shape) == 2:
                    import matplotlib.cbook as cbook
                    data = np.array(cbook._reshape_2D(data, 'x'), dtype=object)

            if len(data.shape) == 2:
                for i in range(data.shape[1]):
                    hist(data[:, i], **kw)
                return

            if _process_by and 'by' in kw:
                by = kw['by']
                pictures = sorted(set(by), key=str)
                for pic in pictures:
                    subplot = [i for i, j in zip(data, by) if j == pic]
                    hist(np.array(subplot, dtype=object), _process_by=False, **kw)
                return

            drawings.append(
                Drawing(
                    DrawingLibrary.pandas,
                    DrawingType.hist,
                    DrawingData(data, np.array([1] * len(data))),
                    kw
                )
            )

        def bar(
            data,
            x=None,
            y=None,
            **kw
        ):
            for k in list(kw.keys()):
                if kw[k] is None:
                    kw.pop(k)

            if type(data) == pandas.DataFrame:
                if y is not None and x is not None:
                    if type(y) == str:
                        y = [y]
                    for col in y:
                        bar(None,
                            data[x].array.to_numpy(),
                            data[col].array.to_numpy(),
                            **kw)
                    return

                elif x is not None:
                    for col in data.columns:
                        if col != x:
                            bar(None,
                                data[x].array.to_numpy(),
                                data[col].array.to_numpy(),
                                **kw)
                    return

                elif y is not None:
                    if type(y) == str:
                        y = [y]
                    for col in y:
                        bar(None,
                            data[col].index.to_numpy(),
                            data[col].array.to_numpy(),
                            **kw)
                    return

                else:
                    for col in data.columns:
                        bar(None,
                            data[col].index.to_numpy(),
                            data[col].array.to_numpy(),
                            **kw)
                    return

            elif type(data) == pandas.Series:
                return bar(None,
                           data.index.to_numpy(),
                           data.array.to_numpy(),
                           **kw)

            drawings.append(
                Drawing(
                    DrawingLibrary.pandas,
                    DrawingType.bar,
                    DrawingData(x, y),
                    kw
                )
            )

        def barh(
            self,
        ):
            pass

        if not PandasHandler._saved:
            PandasHandler._saved = True

            PandasHandler._series_plot = pandas.Series.plot
            PandasHandler._dframe_plot = pandas.DataFrame.plot

            PandasHandler._series_hist = pandas.Series.hist
            PandasHandler._dframe_hist = pandas.DataFrame.hist

            # PandasHandler._series_bar = pandas.Series.bar

            PandasHandler._dframe_boxplot = pandas.DataFrame.boxplot

        pandas.Series.plot = CachedAccessor("plot", CustomPlotAccessor)
        pandas.DataFrame.plot = CachedAccessor("plot", CustomPlotAccessor)

        pandas.Series.hist = hist
        pandas.DataFrame.hist = hist

        pandas.DataFrame.boxplot = boxplot

        PandasHandler._replaced = True

    @staticmethod
    def revert_plots():
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
