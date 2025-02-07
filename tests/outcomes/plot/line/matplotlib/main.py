def plot():
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))

    plt.plot([1, 2], [5, 8])
    ax.plot([1, 2], [5, 8])
    ax.plot([1, 5, 7, 8])

    plt.show()


plot()
