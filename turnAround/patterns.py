import pandas as pd
import talib
import numpy as np
import os
import turnAround.addPlot as addPlot
import turnAround.candles as candles

pd.options.mode.chained_assignment = None  # отключение уведомлений


def tickers(folder):
    return list(filter(lambda x: x.endswith('.csv'), os.listdir(folder)))


def trendUpRed(candle1, candle2, candle3):  # восходящий тренд красный пин бар
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


def trendUpGreen(candle1, candle2, candle3):  # восходящий тренд зеленый пин бар
    if (candle1.Green > 0) & (candle1.bodyGreen >= 0.65):
        if (candle2.PatternGreenHighShadow | candle2.PatternGreenEqShadows) & (candle2.High > candle1.High) & (
                candle2.Open >= (candle1.Close - ((candle1.Close - candle1.Open) * 0.3))) & (
                candle2.Close > candle1.Close):
            if (candle3.Red > 0) & (candle3.Open <= (((candle2.Close - candle2.Open) / 2) + candle2.Open)) & (
                    candle3.Close <= candle1.Open) & (candle3.High < candle2.High):
                return True
    return False


def trendDownRed(candle1, candle2, candle3):  # нисходящий тренд красный пин бар
    if (candle1.Red > 0) & (candle1.bodyRed >= 0.65):
        if (candle2.PatternRedBottomShadow | candle2.PatternRedEqShadows) & (candle2.Close <= candle1.Low) & (
                candle2.Low < candle1.Low) & (
                candle2.Open >= (candle1.Close - ((candle1.Open - candle1.Close) * 0.3))):
            if (candle3.Green > 0) & (candle3.Close > candle2.High) & (
                    candle3.Open >= (candle2.Close - ((candle2.High - candle2.Low) * 0.15))) & (
                    candle3.Low > candle2.Low):
                return True
    return False


def trendDownGreen(candle1, candle2, candle3):  # нисходящий тренд зеленый пин бар
    if (candle1.Red > 0) & (candle1.bodyRed >= 0.65):
        if (candle2.PatternGreenBottomShadow | candle2.PatternGreenEqShadows) & (
                candle2.High <= (((candle1.High - candle1.Low) / 2) + candle1.Low)) & (
                candle2.Close <= ((candle1.Open - candle1.Close) * 0.30) + candle1.Close) & (
                candle2.Open <= candle1.Low) & (candle2.Low < candle1.Low):
            if (candle3.Green > 0) & (candle3.Close > candle2.High) & (
                    candle3.Open >= (candle2.Open - ((candle2.High - candle2.Low) * 0.15))) & (
                    candle3.Low > candle2.Low):
                return True
    return False


def trendUpInnerFirst(candle1, candle2, candle3):  # trendFirst innerFirst(green)
    if (candle1.Green > 0) & (candle1.bodyGreen >= 0.75):
        if ((candle2.Red > 0) & (candle2.bodyRed >= 0.55)) & (
                (candle2.Close >= candle1.Open) & (candle2.Open <= candle1.Close) & (candle2.High <= candle1.High)):
            if ((candle3.Green > 0) & (candle3.Close < (((candle2.Open - candle2.Close) * 0.53) + candle2.Close))):
                return True
            if ((candle3.Red > 0) & (candle3.Open <= (((candle2.Open - candle2.Close) * 0.53) + candle2.Close))):
                print(1)
                return True
    return False


def trendUpInnerSecond(candle1, candle2, candle3):  # trendUp innerSecond(red)
    if ((candle1.Green > 0) & (candle1.bodyGreen >= 0.75)) & (
            (candle1.Close <= candle2.Open) & (candle1.Open >= candle2.Close)):
        if (candle2.Red > 0) & (candle2.bodyRed >= 0.75):
            if ((candle3.Green > 0) & (candle3.Close < (((candle2.Open - candle2.Close) * 0.53) + candle2.Close))):
                return True
            if ((candle3.Red > 0) & (candle3.Open <= (((candle2.Open - candle2.Close) * 0.53) + candle2.Close))):
                print(2)
                return True
    return False


def trendDownInnerSecond(candle1, candle2, candle3):  # trendDown innerSecond(green)
    if ((candle1.Red > 0) & (candle1.bodyRed >= 0.75)):
        if ((candle2.Green > 0) & (candle2.bodyGreen >= 0.55) & (candle2.Open >= candle1.Close) & (
                candle2.Low >= candle1.Low) & (
                candle2.Close > (((candle1.Open - candle1.Close) / 2) + candle1.Close)) & (
                candle2.Close <= candle1.Open)):
            if ((candle3.Green > 0) & (candle3.Close > candle2.Close) & (
                    candle3.Low >= (((candle2.Close - candle2.Open) * 0.49) + candle2.Open))):
                print(3)
                return True
    return False


def trendDownInnerFirst(candle1, candle2, candle3):  # trendDown innerFirst(red)
    if ((candle1.Red > 0) & (candle1.bodyRed >= 0.75)):
        if ((candle2.Green > 0) & (candle2.bodyGreen >= 0.75) & (candle2.Close >= candle1.Open) & (
                candle2.Open <= candle1.Close) & (candle2.Low <= candle1.Low) & (candle2.High >= candle1.High)):
            if ((candle3.Green > 0) & (candle3.Close > candle2.Close) & (
                    candle3.Low >= (((candle2.Close - candle2.Open) * 0.49) + candle2.Open))):
                print(4)
                return True
    return False


def anyPattern(folder, folderName, patternName):
    ticks = tickers(folder)
    funcs = {'Разворот': [trendUpRed, trendUpGreen, trendDownRed, trendDownGreen],
             'ВложенныеUp': [trendUpInnerFirst, trendUpInnerSecond],
             'ВложенныеDown':[trendDownInnerSecond, trendDownInnerFirst]}
    for i in ticks:
        df = pd.read_csv(folder + '/' + i)
        if 'Date' not in df:  # на мелких тф колонка называется Datetime
            df.rename(columns={'Datetime': 'Date'}, inplace=True)
            df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
        try:
            c1 = candles.Candle(df[-3:-2])
            c2 = candles.Candle(df[-2:-1])
            c3 = candles.Candle(df[-1:])
            #c4 = candles.Candle(df[1])
        except ZeroDivisionError:
            continue
        if (patternName == 'Вложенные') & (folder.__contains__('up')):
            patternName = patternName + 'Up'
        if (patternName == 'Вложенные') & (folder.__contains__('down')):
            patternName = patternName + 'Down'
        for j in funcs.get(patternName):
            if j(c1, c2, c3):
                print(str(i)[:-4])
                df['signal'] = np.nan


                trendUp = []
                for t in range (0, df.shape[0]-6):
                    try:
                        c4 = candles.Candle(df[t+1 : t+2])
                        c5 = candles.Candle(df[t+2 : t+3])
                        c6 = candles.Candle(df[t+3 : t+4])
                        c7 = candles.Candle(df[t+5 : t+6])
                    except ZeroDivisionError:
                        continue
                    if (c4.High < c5.High < c6.High) & (c6.High > c7.High):
                        trendUp.append((c6.Date,c6.High))

                #print(trendUp)
                #print(df.head())
                df['trendUp'] = np.nan



                df.signal[-2:-1] = float(df.High[-2:-1]) * 1.01  # отметка свечи
                addPlot.mplot(df, df.signal, str(i)[:-4], folder, folderName, patternName, trendUp)

#name = 'test'
#patternName = 'Разворот'
#folder1 = '/home/linac/Рабочий стол/data/test'
#anyPattern(folder1, 'test', patternName)
