def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(np.random.randn(10, 2), columns=["Col1", "Col2"])
    df["X"] = pd.Series(["A", "A", "A", "A", "A", "B", "B", "B", "B", "B"])
    boxplot = df.boxplot(by="X")
    plt.show()


plot()
