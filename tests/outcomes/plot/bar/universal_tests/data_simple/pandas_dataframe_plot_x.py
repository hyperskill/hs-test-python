def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]),
                      columns=['one', 'two'])

    df.plot.bar(x='one')

    plt.show()


plot()
