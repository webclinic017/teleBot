import pandas as pd
import numpy as np
import re
import turnAround.points as points
from scipy.signal import argrelextrema
import datetime
import mplfinance as mpf

pd.options.mode.chained_assignment = None  # отключение уведомлений


class Point():
    def __init__(self, df1):
        df = df1
        self.Maxi = (df.Maximum > 0)
        self.Mini = (df.Minimum > 0)
        self.MaxiP = float(df.Maximum)
        self.MiniP = float(df.Minimum)
        self.High = float(df.High)
        self.Low = float(df.Low)



def searchingD(df, point):  # ищет в df лоу выше point и далее выше последнего найденного
    global fc
    pStop = []
    for i in range(0, len(df) - 1):
        p1 = df[i:i + 1]
        if (len(pStop) == 0):
            print(fc)
            if (not (fc.__contains__(int(p1.Ind)))) & (((float(p1.Low) >= float(point.Low)) | (np.isclose(float(p1.Low), float(point.Low), atol=0.25)))):
                pStop.append(p1)
            else: return []
        if (len(pStop) >= 1):
            if (not (fc.__contains__(int(p1.Ind)))) & (((float(p1.Low) >= float(pStop[-1].Low)) | (np.isclose(float(p1.Low), float(pStop[-1].Low), atol=0.25)))):
                pStop.append(p1)
                fc.append(int(p1.Ind))
            else: return pStop
    return pStop

def searchingU(df, point):  # ищет в df хаи ниже point и далее ниже последнего найденного
    pStop = []
    for i in range(0, len(df) - 1):
        p1 = df[i:i + 1]
        if (len(pStop) == 0):
            if (not (str(fc2).__contains__(str(p1.Ind)))) & (((float(p1.High) <= float(point.High)) | (np.isclose(float(p1.High), float(point.High), atol=0.080)))):
                pStop.append(p1)
            else:
                return []
        if (len(pStop) >= 1):
            if (not (str(fc2).__contains__(str(p1.Ind)))) & (((float(p1.High) <= float(pStop[-1].High)) | (np.isclose(float(p1.High), float(pStop[-1].High), atol=0.080)))):
                pStop.append(p1)
                fc2.append(p1.Ind)
            else:
                return pStop
    return pStop




def start1():
    df = pd.read_csv('/home/linac/Рабочий стол/data/test/EGP(y)eqSh.csv')
# находим экстермумы
# df["Ind"] = df.index # колонка индексов
    df = df.round(2)
    n = 2
    df['Minimum'] = df.iloc[argrelextrema(df.Low.values, np.less_equal, order=n)[0]]['Low']
    df['Maximum'] = df.iloc[argrelextrema(df.High.values, np.greater_equal, order=n)[0]]['High']
    pointsMin = df['Minimum'].values.tolist()
    pointsMax = df['Maximum'].values.tolist()
# делаем выборку строк где есть экстремумы
    dfmm = df.query("Minimum > 0 or Maximum > 0")
# dfmm = dfmm.reset_index(drop=True)  # сброс индексов с 0
    dfmm["Ind"] = dfmm.index  # добавляем колнку с индексом

# for m in dfmm[1:3].iterrows(): #works!
#    print(m[0])

    count = 0
    count2 = 0
    dfmax = dfmm.query("Maximum > 0")  # отделяем фреймы с мин и макс
    dfmin = dfmm.query("Minimum > 0")
    # end = min(len(dfmax), len(dfmin))  # выбираем наименьший по количеству строк
    # start = 1
    points1 = []
    points2 = []

    for index, row in dfmax.iterrows():
        found = searchingU(dfmax[count:], row)
        if (len(found) > 2):
            points1.append([(str(row.Date).replace(" ", '')[:10], float(row.High)),
                            (str(found[-1].Date)[-36:-26], float(found[-1].High))])
            found.clear()
        count += 1

    for index, row2 in dfmin.iterrows():
        found2 = searchingD(dfmin[count2:], row2)
        if (len(found2) > 2):
            points2.append([(str(row2.Date).replace(" ", '')[:10], float(row2.Low)),
                            (str(found2[-1].Date)[-36:-26], float(found2[-1].Low))])
            found2.clear()
        count2 += 1

    points4 = points1+points2
    df.index = pd.DatetimeIndex(df.Date)
    apds = [mpf.make_addplot(pointsMax, type='scatter', color='k', markersize=50, marker='.'),
            mpf.make_addplot(pointsMin, type='scatter', color='k', markersize=50, marker='.')]
    fig, axes = mpf.plot(df, type='candle', style='yahoo', volume=True, mav=(8, 13, 21, 55),
                         returnfig=True, addplot=apds, alines=points4, figscale=1.6)
    fig.savefig('/home/linac/Рабочий стол/data/test/EGP.png')






'''
for i in range(start, end - 2):
    startMax = dfmax[i:i + 1]
    startMin = dfmin[i:i + 1]

    p2 = dfmax[i + 1:i + 2]
    p3 = dfmax[i + 2:i + 3]
    p4 = dfmin[i + 1:i + 2]
    p5 = dfmin[i + 2:i + 3]
    if ((float(p2.High) < float(startMax.High)) | (np.isclose(float(p2.High), float(startMax.High), atol=0.010))) & (
            (float(p4.Low) >= float(startMin.Low)) | (np.isclose(float(p4.Low), float(startMin.Low), atol=0.010))):
        count = 4
        if ((float(p3.High) < float(startMax.High)) | (
                np.isclose(float(p3.High), float(startMax.High), atol=0.010))) & (
                (float(p5.Low) >= float(startMin.Low)) | (np.isclose(float(p5.Low), float(startMin.Low), atol=0.010))):
            count = 5
            endMax = p3  # if float(p2.High) >= float(p3.High) else p3
            endMin = p5  # if float(p4.Low) >= float(p5.Low) else p5
            if (count == 5):
                points1.append([(str(startMax.Date)[6:16], float(startMax.High)),
                                (str(endMax.Date)[6:16], float(endMax.High))])
                points1.append([(str(startMin.Date)[6:16], float(startMin.Low)),
                                (str(endMin.Date)[6:16], float(endMin.Low))])

                start = i + 3
                count = 0
'''
fc = []
fc2 = []
start1()