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
            #print(p1.Ind.values[0])
            if (not (fc.__contains__(int(p1.Ind.values[0])))) & (((float(p1.Low) >= float(point.Low)) | (np.isclose(float(p1.Low), float(point.Low), atol=0.003)))):
                pStop.append(p1)
            else: return []
        if (len(pStop) >= 1):
            if (not (fc.__contains__(int(p1.Ind.values[0])))) & (((float(p1.Low) >= float(pStop[-1].Low)) | (np.isclose(float(p1.Low), float(pStop[-1].Low), atol=0.003)))):
                pStop.append(p1)
                fc.append(int(p1.Ind.values[0]))
            else: return pStop
    return pStop

def searchingU(df, point):  # ищет в df хаи ниже point и далее ниже последнего найденного
    pStop = []
    for i in range(0, len(df) - 1):
        p1 = df[i:i + 1]
        if (len(pStop) == 0):
            if (not (str(fc2).__contains__(str(p1.Ind.values[0])))) & (((float(p1.High) <= float(point.High)) | (np.isclose(float(p1.High), float(point.High), atol=0.003)))):
                pStop.append(p1)
            else:
                return []
        if (len(pStop) >= 1):
            if (not (str(fc2).__contains__(str(p1.Ind.values[0])))) & (((float(p1.High) <= float(pStop[-1].High)) | (np.isclose(float(p1.High), float(pStop[-1].High), atol=0.003)))):
                pStop.append(p1)
                fc2.append(int(p1.Ind.values[0]))
            else:
                return pStop
    return pStop


def start1(df):
# находим экстермумы
    df = df.round(2)
    df["Ind"] = df.index
    if 'Date' not in df:  # на мелких тф колонка называется Datetime
        df.rename(columns={'Datetime': 'Date'}, inplace=True)
    n = 3
    df['Minimum'] = df.iloc[argrelextrema(df.Low.values, np.less_equal, order=n)[0]]['Low']
    df['Maximum'] = df.iloc[argrelextrema(df.High.values, np.greater_equal, order=n)[0]]['High']
    pointsMin = df['Minimum'].values.tolist()
    pointsMax = df['Maximum'].values.tolist()
# делаем выборку строк где есть экстремумы
    dfmm = df.query("Minimum > 0 or Maximum > 0")
    dfmm["Ind"] = dfmm.index  # добавляем колнку с индексом
    #df.index = df.Ind


    count = 0
    count2 = 0
    dfmax = dfmm.query("Maximum > 0")  # отделяем фреймы с мин и макс
    dfmin = dfmm.query("Minimum > 0")
    points1 = []
    points2 = []
    ind = 0

    for index, row in dfmax.iterrows():
        found = searchingU(dfmax[count:], row)
        if (len(found) > 2):
            ind = (found[-1].Ind.values[0])
            #print(found)
            try:
                dfI = df.loc[(df['Ind'] == ind)]
            except: dfI = df[-1:]
            #print(df)
            #print('found', found)
            points1.append([((row.Date), float(row.High)),((dfI.Date[-1:].values[0]), float(found[-1].High))])
            found.clear()
        count += 1

    for index, row2 in dfmin.iterrows():
        found2 = searchingD(dfmin[count2:], row2)
        if (len(found2) > 2):
            ind = (found2[-1].Ind.values[0])
            try:
                dfI = df.loc[(df['Ind'] == ind)]
            except: dfI = df[-1:]
            points2.append([((row2.Date), float(row2.Low)), ((dfI.Date[-1:].values[0]), float(found2[-1].Low))])
            found2.clear()
        count2 += 1
    points4 = points1+points2
    return [pointsMin, pointsMax, points4]


fc = []
fc2 = []
#start1()