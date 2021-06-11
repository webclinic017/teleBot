import pandas as pd
import numpy as np
import re
import os
from scipy.signal import argrelextrema
import datetime
import mplfinance as mpf
import turnAround.WWTest as ww
#import turnAround.patterns as patterns
import turnAround.points2 as points2
#import turnAround.stat as stat
from datetime import date
import csv



pd.options.mode.chained_assignment = None  # отключение уведомлений

lines = []
ticker = ""
class Point():
    def __init__(self, df1):
        df = df1
        self.maxi = (df.Maximum > 0)
        self.mini = (df.Minimum > 0)
        self.maxiP = float(df.Maximum)
        self.miniP = float(df.Minimum)
        self.High = float(df.High)
        self.Low = float(df.Low)
        self.date = df.Date.values[0]
        self.ind = int(df.Ind)
        self.Close = int(df.Close)

def addStat(list):
    file = open('/home/linac/Рабочий стол/data/stat/testWW32.csv', 'a')
    with file:
        writer = csv.writer(file)
        writer.writerow(list)
    file.close()

def tickers(folder):
    return list(filter(lambda x: x.endswith('.csv'), os.listdir(folder)))

def mplot(df, ticker, folder, lines):
    points = points2.start1(df)
    pointsMax = points[1]
    pointsMin = points[0]
    df.index = pd.DatetimeIndex(df.Date)
    apds = [mpf.make_addplot(pointsMax, type='scatter', color='k', markersize=50, marker='.'),
            mpf.make_addplot(pointsMin, type='scatter', color='k', markersize=50, marker='.')]

    fig, axes = mpf.plot(df, type='candle', style='yahoo', title=ticker, volume=True, mav=(8, 13, 21, 55),
                         returnfig=True, addplot=apds, figscale=1.6, alines=lines, hlines=dict(hlines=lines[0][1], colors='k', linewidths=0.8))
    axes[2].set_title('ema 8,13,21,55 ')
    fig.savefig(folder + '/' + ticker + '.png')
    fig.clear()


def serching(folder, text, patternName):
    print('searching')
    global lines
    global ticker
    ticks = tickers(folder)
    for i in ticks:
        df = pd.read_csv(folder + '/' + i)
        if 'Date' not in df:  # на мелких тф колонка называется Datetime
            df.rename(columns={'Datetime': 'Date'}, inplace=True)
            df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
        ticker = str(i)[:-4]
        findWaves(df)
        #mplot(df, str(i)[:-4], folder, lines) # график

        #if (str(i) == str(ticks[-1])):
         #   print(i, ' checking...')

def findWaves(df):
    global lines
    global ticker
    print('findWaves')
# находим экстермумы
    df = df.round(2)
    df["Ind"] = df.index
    if 'Date' not in df:  # на мелких тф колонка называется Datetime
        df.rename(columns={'Datetime': 'Date'}, inplace=True)
    n = 3
    df['Minimum'] = df.iloc[argrelextrema(df.Low.values, np.less_equal, order=n)[0]]['Low']
    df['Maximum'] = df.iloc[argrelextrema(df.High.values, np.greater_equal, order=n)[0]]['High']
    pointsMin = df['Minimum'].values.tolist()  # листы со строками экстремумов из фрейма
    pointsMax = df['Maximum'].values.tolist()
# делаем выборку строк где есть экстремумы
    dfmm = df.query("Minimum > 0 or Maximum > 0") # фрейм только с экстремумами
    dfmm["Ind"] = dfmm.index  # добавляем колнку с индексом
    dfmm = dfmm.reset_index(drop=True)
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    p5 = 0
    for i, row2 in dfmm.iterrows():
        try:
            p1 = ww.Point(dfmm[i:i + 1])
            p2 = ww.Point(dfmm[i + 1:i + 2])
            p3 = ww.Point(dfmm[i + 2:i + 3])
            p4 = ww.Point(dfmm[i+3:i+4])
            p5 = ww.Point(dfmm[i + 4:i + 5])
        except: break

        if (p1.miniP > p3.miniP) & (p1.miniP < p2.maxiP) & (p1.miniP < p4.maxiP) & (
            p4.maxiP < p2.maxiP) & (p4.maxiP > p3.miniP) & (p5.miniP < p3.miniP):
            p6 = df[p5.ind + 1:p5.ind + 2] # берем следующую свечу после p5

            for str, row3 in df[p5.ind+2:].iterrows():
                if ((float(p6.Close/row3.High) *100) <= 97):
                    addStat([ticker,p6.Date[-1:].values[0],row3.Date,float(p6.Close),'',row3.High,int(p6.Ind),row3.Ind,(int(row3.Ind-p6.Ind)),'Profit'])
                    break
                if ((float(p6.Close/row3.High) *100) >= 102):
                    addStat([ticker,p6.Date[-1:].values[0],row3.Date,float(p6.Close),row3.Low,'',int(p6.Ind),row3.Ind,(int(row3.Ind-p6.Ind)),'Cancel'])
                    break


name = 'test'
patternName = 'WW'
folder1 = '/home/linac/Рабочий стол/data/20210607_10000d1d/'
serching(folder1, 'test', patternName)