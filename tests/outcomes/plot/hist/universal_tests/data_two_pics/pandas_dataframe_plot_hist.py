def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]),
                      columns=['one', 'two'])

    df.plot.hist()

    plt.show()


plot()
