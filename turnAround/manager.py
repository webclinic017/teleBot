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

def startTurnaroundPattern(tf):
    allFolders = []
    timeFrame = {'День': ['60d', '1d'], 'Час': ['10d', '60m'], '30': ['6d', '30m'], '15': ['4d', '15m'], '5': ['1d', '5m']}
    if re.search(r"[в|В]се$", str(tf)):
        for i in timeFrame.keys():
            pathList = dd(timeFrame.get(i)[0], timeFrame.get(i)[1])
            ts(pathList)
            patterns.anyPattern(pathList[1], pathList[-1])
            patterns.anyPattern(pathList[2], pathList[-1])
            allFolders += pathList[:-1] #исключаем folderName
    else:
        pathList = dd(timeFrame.get(tf)[0], timeFrame.get(tf)[1])
        ts(pathList)
        patterns.anyPattern(pathList[1], pathList[-1])
        patterns.anyPattern(pathList[2], pathList[-1])
        allFolders += pathList[:-1] #исключаем folderName
    return allFolders