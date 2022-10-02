def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(np.array([[1, 2], [2, 3], [3, 4]]),
                      columns=['one', 'two'], index=['Mercury', 'Venus', 'Earth'])

    df.plot.pie(subplots=True)

    plt.show()


plot()
