def plot():
    try:
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    df = pd.DataFrame({
        'sales': [3, 2, 3, 9, 10, 6],
        'signups': [5, 5, 6, 12, 14, 13],
        'visits': [20, 42, 28, 62, 81, 50],
    }, index=pd.date_range(start='2018/01/01', end='2018/07/01',
                           freq='M'))
    df.plot.area()
    df.plot(kind='area')

    df = pd.DataFrame({'lab': ['A', 'B', 'C'], 'val': [10, 30, 20]})
    df.plot.bar(x='lab', y='val', rot=0)
    df.plot(kind='bar', x='lab', y='val', rot=0)

    df = pd.DataFrame({'lab': ['A', 'B', 'C'], 'val': [10, 30, 20]})
    df.plot.barh(x='lab', y='val')
    df.plot(kind='barh', x='lab', y='val')

    data = np.random.randn(25, 4)
    df = pd.DataFrame(data, columns=list('ABCD'))
    df.plot.box()
    df.plot(kind='box')

    s = pd.Series([1, 2, 2.5, 3, 3.5, 4, 5])
    s.plot.kde()
    s.plot(kind='kde')

    n = 10000
    df = pd.DataFrame({'x': np.random.randn(n),
                       'y': np.random.randn(n)})
    df.plot.hexbin(x='x', y='y', gridsize=20)
    df.plot(kind='hexbin', x='x', y='y', gridsize=20)

    df = pd.DataFrame(
        np.random.randint(1, 7, 6000),
        columns=['one'])
    df['two'] = df['one'] + np.random.randint(1, 7, 6000)
    df.plot.hist(bins=12, alpha=0.5)
    df.plot(kind='hist', bins=12, alpha=0.5)

    s = pd.Series([1, 3, 2])
    s.plot.line()
    s.plot(kind='line')

    df = pd.DataFrame({'mass': [0.330, 4.87, 5.97],
                       'radius': [2439.7, 6051.8, 6378.1]},
                      index=['Mercury', 'Venus', 'Earth'])
    df.plot.pie(y='mass', figsize=(5, 5))
    df.plot(kind='pie', y='mass', figsize=(5, 5))

    df = pd.DataFrame([[5.1, 3.5, 0], [4.9, 3.0, 0], [7.0, 3.2, 1],
                       [6.4, 3.2, 1], [5.9, 3.0, 2]],
                      columns=['length', 'width', 'species'])
    df.plot.scatter(x='length',
                    y='width',
                    c='DarkBlue')

    df.plot(kind='scatter', x='length',
            y='width',
            c='DarkBlue')

    np.random.seed(1234)
    df = pd.DataFrame(np.random.randn(10, 4),
                      columns=['Col1', 'Col2', 'Col3', 'Col4'])
    df.hist(column=['Col1', 'Col2', 'Col3'])

    d = {'a': 1, 'b': 2, 'c': 3}
    ser = pd.Series(data=d, index=['a', 'b', 'c'])
    ser.hist()


plot()
