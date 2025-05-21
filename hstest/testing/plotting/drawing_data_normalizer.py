from __future__ import annotations

import numpy as np


class DrawingDataNormalizer:
    @staticmethod
    def normalize_x_y_data(x, y) -> np.ndarray:
        try:
            if type(x) != list:
                x = list(x)
            if type(y) != list:
                y = list(y)
        except Exception:
            msg = "The data argument should be an array"
            raise ValueError(msg)

        if len(x) != len(y):
            msg = "Arrays should be the same length"
            raise ValueError(msg)

        result_data = []

        for a, b in zip(x, y, strict=False):
            result_data.append((a, b))

        return np.array(result_data, dtype=object)

    @staticmethod
    def normalize_hist_data(data) -> np.ndarray:
        if type(data) == str:
            data = [data]

        if type(data) != list:
            try:
                data = list(data)
            except Exception:
                msg = "The data argument should be an array"
                raise ValueError(msg)

        return np.array(data, dtype=object)

        """ Code below tries to deduplicate histogram data and sort it
        
        data_types = set([type(i) for i in data])

        if str in data_types:
            parsed_data = [str(i) for i in data]
        else:
            parsed_data = data

        if len(data_types) == 1:
            parsed_data = sorted(parsed_data)
        if len(data_types) == 2 and (int in data_types and float in data_types):
            parsed_data = sorted(parsed_data)

        no_duplicates = list(set(parsed_data))
        result_data = list()

        for element in parsed_data:
            if element not in no_duplicates:
                continue
            else:
                no_duplicates.remove(element)

            occurrence = parsed_data.count(element)
            if type(element) == str:
                if element.isdigit():
                    element = int(element)
                else:
                    try:
                        element = float(element)
                    except ValueError:
                        pass
            result_data.append((element, occurrence))

        return np.array(result_data, dtype=object)
        """  # noqa: W293
        return None

    @staticmethod
    def normalize_bar_data(x, y) -> np.ndarray:
        return DrawingDataNormalizer.normalize_x_y_data(x, y)

    @staticmethod
    def normalize_line_data(x, y) -> np.ndarray:
        return DrawingDataNormalizer.normalize_x_y_data(x, y)

    @staticmethod
    def normalize_scatter_data(x, y) -> np.ndarray:
        return DrawingDataNormalizer.normalize_x_y_data(x, y)

    @staticmethod
    def normalize_pie_data(x, y) -> np.ndarray:
        return DrawingDataNormalizer.normalize_x_y_data(x, y)
