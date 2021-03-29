import csv
import pandas as pd
import os
from datetime import date

folder = '/home/linac/Рабочий стол/data/stat/stat.csv'
def addStat (list):
    file = open(folder, 'a')
    with file:
        writer = csv.writer(file)
        writer.writerow(list)
    file.close()


def checkStat ():
    df = pd.read_csv(folder)
    for index, row in df.iterrows():
        try:
            df.CurrentPoint[index] = updateCurrentPoint(row.Ticker)
        except: pass
        if (row.Trend == 'own') & (float(row.CurrentPoint) >= float(row.TargetPoint)) & (row.Status == ""):
            df.Status[index] = 'Profit'
            df.FinishDate[index] = date.today()
        if (row.Trend == 'own') & (float(row.CurrentPoint) <= float(row.CancelPoint)) & (row.Status == ""):
            df.Status[index] = 'Cancel'
            df.FinishDate[index] = date.today()
        if (row.Trend == 'up') & (float(row.CurrentPoint) <= float(row.CancelPoint)) & (row.Status == ""):
            df.Status[index] = 'Profit'
            df.FinishDate[index] = date.today()
        if (row.Trend == 'up') & (float(row.CurrentPoint) >= float(row.TargetPoint)) & (row.Status == ""):
            df.Status[index] = 'Cancel'
            df.FinishDate[index] = date.today()
    df.to_csv(folder, header = True, index=False) # запись изменений в файл


def updateCurrentPoint(ticker):
    dir = '/home/linac/Рабочий стол/data/'
    dir1 = max([os.path.join(dir,d) for d in os.listdir(dir)], key = os.path.getmtime) + '/' + ticker + '.csv'
    df = pd.read_csv(dir1)
    return float(df.Close[-1:])
