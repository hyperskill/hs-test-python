def plot():
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))

    ax.hist([1, 2, 3, 4, 5])
    plt.hist([1.4, 5, 1, 2, 6, 5])
    plt.hist([1, 4, 2, "1"])
    plt.hist(["1", "a", "5", "2", "b", "bb", "aa"])
    plt.hist([1.1, 5, 2, "1.1", "5"])
    plt.hist([1.1, 2.5, 2.1, 1.5, 3.6])

    plt.show()


plot()
