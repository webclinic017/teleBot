import pandas as pd
import numpy as np


class Candle():
    def __init__(self, df1):
        df = df1
        self.Low = float(df.Low)
        self.Open = float(df.Open)
        self.High = float(df.High)
        self.Close = float(df.Close)
        self.Volume = float(df.Volume)
        self.Date = df.Date
        self.Green = float(df.Close - df.Open)
        self.Red = float(df.Open - df.Close)
        self.bottomShadowGreen = (df.Open - df.Low) / (df.High - df.Low)
        self.bottomShadowRed = (df.Close - df.Low) / (df.High - df.Low)
        self.highShadowGreen = float((df.High - df.Close) / (df.High - df.Low))
        self.highShadowRed = (df.High - df.Open) / (df.High - df.Low)
        self.bodyGreen = float((df.Close - df.Open) / (df.High - df.Low))
        self.bodyRed = float((df.Open - df.Close) / (df.High - df.Low))
        self.PatternGreenBottomShadow = ((df.Close - df.Open) > 0) & (
                    (df.Open - df.Low) / (df.High - df.Low) >= 0.45) & ((df.Close - df.Open) / (
                    df.High - df.Low) >= 0.2)  # & (df.Volume >= int(df.loc[:60].Volume.mean()) * 1.5)
        self.PatternRedBottomShadow = ((df.Open - df.Close) > 0) & (
                    (df.Close - df.Low) / (df.High - df.Low) >= 0.45) & ((df.Open - df.Close) / (
                    df.High - df.Low) >= 0.2)  # & (df.Volume >= int(df.loc[:60].Volume.mean()) * 1.5)
        self.PatternGreenHighShadow = ((df.Close - df.Open) > 0) & (
                    (df.High - df.Close) / (df.High - df.Low) >= 0.45) & ((df.Close - df.Open) / (
                    df.High - df.Low) >= 0.2)  # & (df.Volume >= int(df.loc[:60].Volume.mean()) * 1.5)
        self.PatternRedHighShadow = ((df.Open - df.Close) > 0) & ((df.High - df.Open) / (df.High - df.Low) >= 0.45) & (
                    (df.Open - df.Close) / (
                        df.High - df.Low) >= 0.2)  # & (df.Volume >= int(df.loc[:60].Volume.mean()) * 1.5)
