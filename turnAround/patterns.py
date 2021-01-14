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
    if (candle1.Green > 0) & (candle1.bodyGreen >= 0.7):
        if list(candle2.PatternRedHighShadow)[0] & (candle2.High > candle1.High) & (
        (candle2.Close >= (candle1.Close - ((candle1.Close - candle1.Open) * 0.15)))) & (
                candle2.Low > (((candle1.High - candle1.Low) / 2) + candle1.Low)) & (
                candle2.Open > candle1.Close):
            if (candle3.Red > 0) & (candle3.Close <= candle1.Open) & (
                    candle3.Open <= (((candle2.Open - candle2.Close) / 2) + candle2.Close)) & (
                    candle3.High < candle2.High):
                return True
    return False


def trendUpGreen(candle1, candle2, candle3):  # восходящий тренд зеленый пин бар
    if (candle1.Green > 0) & (candle1.bodyGreen >= 0.7):
        if list(candle2.PatternGreenHighShadow)[0] & (candle2.High > candle1.High) & (
                candle2.Open >= (candle1.Close - ((candle1.Close - candle1.Open) * 0.15))) & (
                candle2.Close > candle1.Close):
            if (candle3.Red > 0) & (candle3.Open <= (((candle2.Close - candle2.Open) / 2) + candle2.Open)) & (
                    candle3.Close <= candle1.Open) & (candle3.High < candle2.High):
                return True
    return False


def trendDownRed(candle1, candle2, candle3):  # нисходящий тренд красный пин бар
    if (candle1.Red > 0) & (candle1.bodyRed >= 0.7):
        if list(candle2.PatternRedBottomShadow)[0] & (candle2.Close <= candle1.Low) & (candle2.Low < candle1.Low) & (
                candle2.Open >= (candle1.Close - ((candle1.Open - candle1.Close) * 0.15))):
            if (candle3.Green > 0) & (candle3.Close > candle2.High) & (
                    candle3.Open >= (candle2.Close - ((candle2.High - candle2.Low) * 0.15))) & (
                    candle3.Low > candle2.Low):
                return True
    return False


def trendDownGreen(candle1, candle2, candle3):  # нисходящий тренд зеленый пин бар
    if (candle1.Red > 0) & (candle1.bodyRed >= 0.7):
        if list(candle2.PatternGreenBottomShadow)[0] & (
                candle2.High <= (((candle1.High - candle1.Low) / 2) + candle1.Low)) & (
                candle2.Close <= ((candle1.Open - candle1.Close) * 0.15) + candle1.Close) & (
                candle2.Open < candle1.Low) & (candle2.Low < candle1.Low):
            if (candle3.Green > 0) & (candle3.Close > candle2.High) & (
                    candle3.Open >= (candle2.Open - ((candle2.High - candle2.Low) * 0.15))) & (
                    candle3.Low > candle2.Low):
                return True
    return False


def anyPattern(folder):
    ticks = tickers(folder)
    for i in ticks:
        df = pd.read_csv(folder + '/' + i)
        if 'Date' not in df:  # на мелких тф колонка называется Datetime
            df.rename(columns={'Datetime': 'Date'}, inplace=True)
            df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
        c1 = candles.Candle(df[-3:-2])
        c2 = candles.Candle(df[-2:-1])
        c3 = candles.Candle(df[-1:])
        if (trendUpRed(c1, c2, c3) | trendUpGreen(c1, c2, c3) | trendDownRed(c1, c2, c3) | trendDownGreen(c1, c2, c3)):
            print(str(i)[:-4])
            df['signal'] = np.nan
            df.signal[-2:-1] = float(df.High[-2:-1]) * 1.01  # отметка свечи
            addPlot.mplot(df, df.signal, str(i)[:-4], folder)


#folder1 = '/home/linac/Рабочий стол/data/20210113_60d1d/'
#anyPattern(folder1)
