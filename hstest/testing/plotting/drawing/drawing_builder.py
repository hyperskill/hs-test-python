from hstest.testing.plotting.drawing_data_normalizer import DrawingDataNormalizer
from hstest.testing.plotting.drawing.drawing_type import DrawingType
from hstest.testing.plotting.drawing.drawing import Drawing
from hstest.testing.plotting.drawing.drawing_data import DrawingData


class DrawingBuilder:
    @staticmethod
    def get_hist_drawing(data, library) -> Drawing:
        return Drawing(
            library,
            DrawingType.hist,
            DrawingData(
                DrawingDataNormalizer.normalize_hist_data(data)
            )
        )

    @staticmethod
    def get_line_drawing(x, y, library):
        return Drawing(
            library,
            DrawingType.line,
            DrawingData(
                DrawingDataNormalizer.normalize_bar_data(x, y)
            )
        )

    @staticmethod
    def get_scatter_drawing(x, y, library):
        return Drawing(
            library,
            DrawingType.scatter,
            DrawingData(
                DrawingDataNormalizer.normalize_bar_data(x, y)
            )
        )

    @staticmethod
    def get_pie_drawing(x, y, library):
        return Drawing(
            library,
            DrawingType.pie,
            DrawingData(
                DrawingDataNormalizer.normalize_pie_data(x, y)
            )
        )

    @staticmethod
    def get_bar_drawing(x, y, library):
        return Drawing(
            library,
            DrawingType.bar,
            DrawingData(
                DrawingDataNormalizer.normalize_bar_data(x, y)
            )
        )
