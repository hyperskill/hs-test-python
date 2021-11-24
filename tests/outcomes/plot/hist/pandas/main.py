def plot():
    try:
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(np.array([1, 2, 3, 4, 5]), columns=['one'])
    df['two'] = df['one'] + np.array([1, 7, 3, 2, 1])

    df.plot.hist(bins=12, alpha=0.5)
    df.plot(kind='hist', bins=12, alpha=0.5)

    d = {'a': 1, 'b': 2, 'c': 3}
    ser = pd.Series(data=np.array([1, 2, 3, 4, 5]))
    ser.hist()

    import matplotlib.pyplot as plt

    plt.show()


plot()
