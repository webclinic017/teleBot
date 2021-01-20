import csv
import os
import yfinance as yf
import pandas as pd
from datetime import datetime

'''
Метод download получает на вход период и интервал, по которым скачивает данные. Данные параметры используются также
в имени каталога, куда скачиваются данные. Создает каталог для скачивания и еще два каталога для будущей сортировки.
Возвращает лист из 3 путей и имя каталога folderName для его отоборажения на графике.
'''

def download(period1, interval1):
    folderName = str(datetime.date(datetime.now())).replace('-', '') + '_' + str(period1) + str(interval1)
    path = '/home/linac/Рабочий стол/data/' + folderName + '/'
    pathUp = '/home/linac/Рабочий стол/data/' + folderName + '/up/'
    pathDown = '/home/linac/Рабочий стол/data/' + folderName + '/down/'
    try:
        os.mkdir(path)
        os.mkdir(pathUp)
        os.mkdir(pathDown)
    except FileExistsError:
        pass

    ticker_list = []
    with open('/home/linac/Рабочий стол/data/tickers/tickers.csv', 'r') as str0:
        for i in str0.read().split(" "):
            ticker_list.append(i)
    str0.close()
    for i in range(0, int(len(ticker_list) / 100)):
        data = yf.download(
            tickers=ticker_list[i * 100:(i * 100) + 100],
            period=str(period1),  # 60d
            interval=str(interval1),  # 1h
            group_by='ticker',
            auto_adjust=True,
            prepost=False,
            threads=True
        )
        data = data.T
        for ticker in ticker_list[i * 100:(i * 100) + 100]:
            with open('/home/linac/Рабочий стол/data/' + folderName + '/' + ticker + '.csv', 'w') as f:  # в файл
                f.write(data.loc[ticker].T.to_csv(sep=','))
            f.close()
    return [path, pathUp, pathDown, folderName]