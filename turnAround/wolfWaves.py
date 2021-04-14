import pandas as pd
import numpy as np
import re
from scipy.signal import argrelextrema
import datetime
import mplfinance as mpf
import turnAround.wolfWaves as ww
import turnAround.patterns as patterns

pd.options.mode.chained_assignment = None  # отключение уведомлений


class Point():
    def __init__(self, df1):
        df = df1
        self.maxi = (df.Maximum > 0)
        self.mini = (df.Minimum > 0)
        self.maxiP = float(df.Maximum)
        self.miniP = float(df.Minimum)
        self.High = float(df.High)
        self.Low = float(df.Low)


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

def findWaves(df):

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
        except: return False
        #print(p1.miniP,p2.maxiP,p3.miniP,p4.maxiP)

        print(p1.miniP > p3.miniP, p1.miniP < p2.maxiP, p1.miniP < p4.maxiP,p4.maxiP < p2.maxiP, p4.maxiP > p3.miniP, p5.miniP < p3.miniP)

        if (p1.miniP > p3.miniP) & (p1.miniP < p2.maxiP) & (p1.miniP < p4.maxiP) & (
            p4.maxiP < p2.maxiP) & (p4.maxiP > p3.miniP) & (p5.miniP < p3.miniP):
            return True



#name = 'test'
#patternName = 'test'
#folder1 = '/home/linac/Рабочий стол/data/20210406_60d1d'
#patterns.anyPattern(folder1, 'test', patternName)

#start1(pd.read_csv('/home/linac/Рабочий стол/data/test/SKX.csv'))