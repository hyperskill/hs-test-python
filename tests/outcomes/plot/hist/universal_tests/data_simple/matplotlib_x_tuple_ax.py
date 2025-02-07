def plot():
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    ax.hist((1, 2, 3, 4, 5))
    plt.show()


plot()
