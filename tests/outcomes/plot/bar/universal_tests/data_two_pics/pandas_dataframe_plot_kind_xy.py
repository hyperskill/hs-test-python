def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(
        np.array([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7], [5, 6, 7, 8]]),
        columns=['one', 'two', 'three', 'four']
    )

    df.plot(x='one', y=['two', 'three'], kind='bar')

    plt.show()


plot()
