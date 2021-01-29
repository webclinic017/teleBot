import pandas as pd
import time
import yfinance as yf
import os
from turnAround.download import download as dd
from turnAround.download import checkFolder as dCheck

from turnAround.trend import trendSort as ts
import turnAround.patterns as patterns
import re

'''
Управляет скачиванием данных, определением тренда и запуском стратегий
startTurnaroundPattern - принимает на вход интервал(tf), название паттерна(patternName), ключ проверки данных(key)
функция проверяет наличие каталогов с указанным интервалом, если она есть, то вернет боту False, бот в свою очередь 
предложит пользователю выбор. Иначе функция вернет список путей до созданных каталогов.
В случе, если интервал == Все, то проверка делается по всем интервалам. Переменная key - целое число, является 
индикатором проверки наличия каталога с указанным интервалом.
'''

timeFrame = {'День': ['60d', '1d'], 'Час': ['10d', '60m'], '30': ['6d', '30m'], '15': ['4d', '15m'], '5': ['1d', '5m']}
funcs = {'Разворот': patterns.anyPattern, 'Вложенные': patterns.anyPattern}

def startTurnaroundPattern(tf, patternName, key):
    allFolders = []
    global timeFrame
    global funcs
    if re.search(r"[в|В]се$", str(tf)):
        check = []
        for j in timeFrame.keys(): # проверяем, существуют ли каталоги
            check.append(dCheck(timeFrame.get(j)[0], timeFrame.get(j)[1]))
        if (check.__contains__(True)) & (key == 0): # если каталог существует и это первая проверка
            return False
        elif (not (check.__contains__(True))) & (key == 0):
            return True
        else:
            for i in timeFrame.keys():
                pathList = dd(timeFrame.get(i)[0], timeFrame.get(i)[1], key)
                ts(pathList)
                funcs.get(patternName)(pathList[1], pathList[-1], patternName)
                funcs.get(patternName)(pathList[2], pathList[-1], patternName)
                allFolders += pathList[:-1] #исключаем folderName
            return allFolders
    else:
        if (dCheck(timeFrame.get(tf)[0], timeFrame.get(tf)[1])) & (key == 0): # если каталог существует и это первая проверка:
            return False
        elif (not (dCheck(timeFrame.get(tf)[0], timeFrame.get(tf)[1]))) & (key == 0):
            return True
        else:
            pathList = dd(timeFrame.get(tf)[0], timeFrame.get(tf)[1], key)
            ts(pathList)
            funcs.get(patternName)(pathList[1], pathList[-1], patternName)
            funcs.get(patternName)(pathList[2], pathList[-1], patternName)
            allFolders += pathList[:-1] #исключаем folderName
        return allFolders