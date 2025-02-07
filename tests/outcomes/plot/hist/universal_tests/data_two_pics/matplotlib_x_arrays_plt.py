def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ModuleNotFoundError:
        return

    plt.hist(np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]))
    plt.show()


plot()
