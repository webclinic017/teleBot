import pandas as pd
import numpy as np
import re


class Candle():
    def __init__(self, df1):
        df = df1
        self.Low = float(df.Low)
        self.Open = float(df.Open)
        self.High = float(df.High)
        self.Close = float(df.Close)
        self.Volume = float(df.Volume)
        self.Date = str(df.Date.values[0])
        self.Green = float(df.Close - df.Open)
        self.Red = float(df.Open - df.Close)
        self.bottomShadowGreen = float((df.Open - df.Low))# / (df.High - df.Low))
        self.bottomShadowRed = float((df.Close - df.Low))# / (df.High - df.Low))
        self.highShadowGreen = float((df.High - df.Close))# / (df.High - df.Low))
        self.highShadowRed = float((df.High - df.Open))# / (df.High - df.Low))
        self.size = float(df.High - df.Low)
        self.bodyGreen = float((df.Close - df.Open) / (df.High - df.Low))
        self.bodyRed = float((df.Open - df.Close) / (df.High - df.Low))
        self.PatternGreenBottomShadow = (self.Green > 0) & ((self.bottomShadowGreen / self.size) >= 0.45) & ((self.Green / self.size) >= 0.2)  # & (df.Volume >= int(df.loc[:60].Volume.mean()) * 1.5)
        self.PatternRedBottomShadow = (self.Red > 0) & ((self.bottomShadowRed / self.size) >= 0.45) & ((self.Red / self.size) >= 0.2)  # & (df.Volume >= int(df.loc[:60].Volume.mean()) * 1.5)
        self.PatternGreenHighShadow = (self.Green > 0) & ((self.highShadowGreen / self.size) >= 0.45) & ((self.Green / self.size) >= 0.2)  # & (df.Volume >= int(df.loc[:60].Volume.mean()) * 1.5)
        self.PatternRedHighShadow = (self.Red > 0) & ((self.highShadowRed / self.size) >= 0.45) & ((self.Red / self.size) >= 0.2)  # & (df.Volume >= int(df.loc[:60].Volume.mean()) * 1.5)
        self.PatternRedEqShadows = (((self.highShadowRed - self.bottomShadowRed) > 0) & ((self.highShadowRed - self.bottomShadowRed) <= (self.size * 0.065))) | (((self.bottomShadowRed - self.highShadowRed) > 0) & ((self.bottomShadowRed - self.highShadowRed) <= (self.size * 0.065))) & ((self.bodyRed > 0.45) & (self.bodyRed < 0.55))
        self.PatternGreenEqShadows = (((self.highShadowGreen - self.bottomShadowGreen) > 0) & ((self.highShadowGreen - self.bottomShadowGreen) <= (self.size * 0.065))) | (((self.bottomShadowGreen - self.highShadowGreen) > 0) & ((self.bottomShadowGreen - self.highShadowGreen) <= (self.size * 0.065))) & ((self.bodyGreen > 0.45) & (self.bodyGreen < 0.55))