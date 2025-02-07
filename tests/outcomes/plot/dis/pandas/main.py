def plot():
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except ModuleNotFoundError:
        return

    s = pd.Series([1, 2, 2.5, 3, 3.5, 4, 5])
    s.plot.kde()
    plt.show()


plot()
