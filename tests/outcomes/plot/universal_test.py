from hstest.exception.outcomes import WrongAnswer


def universal_test(file, plot_type, correct_data_x, correct_data_y, figures):
    if len(correct_data_x) != len(correct_data_y):
        raise WrongAnswer('Correct answers should be of the same length')

    if len(figures) != len(correct_data_x):
        raise WrongAnswer(
            f"Should be {len(correct_data_x)} plot(s), "
            f"found {len(figures)}\n\n{file}"
        )

    for figure, corr_x, corr_y in zip(figures, correct_data_x, correct_data_y):
        if figure.type != plot_type:
            raise WrongAnswer(
                f"Should be plot with type={plot_type}, "
                f"found {figure.type}\n\n{file}"
            )

        found_data_x = figure.data.x.tolist()
        found_data_y = figure.data.y.tolist()

        if corr_x != found_data_x:
            raise WrongAnswer(
                f"{file}\n\n"
                f"Found data: {found_data_x}\n"
                f"Right data: {corr_x}"
            )

        if corr_y != found_data_y:
            raise WrongAnswer(
                f"{file}\n\n"
                f"Found data: {found_data_y}\n"
                f"Right data: {corr_y}"
            )

    print(plot_type.capitalize(), file, 'OK')
