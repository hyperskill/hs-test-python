def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ModuleNotFoundError:
        return

    plt.hist(np.array([1, 2, 3, 4, 5]))
    plt.show()


plot()
