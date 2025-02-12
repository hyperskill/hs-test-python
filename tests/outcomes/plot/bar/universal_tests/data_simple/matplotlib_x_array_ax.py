def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    ax.bar(np.array([1, 2, 3, 4, 5]), [2, 3, 4, 5, 6])
    plt.show()


plot()
