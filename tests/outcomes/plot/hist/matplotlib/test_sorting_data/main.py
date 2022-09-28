def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))

    plt.hist([3, 2, 1])
    plt.hist([3, 2, '1'])
    plt.hist(['3', '2', '1'])
    plt.hist([3.1, 2.1, 1])
    plt.hist(['b', 'a', 'c'])
    plt.hist([1, 5, 2, '1'])

    plt.show()


plot()
