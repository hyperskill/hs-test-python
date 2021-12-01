import numpy as np


class DrawingDataNormalizer:

    @staticmethod
    def normalize_x_y_data(x, y):
        try:
            if type(x) != list:
                x = list(x)
            if type(y) != list:
                y = list(y)
        except Exception as _:
            raise ValueError('The data argument should be an array')

        if len(x) != len(y):
            raise ValueError('Arrays should be the same length')

        result_data = list()

        for a, b in zip(x, y):
            result_data.append((a, b))

        return np.array(result_data, dtype=object)

    @staticmethod
    def normalize_hist_data(data):

        if type(data) != list:
            try:
                data = list(data)
            except Exception as _:
                raise ValueError('The data argument should be an array')

        if len(set(type(i) for i in data)) == 1:
            data.sort()

        data = []

        for i in data:
            if type(i) == str:
                if i.isdigit():
                    data += [int(i)]
                else:
                    try:
                        data += [float(i)]
                    except ValueError:
                        data += [i]
            else:
                data += [i]

        data_wo_duplicates = list(set(data))
        result_data = list()

        for element in data_wo_duplicates:
            result_data.append((element, data.count(element)))

        return np.array(result_data)

    @staticmethod
    def normalize_bar_data(x, y):
        return DrawingDataNormalizer.normalize_x_y_data(x, y)

    @staticmethod
    def normalize_line_data(x, y):
        return DrawingDataNormalizer.normalize_x_y_data(x, y)

    @staticmethod
    def normalize_scatter_data(x, y):
        return DrawingDataNormalizer.normalize_x_y_data(x, y)

    @staticmethod
    def normalize_pie_data(x, y):
        return DrawingDataNormalizer.normalize_x_y_data(x, y)
