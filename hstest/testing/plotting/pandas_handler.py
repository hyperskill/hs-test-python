import pandas as pd

from hstest.testing.plotting.drawing import Drawing, DrawingType, DrawingLibrary
from hstest.testing.plotting.matplotlib_handler import MatplotlibHandler


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
        'density': DrawingType.dis
    }

    graph_type_to_normalized_data = {
        'hist': lambda data: PandasHandler.get_hist_drawing_with_normalized_data(data)
    }

    @staticmethod
    def get_hist_drawing_with_normalized_data(data: pd.DataFrame):

        result_data = []

        for column in data.columns:
            result_data.append(data[column].to_numpy())

        drawing = Drawing(
            DrawingLibrary.pandas,
            DrawingType.hist,
            {
                'x': tuple(result_data)
            }
        )
        return drawing

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

                drawing = PandasHandler.graph_type_to_normalized_data[plot_name](data) \
                    if plot_name in PandasHandler.graph_type_to_normalized_data else \
                    Drawing(
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
            data = self
            drawing = Drawing(
                DrawingLibrary.pandas,
                DrawingType.box,
                data={
                    'data': data,
                    'column': column,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def hist(
            self,
            column=None,
            **kwargs
        ):
            drawing = PandasHandler.get_hist_drawing_with_normalized_data(self)
            drawings.append(drawing)

        def hist_series(
            self,
            **kwargs
        ):
            data = self
            drawing = Drawing(
                DrawingLibrary.pandas,
                DrawingType.hist,
                data={
                    'x': tuple(data)
                }
            )
            drawings.append(drawing)

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
