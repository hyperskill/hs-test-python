def plot():
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))

    # Matplotlib
    # basics

    plt.hist([1, 2])
    ax.hist([1, 5])

    plt.plot([1, 2], [5, 8])
    ax.plot([1, 5], [5, 8])

    plt.scatter([1, 2], [2, 6])
    ax.scatter([1, 5], [3, 8])

    plt.pie([1, 2])
    ax.pie([1, 2])

    plt.bar([1, 2, 4, 6], 100)
    ax.bar([1, 2, 4, 6], 100)

    plt.barh([1, 2, 4, 6], 100)
    ax.barh([1, 2, 4, 6], 100)

    plt.violinplot([1, 2, 4])
    ax.violinplot([1, 2, 4])

    smile = [[0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
             [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
             [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]]

    plt.imshow(smile)
    ax.imshow(smile)

    plt.boxplot([1, 2, 4])
    ax.boxplot([1, 2, 4])


plot()
