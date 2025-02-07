import numpy as np

from hstest import correct, wrong


def test_line_drawing(figures, correct_plot_count, correct_data, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f"Expected {correct_plot_count} plots to be plotted "
            f"using {library_type} library, found {len(figures)}"
        )

    for i, line in enumerate(figures):
        if line.type != "line":
            return wrong(f"Wrong drawing type {line.type}. Expected line")

        if line.library != library_type:
            return wrong(
                f"{line.library} is wrong library type. Expected {library_type}"
            )

        if not isinstance(line.data, np.ndarray):
            return wrong("The data value should be a ndarray")

        if not np.array_equal(correct_data[i], line.data.data):
            return wrong("Wrong data of the line graph")

    return correct()
