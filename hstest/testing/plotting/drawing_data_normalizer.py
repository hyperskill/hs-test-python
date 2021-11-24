import numpy as np


class DrawingDataNormalizer:

    @staticmethod
    def normalize_hist_data(data):

        if type(data) != list:
            try:
                data = list(data)
            except Exception as _:
                raise ValueError('The data argument should be an array')

        # The data can't be sorted because it may contain mixed data types
        data_wo_duplicates = list(set(data))
        result_data = list()

        for element in data_wo_duplicates:
            result_data.append((element, data.count(element)))

        return np.array(result_data)
