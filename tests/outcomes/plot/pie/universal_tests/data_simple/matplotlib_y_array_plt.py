def plot():
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return
    plt.pie([1, 2, 3], labels=["Mercury", "Venus", "Earth"])

    plt.show()


plot()
