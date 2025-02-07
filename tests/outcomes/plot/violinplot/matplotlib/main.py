def plot():
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    plt.violinplot([[1, 2, 4], 2, 1])
    ax.violinplot([1, 2, 5])

    plt.show()


plot()
