import numpy as np
import pandas as pd

from hstest.testing.plotting.drawing import Drawing, DrawingType, DrawingLibrary
from hstest.testing.plotting.matplotlib_handler import MatplotlibHandler
from pandas.api.types import is_numeric_dtype


class PandasHandler:
    _saved = False
    _replaced = False

    _PlotAccessor = None
    _Series_plot = None
    _Dataframe_plot = None
    _Dataframe_boxplot = None
    _Dataframe_hist = None
    _Series_hist = None

    plot_name_to_basic_name = {
        'barh': DrawingType.bar,
        'density': DrawingType.dis,
        'kde': DrawingType.dis,
    }

    graph_type_to_normalized_data = {
        'scatter': lambda data, x, y: PandasHandler.get_scatter_drawings_with_normalized_data(data, x, y),
        'hist': lambda data, x, y: PandasHandler.get_hist_drawings_with_normalized_data(data, x, y),
        'line': lambda data, x, y: PandasHandler.get_line_drawings_with_normalized_data(data, x, y),
        'pie': lambda data, x, y: PandasHandler.get_pie_drawings_with_normalized_data(data, x, y),
        'bar': lambda data, x, y: PandasHandler.get_bar_drawings_with_normalized_data(data, x, y),
        'box': lambda data, x, y: PandasHandler.get_box_drawings_with_normalized_data(data, x, y),
        'dis': lambda data, x, y: PandasHandler.get_dis_drawings_with_normalized_data(data, x, y),
    }

    @staticmethod
    def get_hist_drawings_with_normalized_data(data: pd.DataFrame, x, y):
        drawings = []

        for column in data.columns:
            drawings.append(
                Drawing.get_hist_drawing(
                    data[column],
                    DrawingLibrary.pandas
                )
            )

        return drawings

    @staticmethod
    def get_line_drawings_with_normalized_data(data, x, y):
        drawings = list()

        if type(data) is pd.Series:
            drawings.append(
                Drawing.get_line_drawing(
                    data.index,
                    data,
                    DrawingLibrary.pandas
                )
            )
            return drawings

        for column in data.columns:
            drawings.append(
                Drawing.get_line_drawing(
                    data.index,
                    data[column],
                    DrawingLibrary.pandas
                )
            )

        return drawings

    @staticmethod
    def get_scatter_drawings_with_normalized_data(data, x, y):
        return [
            Drawing.get_scatter_drawing(
                data[x], data[y],
                DrawingLibrary.pandas
            )
        ]

    @staticmethod
    def get_pie_drawings_with_normalized_data(data: pd.DataFrame, x, y):
        if y is not None:
            drawing = Drawing.get_pie_drawing(
                data.index, data[y],
                DrawingLibrary.pandas
            )
            return [drawing]

        drawings = []

        for column in data.columns:
            if not is_numeric_dtype(data[column]):
                continue
            drawing = Drawing.get_pie_drawing(
                data.index, data[column],
                DrawingLibrary.pandas
            )
            drawings.append(drawing)
        return drawings

    @staticmethod
    def get_bar_drawings_with_normalized_data(data: pd.DataFrame, x, y):
        x_arr = np.array([])
        drawings = []

        if x is not None:
            x_arr = data[x].to_numpy()
        else:
            x_arr = data.index.to_numpy()

        if y is not None:
            y_arr = data[y].to_numpy()
            drawing = Drawing(
                DrawingLibrary.pandas,
                DrawingType.bar,
                {
                    'x': x_arr,
                    'y': y_arr
                }
            )
            drawings.append(drawing)
            return drawings

        for column in data.columns:
            if not is_numeric_dtype(data[column]):
                continue
            drawing = Drawing(
                DrawingLibrary.pandas,
                DrawingType.bar,
                {
                    'x': x_arr,
                    'y': data[column].to_numpy()
                }
            )
            drawings.append(drawing)
        return drawings

    @staticmethod
    def get_box_drawings_with_normalized_data(data: pd.DataFrame, x, y):

        drawings = []

        # Columns are not specified
        if x is None:
            for column in data.columns:
                if not is_numeric_dtype(data[column]):
                    continue
                drawing = Drawing(
                    DrawingLibrary.pandas,
                    DrawingType.box,
                    {
                        'x': np.array([column]),
                        'y': data[column].to_numpy()
                    }
                )
                drawings.append(drawing)
            return drawings

        for column in x:
            if not is_numeric_dtype(data[column]):
                continue
            drawing = Drawing(
                DrawingLibrary.pandas,
                DrawingType.box,
                {
                    'x': np.array([column]),
                    'y': data[column].to_numpy()
                }
            )
            drawings.append(drawing)
        return drawings

    @staticmethod
    def get_dis_drawings_with_normalized_data(data, x, y):
        drawings = []

        if type(data) == pd.Series:
            drawing = Drawing(
                DrawingLibrary.pandas,
                DrawingType.dis,
                {
                    'x': data.to_numpy()
                }
            )
            drawings.append(drawing)
            return

        if x:
            drawing = Drawing(
                DrawingLibrary.pandas,
                DrawingType.dis,
                {
                    'x': np.array(data[x]),
                }
            )
            drawings.append(drawing)
        if y:
            drawing = Drawing(
                DrawingLibrary.pandas,
                DrawingType.dis,
                {
                    'x': np.array(data[y]),
                }
            )
            drawings.append(drawing)

        if not x and not y:
            for column in data.columns:
                if not is_numeric_dtype(data[column]):
                    continue
                drawing = Drawing(
                    DrawingLibrary.pandas,
                    DrawingType.dis,
                    {
                        'x': data[column].to_numpy()
                    }
                )
                drawings.append(drawing)
        return drawings

    @staticmethod
    def replace_plots(drawings):
        try:
            import pandas.plotting as pd
        except ModuleNotFoundError:
            return

        import pandas.plotting
        from pandas.core.accessor import CachedAccessor

        class CustomPlotAccessor(pandas.plotting.PlotAccessor):
            def __call__(self, *args, **kwargs):
                from pandas.plotting._core import _get_plot_backend

                plot_backend = _get_plot_backend(kwargs.pop("backend", None))

                x, y, kind, kwargs = self._get_call_args(
                    plot_backend.__name__, self._parent, args, kwargs
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

                if plot_name in PandasHandler.graph_type_to_normalized_data:
                    all_drawings = PandasHandler.graph_type_to_normalized_data[plot_name](data, x, y)
                    drawings.extend(all_drawings)
                else:
                    drawing = Drawing(
                        DrawingLibrary.pandas,
                        plot_name,
                        {
                            'data': data,
                            'x': x,
                            'y': y,
                            'kwargs': kwargs
                        }
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
            self,
            column=None,
            **kwargs
        ):
            drawings.append(
                Drawing.get_hist_drawing(
                    self,
                    DrawingLibrary.pandas
                )
            )

        def hist_series(
            self,
            **kwargs
        ):
            drawings.append(
                Drawing.get_hist_drawing(
                    self,
                    DrawingLibrary.pandas
                )
            )

        if not PandasHandler._saved:
            PandasHandler._saved = True
            PandasHandler._Series_plot = pandas.Series.plot
            PandasHandler._Dataframe_plot = pandas.DataFrame.plot
            PandasHandler._Dataframe_boxplot = pandas.DataFrame.boxplot
            PandasHandler._Dataframe_hist = pandas.DataFrame.hist
            PandasHandler._Series_hist = pandas.Series.hist

        pandas.Series.plot = CachedAccessor("plot", CustomPlotAccessor)
        pandas.DataFrame.plot = CachedAccessor("plot", CustomPlotAccessor)

        pandas.DataFrame.boxplot = boxplot
        pandas.DataFrame.hist = hist
        pandas.Series.hist = hist_series

        PandasHandler._replaced = True

    @staticmethod
    def revert_plots():
        if not PandasHandler._replaced:
            return

        MatplotlibHandler.revert_plots()

        import pandas.plotting
        from pandas.core.accessor import CachedAccessor

        pandas.DataFrame.boxplot = PandasHandler._Dataframe_boxplot
        pandas.DataFrame.hist = PandasHandler._Dataframe_hist
        pandas.Series.hist = PandasHandler._Series_hist

        pandas.Series.plot = CachedAccessor("plot", pandas.plotting.PlotAccessor)
        pandas.DataFrame.plot = CachedAccessor("plot", pandas.plotting.PlotAccessor)

        PandasHandler._replaced = False
