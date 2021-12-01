import numpy as np

from hstest.testing.plotting.drawing_data_normalizer import DrawingDataNormalizer


class Drawing:
    def __init__(self, library: str, plot_type: str, data: np.ndarray):
        self.library: str = library
        self.type: str = plot_type
        self.data: np.ndarray = data

    @staticmethod
    def get_hist_drawing(data, library) -> 'Drawing':
        return Drawing(
            library,
            DrawingType.hist,
            DrawingDataNormalizer.normalize_hist_data(data)
        )

    @staticmethod
    def get_line_drawing(x, y, library):
        return Drawing(
            library,
            DrawingType.line,
            DrawingDataNormalizer.normalize_line_data(x, y)
        )

    @staticmethod
    def get_scatter_drawing(x, y, library):
        return Drawing(
            library,
            DrawingType.scatter,
            DrawingDataNormalizer.normalize_scatter_data(x, y)
        )

    @staticmethod
    def get_pie_drawing(x, y, library):
        return Drawing(
            library,
            DrawingType.pie,
            DrawingDataNormalizer.normalize_pie_data(x, y)
        )

    @staticmethod
    def get_bar_drawing(x, y, library):
        return Drawing(
            library,
            DrawingType.bar,
            DrawingDataNormalizer.normalize_bar_data(x, y)
        )


class DrawingLibrary:
    matplotlib = "matplotlib"
    pandas = "pandas"
    seaborn = "seaborn"


class DrawingType:
    # common types
    hist = "hist"
    line = "line"
    scatter = "scatter"
    pie = "pie"
    bar = "bar"
    violin = "violin"
    heatmap = "heatmap"
    box = "box"
    dis = "dis"  # distribution plot (pandas' density, seaborn' displot)

    # pandas
    kde = "kde"
    density = "density"
    area = "area"
    hexbin = "hexbin"

    # seaborn
    lm = "lm"
    cat = "cat"
