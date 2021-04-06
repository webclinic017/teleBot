from turnAround.patterns import anyPattern


class Point():
    def __init__(self, df1):
        df = df1
        self.maxi = (df.Maximum > 0)
        self.mini = (df.Minimum > 0)
        self.maxiP = float(df.Maximum)
        self.miniP = float(df.Minimum)
        self.High = float(df.High)
        self.Low = float(df.Low)


#name = 'Все'
#patternName = 'Все'
#folder1 = '/home/linac/Рабочий стол/data/20210406_60d1d'
#anyPattern(folder1, 'test', patternName)