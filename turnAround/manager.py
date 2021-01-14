import pandas as pd
import time
import yfinance as yf
import os
from turnAround.download import download as dd
from turnAround.trend import trendSort as ts
import turnAround.patterns as patterns
import re

'''
Управляет скачиванием данных, определением тренда и запуском стратегий
'''
'''
timeFrame = {'день': ['60d', '1d'], 'час': ['10d', '60m'], '30': ['10d', '30m'], '15': ['10d', '15m']}

pathList1 = dd(timeFrame.get('день')[0], timeFrame.get('день')[1])
ts(pathList1)
patterns.anyPattern(pathList1[1])
patterns.anyPattern(pathList1[2])
pathList2 = dd(timeFrame.get('час')[0], timeFrame.get('час')[1])
ts(pathList2)
patterns.anyPattern(pathList2[1])
patterns.anyPattern(pathList2[2])
pathList3 = dd(timeFrame.get('30')[0], timeFrame.get('30')[1])
ts(pathList3)
patterns.anyPattern(pathList3[1])
patterns.anyPattern(pathList3[2])
pathList4 = dd(timeFrame.get('15')[0], timeFrame.get('15')[1])
ts(pathList4)
patterns.anyPattern(pathList4[1])
patterns.anyPattern(pathList4[2])
'''

def startTurnaroundPattern(tf):
    allFolders = []
    timeFrame = {'день': ['60d', '1d'], 'час': ['10d', '60m'], '30': ['10d', '30m'], '15': ['10d', '15m']}
    if re.search(r"[в|В]се$", str(tf)):
        for i in timeFrame.keys():
            pathList = dd(timeFrame.get(i)[0], timeFrame.get(i)[1])
            ts(pathList)
            patterns.anyPattern(pathList[1])
            patterns.anyPattern(pathList[2])
            allFolders += pathList
    else:
        #try:
        pathList = dd(timeFrame.get(tf)[0], timeFrame.get(tf)[1])
        ts(pathList)
        patterns.anyPattern(pathList[1])
        patterns.anyPattern(pathList[2])
        allFolders += pathList
        #except:
         #   print("Неправильно указан тайм-фрейм")
    return allFolders