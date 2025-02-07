def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import seaborn as sns
    except ModuleNotFoundError:
        return

    sns.histplot(np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]), bins=10)

    plt.show()


plot()
