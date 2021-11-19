def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt

    except ModuleNotFoundError:
        return

    df = pd.DataFrame({'lab': ['A', 'B', 'C'], 'val': [10, 30, 20], 'val1': [5, 10, 15]})
    df.plot.bar(x='lab', rot=0)

    df.plot.bar(y='val', rot=0)

    df.plot.bar(rot=0)

    plt.show()


plot()
