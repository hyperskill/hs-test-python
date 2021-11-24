from hstest.testing.plotting.drawing_data_normalizer import DrawingDataNormalizer


class Drawing:
    def __init__(self, library, plot_type, data):
        self.library = library
        self.type = plot_type
        self.data = data

    @staticmethod
    def get_hist_drawing(data, library):
        return Drawing(
            library,
            DrawingType.hist,
            DrawingData(
                DrawingDataNormalizer.normalize_hist_data(data)
            )
        )


class DrawingData:
    def __init__(self, data):
        self.data = data


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
