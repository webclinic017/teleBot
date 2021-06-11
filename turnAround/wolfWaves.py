import pandas as pd
import numpy as np
import re
import os
from scipy.signal import argrelextrema
import datetime
import mplfinance as mpf
import turnAround.wolfWaves as ww
import turnAround.patterns as patterns
import turnAround.points2 as points2
import turnAround.stat as stat
import turnAround.ib2 as ib2
from datetime import date


pd.options.mode.chained_assignment = None  # отключение уведомлений

lines = []
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


'''
Бычий паттерн:
Нахождение точек:
Точка 1 – эта первая точка является основанием первой волны (минимум первой волны).
Точка 2 – это максимум первой волны (вершина первой волны). В то же время она является основанием второй волны. 
Это самая главная точка, на ее основе строятся все оставшиеся точки. Она является первой вершиной в паттерне, который мы ищем.
Точка 3 – это окончание второй волны и в то же время начало третьей (минимум второй волны и основание третьей). 
Данная точка является следующим минимумом паттерна после точки 1.
Точка 4 – это максимум волны три и основание волны 4. Является новым максимумом после точки 2.
Точка 5 – это точка разворота, вычислив которую, мы находим точку для входа в рынок, именно для ее нахождения 
производится все предыдущее построение. Для того чтобы ее найти, следует провести важную вспомогательную линию 
из точки 1 в точку 3. Когда цена достигнет этой линии, паттерн считается приемлемым для открытия торговой позиции. 
В этом месте устанавливается точка 5 и открывается сделка.
Точка 6 – это точка, в которой устанавливается цель по прибыли. Формируется она на основе вспомогательной линии, 
проведенной из точки 1 в точку 4. Когда цена достигает этой линии, сделку следует закрыть, и считается, что эта модель отработала.

Дополнительно:
Точка 1 должна соблюдать такие условия, как находиться выше точки 3 и ниже точки 2 и 4.
Точка 2 находится выше точки 1.
Точка 3 находится ниже точки 1.
Точка 4 находится ниже точки 2 и выше точки 3.
Точка 5 всегда находится ниже точки 3.
Точки 1-3-5 находятся на одной линии.
'''
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
    global lines
    ticks = tickers(folder)
    for i in ticks:
        df = pd.read_csv(folder + '/' + i)
        if 'Date' not in df:  # на мелких тф колонка называется Datetime
            df.rename(columns={'Datetime': 'Date'}, inplace=True)
            df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)

        if findWaves(df):
                #print(str(i)[:-4])
            mplot(df, str(i)[:-4], folder, lines) # график
            # статистика
            stat.addStat([str(i)[:-4], patternName, str(folder).replace('/home/linac/Рабочий стол/data/',''), 'noTrend', date.today(),
                              float(df.Close[-1:]),
                              float(df.Close[-1:]) * 1.07, float(df.Close[-1:]) * 0.93, float(df.Close[-1:])])
            try:
                ib2.starHere(str(i)[:-4], float(df.Close[-1:]), float(df.Close[-1:]) * 1.02, float(df.Close[-1:]) * 0.98)
            except: pass

        if (str(i) == str(ticks[-1])):
            print(i, ' checking...')
            stat.checkStat()

def findWaves(df):
    global lines
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

    #for i, row2 in dfmm.iterrows():
    try:
        p1 = ww.Point(dfmm[-5:-4])
        p2 = ww.Point(dfmm[-4:-3])
        p3 = ww.Point(dfmm[-3:-2])
        p4 = ww.Point(dfmm[-2:-1])
        p5 = ww.Point(dfmm[-1:])
    except: return False
            #p1 = ww.Point(dfmm[i:i + 1])
            #p2 = ww.Point(dfmm[i + 1:i + 2])
            #p3 = ww.Point(dfmm[i + 2:i + 3])
            #p4 = ww.Point(dfmm[i+3:i+4])
            #p5 = ww.Point(dfmm[i + 4:i + 5])


        #print(p1.miniP > p3.miniP, p1.miniP < p2.maxiP, p1.miniP < p4.maxiP,p4.maxiP < p2.maxiP, p4.maxiP > p3.miniP, p5.miniP < p3.miniP)

    if (p1.miniP > p3.miniP) & (p1.miniP < p2.maxiP) & (p1.miniP < p4.maxiP) & (
            p4.maxiP < p2.maxiP) & (p4.maxiP > p3.miniP) & (p5.miniP < p3.miniP):
        lines = [(p1.date,p1.Low), (p2.date,p2.High), (p3.date,p3.Low), (p4.date,p4.High), (p5.date,p5.Low)]
        return True



name = 'test'
patternName = 'WW'#
folder1 = '/home/linac/Рабочий стол/data/20210611_60d1d'
ww.serching(folder1, 'test', patternName)