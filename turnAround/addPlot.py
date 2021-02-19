import pandas as pd
import yfinance as yf
import os
import talib
import mplfinance as mpf
import numpy as np


def mplot(df, signal, ticker, folder, folderName, patternName):
    df.index = pd.to_datetime(df.Date)  # выставляем столбик с датой как индекс
    apds = [mpf.make_addplot(signal, type='scatter', color='r', markersize=70, marker='v')]

    # объединияем все столбцы в один и ищем наиболее частые совпадения
    columnlist = ['Open', 'Close', 'High', 'Low']
    df2 = pd.concat(map(df.get, columnlist)).reset_index(drop=True)
    df2 = df2.round(2) # округление
    lines = []
    count = 0
    for i in list(df2.value_counts()):
        if i >= 3:
            lines.append(df2.value_counts().keys()[count])
        count += 1
    fig, axes = mpf.plot(df, type='candle', style='yahoo', title=ticker, volume=True, mav=(8, 13, 21, 55),
                         returnfig=True, addplot=apds, figscale=1.6,
                         hlines=dict(hlines=lines, colors='b', linewidths=7, alpha=0.08))
    # tdates = [(df.index[0], df.index[-1])]
    # fig, axes = mpf.plot(df, type='candle', style='yahoo', title=ticker, volume=True, mav=(8, 13, 21, 55),
    #                     returnfig=True, addplot=apds, figscale=1.6, tlines=[
    #        dict(tlines=tdates, tline_use=['Open', 'Close', 'High', 'Low'], tline_method='least-squares', colors='r',
    #             linewidths=(0.5))])

    axes[0].set_title(patternName + '       (' + folderName + ')' + "       buy = , stop = , take = ")
    axes[2].set_title('ema 8,13,21,55 ')
    fig.savefig(folder + '/' + ticker + '.png')
    fig.clear()


'''
direct = '/home/linac/Рабочий стол/data/20210116_60d1d/up/'
allCsv = list(filter(lambda x: x.endswith('.csv'), os.listdir(direct)))
for i in allCsv:
    df = pd.read_csv(direct + '/' + i)
    df['signal'] = np.nan
    df.signal[-2:-1] = float(df.High[-2:-1]) * 1.01
    mplot(df, df.signal, i, direct, 'test')
'''
