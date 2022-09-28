def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        import seaborn as sns
    except ModuleNotFoundError:
        return

    df = pd.DataFrame({'lab': ['A', 'B', 'C'], 'val': [10, 30, 20], 'val1': [5, 10, 15]})

    df.plot.bar()
    df.plot.bar(x='lab', y='val')

    plt.show()


plot()
