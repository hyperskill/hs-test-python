from hstest import correct, wrong


def test_hexbin_drawing(figures, correct_plot_count, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f"Expected {correct_plot_count} plots to be plotted "
            f"using {library_type} library, found {len(figures)}"
        )

    for i, hexbin in enumerate(figures):
        if hexbin.type != "hexbin":
            return wrong(f"Wrong drawing type {hexbin.type}. Expected hexbin")

        if hexbin.library != library_type:
            return wrong(
                f"{hexbin.library} is wrong library type. Expected {library_type}"
            )

        if hexbin.data is not None:
            return wrong("The data value should be None")

    return correct()
