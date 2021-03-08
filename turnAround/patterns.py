import pandas as pd
import talib
import numpy as np
import os
import turnAround.addPlot as addPlot
import turnAround.candles as candles

pd.options.mode.chained_assignment = None  # отключение уведомлений


def tickers(folder):
    return list(filter(lambda x: x.endswith('.csv'), os.listdir(folder)))


df = ''
folder = ''
tick = ''


def trendUpRed(candle0, candle1, candle2, candle3):  # восходящий тренд красный пин бар
    if str(folder).__contains__('up'):
        if (candle1.Green > 0) & (candle1.bodyGreen >= 0.65):
            if (candle2.PatternRedHighShadow | candle2.PatternRedEqShadows) & (candle2.High > candle1.High) & (
                    (candle2.Close >= (candle1.Close - ((candle1.Close - candle1.Open) * 0.3)))) & (
                    candle2.Low > (((candle1.High - candle1.Low) / 2) + candle1.Low)) & (
                    candle2.Open > candle1.Close):
                if (candle3.Red > 0) & (candle3.Close <= candle1.Open) & (
                        candle3.Open <= (((candle2.Open - candle2.Close) / 2) + candle2.Close)) & (
                        candle3.High < candle2.High):
                    return True
    return False


def trendUpGreen(candle0, candle1, candle2, candle3):  # восходящий тренд зеленый пин бар
    if str(folder).__contains__('up'):
        if (candle1.Green > 0) & (candle1.bodyGreen >= 0.65):
            if (candle2.PatternGreenHighShadow | candle2.PatternGreenEqShadows) & (candle2.High > candle1.High) & (
                    candle2.Open >= (candle1.Close - ((candle1.Close - candle1.Open) * 0.3))) & (
                    candle2.Close > candle1.Close):
                if (candle3.Red > 0) & (candle3.Open <= (((candle2.Close - candle2.Open) / 2) + candle2.Open)) & (
                        candle3.Close <= candle1.Open) & (candle3.High < candle2.High):
                    return True
    return False


def trendDownRed(candle0, candle1, candle2, candle3):  # нисходящий тренд красный пин бар
    if str(folder).__contains__('down'):
        if (candle1.Red > 0) & (candle1.bodyRed >= 0.65):
            if (candle2.PatternRedBottomShadow | candle2.PatternRedEqShadows) & (candle2.Close <= candle1.Low) & (
                    candle2.Low < candle1.Low) & (
                    candle2.Open >= (candle1.Close - ((candle1.Open - candle1.Close) * 0.3))):
                if (candle3.Green > 0) & (candle3.Close > candle2.High) & (
                        candle3.Open >= (candle2.Close - ((candle2.High - candle2.Low) * 0.15))) & (
                        candle3.Low > candle2.Low):
                    return True
    return False


def trendDownGreen(candle0, candle1, candle2, candle3):  # нисходящий тренд зеленый пин бар
    if str(folder).__contains__('down'):
        if (candle1.Red > 0) & (candle1.bodyRed >= 0.65):
            if (candle2.PatternGreenBottomShadow | candle2.PatternGreenEqShadows) & (
                    candle2.High <= (((candle1.High - candle1.Low) * 0.66) + candle1.Low)) & (
                    candle2.Close <= ((candle1.Open - candle1.Close) * 0.30) + candle1.Close) & (
                    candle2.Open <= candle1.Low) & (candle2.Low < candle1.Low):
                if (candle3.Green > 0) & (candle3.Close > candle2.High) & (
                        candle3.Open >= (candle2.Open - ((candle2.High - candle2.Low) * 0.15))) & (
                        candle3.Low > candle2.Low):
                    return True
    return False


def trendUpInnerFirst(candle0, candle1, candle2, candle3):  # trendFirst innerFirst(green)
    if str(folder).__contains__('up'):
        if (candle1.Green > 0) & (candle1.bodyGreen >= 0.75):
            if ((candle2.Red > 0) & (candle2.bodyRed >= 0.55)) & (
                    (candle2.Close >= candle1.Open) & (candle2.Open <= candle1.Close) & (candle2.High <= candle1.High)):
                if ((candle3.Green > 0) & (candle3.Close < (((candle2.Open - candle2.Close) * 0.53) + candle2.Close))):
                    return True
                if ((candle3.Red > 0) & (candle3.Open <= (((candle2.Open - candle2.Close) * 0.53) + candle2.Close))):
                    return True
    return False


def trendUpInnerSecond(candle0, candle1, candle2, candle3):  # trendUp innerSecond(red)
    if str(folder).__contains__('up'):
        if ((candle1.Green > 0) & (candle1.bodyGreen >= 0.75)) & (
                (candle1.Close <= candle2.Open) & (candle1.Open >= candle2.Close)):
            if (candle2.Red > 0) & (candle2.bodyRed >= 0.75):
                if ((candle3.Green > 0) & (candle3.Close < (((candle2.Open - candle2.Close) * 0.53) + candle2.Close))):
                    return True
                if ((candle3.Red > 0) & (candle3.Open <= (((candle2.Open - candle2.Close) * 0.53) + candle2.Close))):
                    return True
    return False


def trendDownInnerSecond(candle0, candle1, candle2, candle3):  # trendDown innerSecond(green)
    if str(folder).__contains__('down'):
        if ((candle1.Red > 0) & (candle1.bodyRed >= 0.75)):
            if ((candle2.Green > 0) & (candle2.bodyGreen >= 0.55) & (candle2.Open >= candle1.Close) & (
                    candle2.Low >= candle1.Low) & (
                    candle2.Close > (((candle1.Open - candle1.Close) / 2) + candle1.Close)) & (
                    candle2.Close <= candle1.Open)):
                if ((candle3.Green > 0) & (candle3.Close > candle2.Close) & (
                        candle3.Low >= (((candle2.Close - candle2.Open) * 0.49) + candle2.Open))):
                    return True
    return False


def trendDownInnerFirst(candle0, candle1, candle2, candle3):  # trendDown innerFirst(red)
    if str(folder).__contains__('down'):
        if ((candle1.Red > 0) & (candle1.bodyRed >= 0.75)):
            if ((candle2.Green > 0) & (candle2.bodyGreen >= 0.75) & (candle2.Close >= candle1.Open) & (
                    candle2.Open <= candle1.Close) & (candle2.Low <= candle1.Low) & (candle2.High >= candle1.High)):
                if ((candle3.Green > 0) & (candle3.Close > candle2.Close) & (
                        candle3.Low >= (((candle2.Close - candle2.Open) * 0.49) + candle2.Open))):
                    return True
    return False


def ricochet(candle0, candle1, candle2, candle3):
    global folder
    if str(folder).__contains__('up'):
        if ((candle0.Green > 0) & (candle0.bodyGreen >= 0.8)):
            if ((candle1.Green > 0) & (candle1.bodyGreen >= 0.8) & (candle1.Open >= candle0.Open)):
                if ((candle2.Green > 0) & (candle2.bodyGreen >= 0.5) & (candle2.Open >= candle1.Open) & (
                        candle2.highShadowGreen > candle2.bottomShadowGreen)) | (
                        (candle2.Red > 0) & (candle2.bodyRed >= 0.5) & (candle2.Close >= candle1.Open) & (
                        candle2.highShadowRed > candle2.bottomShadowRed)):
                    if ((candle2.High < candle3.Low) & (candle3.Red > 0) & (candle3.bodyRed >= 0.8) & (
                            candle3.Close <= candle1.Open)):
                        return True
    if str(folder).__contains__('down'):
        if ((candle0.Red > 0) & (candle0.bodyRed >= 0.8)):
            if ((candle1.Red > 0) & (candle1.bodyRed >= 0.8) & (candle1.Low < candle0.Low)):
                if ((candle2.Red > 0) & (candle2.bodyRed >= 0.5) & (candle2.Low < candle1.Low) & (
                        candle2.highShadowRed < candle2.bottomShadowRed)) | (
                        (candle2.Green > 0) & (candle2.bodyGreen >= 0.5) & (candle2.Low < candle1.Low) & (
                        candle2.highShadowGreen < candle2.bottomShadowGreen)):
                    if ((candle2.High < candle3.Low) & (candle3.Green > 0) & (candle3.bodyGreen >= 0.8) & (
                            candle3.Close >= candle1.Open)):
                        return True
    return False


def haramiUp(candle0, candle1, candle2, candle3):
    if str(folder).__contains__('up'):  # trend up
        if ((candle0.Green > 0) & (candle0.bodyGreen >= 0.65)):
            c1G = (candle1.Green > 0) & (candle1.bodyGreen >= 0.65) & (candle1.High <= candle0.Close) & (
                    candle1.Low >= candle0.Open) & (candle1.highShadowGreen >= candle1.bottomShadowGreen) & (
                          candle1.Close <= (candle0.Close - ((candle0.Close - candle0.Open) * 0.25))) & (
                          candle1.Open >= (candle0.Open + ((candle0.Close - candle0.Open) * 0.25)))
            c1R = (candle1.Red > 0) & (candle1.bodyRed >= 0.65) & (candle1.High <= candle0.Close) & (
                    candle1.Low >= candle0.Open) & (candle1.highShadowRed >= candle1.bottomShadowRed) & (
                          candle1.Open <= (candle0.Close - ((candle0.Close - candle0.Open) * 0.25))) & (
                          candle1.Close >= (candle0.Open + ((candle0.Close - candle0.Open) * 0.25)))
            if (c1G | c1R):
                c2R = (candle2.Red > 0) & (candle2.High < candle0.High) & (candle2.Low > candle0.Low) & (
                        candle2.PatternRedEqShadows | candle2.PatternRedDoje | candle2.PatternRedHighShadow | candle2.PatternRedBottomShadow)
                c2G = (candle2.Green > 0) & (candle2.High < candle0.High) & (candle2.Low > candle0.Low) & (
                        candle2.PatternGreenEqShadows | candle2.PatternGreenDoje | candle2.PatternGreenHighShadow | candle2.PatternGreenBottomShadow)
                if not (c2R | c2G):
                    candle3 = candle2
                if ((candle3.Red > 0) & (candle3.Close < candle0.Open)):
                    return True
    return False


def haramiDown(c0, c1, c2, c3):
    if str(folder).__contains__('down'):  # trend down
        if ((c0.Red > 0) & (c0.bodyRed >= 0.65)):
            c1G = (c1.Green > 0) & (c1.bodyGreen >= 0.65) & (c1.High <= c0.Open) & (c1.Low >= c0.Close) & (
                        c1.highShadowGreen <= c1.bottomShadowGreen) & (
                              c1.Close <= (c0.Open - ((c0.Open - c0.Close) * 0.25))) & (
                              c1.Open >= (c0.Close + ((c0.Open - c0.Close) * 0.25)))
            c1R = (c1.Red > 0) & (c1.bodyRed >= 0.65) & (c1.High <= c0.Open) & (c1.Low >= c0.Close) & (
                        c1.highShadowRed <= c1.bottomShadowRed) & (
                              c1.Open <= (c0.Open - ((c0.Open - c0.Close) * 0.25))) & (
                              c1.Close >= (c0.Close + ((c0.Open - c0.Close) * 0.25)))
            if (c1G | c1R):
                c2R = (c2.Red > 0) & (c2.High < c0.High) & (c2.Low > c0.Low) & (
                        c2.PatternRedEqShadows | c2.PatternRedDoje | c2.PatternRedHighShadow | c2.PatternRedBottomShadow)
                c2G = (c2.Green > 0) & (c2.High < c0.High) & (c2.Low > c0.Low) & (
                        c2.PatternGreenEqShadows | c2.PatternGreenDoje | c2.PatternGreenHighShadow | c2.PatternGreenBottomShadow)
                if not (c2R | c2G):
                    c3 = c2
                if ((c3.Green > 0) & (c3.Close > c0.Open)):
                    return True
    return False


def raiseUp(c0, c1, c2, c3):
    if str(folder).__contains__('up'):  # trend up
        if ((c1.Green > 0) & (c1.bodyGreen >= 0.6) & (c1.highShadowGreen >= c1.bottomShadowGreen)):
            print(1,tick)
            if ((c2.Red > 0) & (c2.bodyRed >= 0.6) & (
                    c2.Open < (c1.Close - ((c1.Close - c1.Open) * 0.16))) & (
                    c2.Close < (c1.Close - ((c1.Close - c1.Open) * 0.16)))):
                print(2)
                if ((c3.Red > 0) & (c3.bodyRed >= 0.65) & (c3.Close < c2.Low) & (c3.Open <= c1.Open)):
                    return True
    return False


def raiseDown(c0, c1, c2, c3):
    if str(folder).__contains__('down'):  # trend down
        if ((c1.Red > 0) & (c1.bodyRed >= 0.75) & (c1.bottomShadowRed >= c1.highShadowRed)):
            if ((c2.Green > 0) & (c2.bodyGreen >= 0.65) & (
                    c2.Open > (c1.Close + ((c1.Open - c1.Close) * 0.16))) & (
                    c2.Close > (c1.Open + ((c1.Open - c1.Close) * 0.16)))):
                if ((c3.Green > 0) & (c3.bodyGreen >= 0.65) & (c3.Close > c2.High) & (c3.Open >= c1.Open)):
                    return True
    return False


def halfCandleInner(candle0, candle1, candle2, candle3):  # half
    global df
    global folder
    try:
        v = int(df.loc[:60].Volume.mean() * 2)
        midV = int(df.loc[:60].Volume.mean() * 2)
        candle8 = candles.Candle(df[-8:-7])
        candle7 = candles.Candle(df[-7:-6])
        candle6 = candles.Candle(df[-6:-5])
        candle5 = candles.Candle(df[-5:-4])
    except:
        return False
    if (((candle0.Red > 0) & (candle0.bodyRed <= 0.5)) & (candle0.highShadowRed > candle0.bottomShadowRed)) | (
            ((candle0.Green > 0) & (candle0.bodyGreen <= 0.5)) & (candle0.highShadowGreen > candle0.bottomShadowGreen)):
        if (candle0.Volume >= v) & (candle5.Volume <= midV) & (candle6.Volume <= midV) & (candle7.Volume <= midV) & (
                candle8.Volume <= midV):
            if str(folder).__contains__('up'):
                print('Up')
                pointX = candle0.Low + ((candle0.High - candle0.Low) * 0.6)
                c1 = ((candle1.Red > 0) & (candle1.Open <= pointX)) | ((candle1.Green > 0) & (candle1.Close <= pointX))
                c2 = ((candle2.Red > 0) & (candle2.Open <= pointX)) | ((candle2.Green > 0) & (candle2.Close <= pointX))
                c3 = ((candle3.Red > 0) & (candle3.Open <= pointX)) | ((candle3.Green > 0) & (candle3.Close <= pointX))
                if (c1 & c2 & c3) & (candle1.Low >= candle0.Low) & (candle2.Low >= candle0.Low) & (
                        candle3.Low >= candle0.Low):
                    return True
            if str(folder).__contains__('down'):
                print('down')
                pointX = candle0.High - ((candle0.High - candle0.Low) * 0.6)
                c1H = ((candle1.Red > 0) & (candle1.Open <= candle0.High)) | (
                        (candle1.Green > 0) & (candle1.Close <= candle0.High))
                c2H = ((candle2.Red > 0) & (candle2.Open <= candle0.High)) | (
                        (candle2.Green > 0) & (candle2.Close <= candle0.High))
                c3H = ((candle3.Red > 0) & (candle3.Open <= candle0.High)) | (
                        (candle3.Green > 0) & (candle3.Close <= candle0.High))
                if (c1H & c2H & c3H) & (candle1.Low >= candle0.Low) & (candle2.Low >= candle0.Low) & (
                        candle3.Low >= candle0.Low):
                    c1L = ((candle1.Red > 0) & (candle1.Close >= pointX)) | (
                            (candle1.Green > 0) & (candle1.Open >= pointX))
                    c2L = ((candle2.Red > 0) & (candle2.Close >= pointX)) | (
                            (candle2.Green > 0) & (candle2.Open >= pointX))
                    c3L = ((candle3.Red > 0) & (candle3.Close >= pointX)) | (
                            (candle3.Green > 0) & (candle3.Open >= pointX))
                    if (c1L & c2L & c3L):
                        return True
    return False


def highVolumePattern(candle0, candle1, candle2, candle3):
    # метод ищет высокий объем среди последних 10 свечей (свеча X), предыдущие 3 свечи должны иметь объем меньше чем 60%X объема
    # следующие 3 свечи после Х имеют снижение в объеме относительно предыдущей свечи
    v = []
    global df
    a = int(df.loc[:].Volume.mean() * 4)
    dfV = df.tail(10)  # берем строки с конца
    dfV.insert(0, 'Ind', range(0, len(dfV)))  # добавляем колнонку с цифровым индексом
    v = dfV.Ind[dfV.Volume > a].tolist()
    count = 0
    flag = False
    # print(dfV)
    for i in v:
        if 3 <= i <= 5:
            for j in range(i - 3, i):
                if int(dfV.loc[dfV.Ind == j].Volume) < int((dfV.loc[dfV.Ind == i].Volume * 0.60)):
                    count += 1
            # следующие 3 свечи по Х снижение объема
            if int(dfV.loc[dfV.Ind == i + 1].Volume) < int((dfV.loc[dfV.Ind == i].Volume * 0.95)):
                if int(dfV.loc[dfV.Ind == i + 2].Volume) < int((dfV.loc[dfV.Ind == i + 1].Volume * 0.95)):
                    if int(dfV.loc[dfV.Ind == i + 3].Volume) < int((dfV.loc[dfV.Ind == i + 2].Volume * 0.95)):
                        flag = True
            if (count == 3) & flag:
                return True
    return False


def anyPattern(folder1, folderName, patternName):
    global df
    global folder
    global tick
    folder = folder1
    patterns = [patternName]
    ticks = tickers(folder)
    funcs = {'Разворот': [trendUpRed, trendUpGreen, trendDownRed, trendDownGreen],
             'Вложенные': [trendUpInnerFirst, trendUpInnerSecond, trendDownInnerSecond, trendDownInnerFirst],
             'Рикошет': [ricochet],
             'Пистолет': [halfCandleInner],
             'Харами': [haramiUp, haramiDown],
             'Усиление': [raiseUp, raiseDown]}

    for i in ticks:
        tick = i
        df = pd.read_csv(folder + '/' + i)
        if 'Date' not in df:  # на мелких тф колонка называется Datetime
            df.rename(columns={'Datetime': 'Date'}, inplace=True)
            df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
        try:
            c0 = candles.Candle(df[-4:-3])
            c1 = candles.Candle(df[-3:-2])
            c2 = candles.Candle(df[-2:-1])
            c3 = candles.Candle(df[-1:])
        except ZeroDivisionError:
            continue

        if patternName == 'Все':  # получаем список всех паттернов и проходим их в цикле далее
            patterns = funcs.keys()
        for pattern in patterns:
            patternName = pattern
            for j in funcs.get(patternName):
                if j(c0, c1, c2, c3):
                    print(str(i)[:-4])
                    df['signal'] = np.nan
                    df.signal[-2:-1] = float(df.High[-2:-1]) * 1.01  # отметка свечи
                    addPlot.mplot(df, df.signal, str(i)[:-4], folder, folderName, patternName)
name = 'Усиление'
patternName = 'Усиление'
folder1 = '/home/linac/Рабочий стол/data/test/up/'
anyPattern(folder1, 'test', patternName)
