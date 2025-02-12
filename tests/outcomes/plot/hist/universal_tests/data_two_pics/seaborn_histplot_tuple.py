def plot():
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ModuleNotFoundError:
        return

    sns.histplot(((1, 3, 5, 7, 9), (2, 4, 6, 8, 10)), bins=10)

    plt.show()


plot()
