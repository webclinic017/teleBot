import pandas as pd
import yfinance as yf
import os
import talib
import mplfinance as mpf


def mplot(df, signal, ticker, folder):
    df.index = pd.to_datetime(df.Date)  # выставляем столбик с датой как индекс
    apds = [mpf.make_addplot(signal, type='scatter', color='r', markersize=70, marker='v')]
    # mpf.make_addplot(hammerMan.man(df), type='scatter', color='r', markersize=70, marker='o')]
    fig, axes = mpf.plot(df, type='candle', volume=True, mav=(10, 55), returnfig=True, addplot=apds, figscale=1.3)
    axes[0].set_title(ticker)
    axes[2].set_title('ema 10,55 ')
    fig.savefig(folder + '/' + ticker + '.png')
    fig.clear()
