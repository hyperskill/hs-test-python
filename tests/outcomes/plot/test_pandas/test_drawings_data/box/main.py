def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt

    except ModuleNotFoundError:
        return

    df = pd.DataFrame([[1, 2], [3, 4]],
                      columns=['Col1', 'Col2'])
    df.boxplot(column=['Col1'])
    df.plot.box()

    plt.show()


plot()
