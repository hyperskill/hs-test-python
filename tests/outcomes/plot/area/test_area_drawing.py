from hstest import correct, wrong


def test_area_drawing(figures, correct_plot_count, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f"Expected {correct_plot_count} plots to be plotted "
            f"using {library_type} library, found {len(figures)}"
        )

    for i, area in enumerate(figures):
        if area.type != "area":
            return wrong(f"Wrong drawing type {area.type}. Expected area")

        if area.library != library_type:
            return wrong(
                f"{area.library} is wrong library type. Expected {library_type}"
            )

        if area.data is not None:
            return wrong("The data value should be None")

    return correct()
