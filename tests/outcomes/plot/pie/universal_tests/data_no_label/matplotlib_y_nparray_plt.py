def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ModuleNotFoundError:
        return

    plt.pie(np.array([1, 2, 3]))

    plt.show()


plot()
