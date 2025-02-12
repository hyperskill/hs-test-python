def plot():
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))

    plt.scatter([1, 2], [2, 6])
    ax.scatter([1, 2], [2, 6])

    plt.show()


plot()
