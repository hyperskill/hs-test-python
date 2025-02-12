from hstest import correct, wrong


def test_box_drawing(figures, correct_plot_count, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f"Expected {correct_plot_count} plots to be plotted "
            f"using {library_type} library, found {len(figures)}"
        )

    for i, box in enumerate(figures):
        if box.type != "box":
            return wrong(f"Wrong drawing type {box.type}. Expected box")

        if box.library != library_type:
            return wrong(
                f"{box.library} is wrong library type. Expected {library_type}"
            )

        if box.data is not None:
            return wrong("The data value should be None")

    return correct()
