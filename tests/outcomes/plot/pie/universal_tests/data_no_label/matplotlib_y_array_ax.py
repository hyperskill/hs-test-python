def plot():
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))

    ax.pie([1, 2, 3])

    plt.show()


plot()
