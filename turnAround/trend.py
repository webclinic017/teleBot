import pandas as pd
import time
import requests
import threading as thr
import yfinance as yf
import os
import talib
from shutil import copy as copy  # для копирования файлов

'''
Определение тренда: Берем последние 10 дней (для дневного тф), каждая из 5 любых идущих друг за другом свечей 
должны повышать свой лоу относительно предыдущей + они должны быть над 8 средней + 8 средняя все 10 свечей выше 14 средней

Для нисходящего тренда следующие требования:ниже 12 средней, берем 10 последних свечей, любые последовательные 3 из них должны 
быть под 12 и их хай должен уменьшаться

trendSort получает на вход лист из 3 путей, по 1 пути он собирает все csv файлы и проверяет их под требования 
восходящего тренда, для проверки на нисходящий тренд он задействует метод trendDown (df - проверяемый дата фрейм,
pathList - лист из 3 путей, i - название текущего документа. Во второй путь копируются отобранные файлы 
восходящего тренда, в 3 путь нисходящего. Оба метода ничего не возвращают.)
'''
timeStart = time.time()
strTickers = 'https://finviz.com/screener.ashx?v=211&ft=3&t='
allCsv = []


def trendDown(df, pathList, i):
    try:
        df['ema8'] = talib.EMA(df['Close'].values, timeperiod=8)  # добавляем столбец с расчитанным SMA
        trendNumber = df[-10:].loc[df.Close < df.ema8]  # берем 10 дней, хаи ниже 20 средней
        if trendNumber.shape[0] >= 3:
            count = 0
            firstIndex = 1
            trendNumber = trendNumber.reset_index(drop=True)  # сброс индексов с 0
            for j in trendNumber.Close[firstIndex:]:
                # ищем последовательность 3 свечей с падающим хай
                if (trendNumber.Close[firstIndex - 1] > j) & (
                        trendNumber.Open[firstIndex - 1] < trendNumber.ema8[firstIndex - 1]) & (
                        trendNumber.Open[firstIndex] < trendNumber.ema8[firstIndex - 1]):
                    count += 1
                else:
                    count = 0
                firstIndex += 1
                if count == 3:
                    copy(pathList[0] + i, pathList[2])
                    break
    except:
        pass


def trendSort(pathlist):
    global allCsv
    # получаем список всех csv
    direct = os.listdir(pathlist[0])
    allCsv = filter(lambda x: x.endswith('.csv'), direct)
    allCsv = list(allCsv)
    for i in allCsv:
        # определеяем тренд
        try:  # обработка NaN
            df = pd.read_csv(pathlist[0] + i)
            trendDown(df, pathlist, i)
            df['ema8'] = talib.EMA(df['Close'].values, timeperiod=8)  # добавляем столбец с расчитанным SMA
            df['ema14'] = talib.EMA(df['Close'].values, timeperiod=14)  # добавляем столбец с расчитанным SMA
            trendNumber = df[-10:].loc[df.ema8 > df.ema14]  # берем 10 дней, 8 средняя выше 14
            if trendNumber.shape[0] >= 5:
                count = 0
                firstIndex = 1
                trendNumber = trendNumber.reset_index(drop=True)  # сброс индексов с 0
                for j in trendNumber.Low[firstIndex:]:
                    # ищем последоватьельность 5 свечей с ростущим лоу
                    if (trendNumber.Low[firstIndex - 1] < j) & (
                            trendNumber.Close[firstIndex - 1] > trendNumber.ema8[firstIndex - 1]) & (
                            trendNumber.Close[firstIndex] > trendNumber.ema8[firstIndex - 1]):
                        count += 1
                    else:
                        count = 0
                    firstIndex += 1
                    if count == 5:
                        copy(pathlist[0] + i, pathlist[1])
                        break
        except:
            pass

# print((time.time() - timeStart)/60, 'minutes.')
