import pandas as pd
import yfinance as yf
import os
import talib
import mplfinance as mpf
import numpy as np


def mplot(df, signal, ticker, folder, folderName):
    df.index = pd.to_datetime(df.Date)  # выставляем столбик с датой как индекс
    apds = [mpf.make_addplot(signal, type='scatter', color='r', markersize=70, marker='v')]
    # mpf.make_addplot(hammerMan.man(df), type='scatter', color='r', markersize=70, marker='o')]
    fig, axes = mpf.plot(df, type='candle',style ='yahoo', title = ticker, volume=True, mav=(10, 55), returnfig=True, addplot=apds, figscale=1.6)
    axes[0].set_title('(' + folderName + ')' + "       buy = , stop = , take = ")
    axes[2].set_title('ema 10,55 ')
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