from hstest.testing.plotting.drawing.drawing import Drawing
from hstest.testing.plotting.drawing.drawing_type import DrawingType
from hstest.testing.plotting.drawing_data_normalizer import DrawingDataNormalizer


class DrawingBuilder:
    @staticmethod
    def get_hist_drawing(data, library, **kwargs) -> Drawing:
        return Drawing(
            library,
            DrawingType.hist,
            DrawingDataNormalizer.normalize_hist_data(data),
            kwargs,
        )

    @staticmethod
    def get_line_drawing(x, y, library, **kwargs) -> Drawing:
        return Drawing(
            library,
            DrawingType.line,
            DrawingDataNormalizer.normalize_bar_data(x, y),
            kwargs,
        )

    @staticmethod
    def get_scatter_drawing(x, y, library, **kwargs) -> Drawing:
        return Drawing(
            library,
            DrawingType.scatter,
            DrawingDataNormalizer.normalize_bar_data(x, y),
            kwargs,
        )

    @staticmethod
    def get_pie_drawing(x, y, library, **kwargs) -> Drawing:
        return Drawing(
            library,
            DrawingType.pie,
            DrawingDataNormalizer.normalize_pie_data(x, y),
            kwargs,
        )

    @staticmethod
    def get_bar_drawing(x, y, library, **kwargs) -> Drawing:
        return Drawing(
            library,
            DrawingType.bar,
            DrawingDataNormalizer.normalize_bar_data(x, y),
            kwargs,
        )
