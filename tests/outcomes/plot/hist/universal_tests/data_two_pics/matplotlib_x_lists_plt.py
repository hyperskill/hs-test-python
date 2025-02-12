def plot():
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    plt.hist([[1, 3, 5, 7, 9], [2, 4, 6, 8, 10]])
    plt.show()


plot()
