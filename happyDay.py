import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

'''
happyDay - расчитывает вероятность закрытиия какой либо бумаги в плюсе в конкретный день. 
Метод calcDay принимает на вход строку ticker(например SPY) и day(день в формате строки, 
например '11-27' что является 27 ноября)
Метод возвращает строку ответ.
Общая команда для Бота имеет формат - День spy 11-27
'''


def calcDay(ticker, day):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&apikey=WLFNX0UVYNZDJ0E0&datatype=csv&outputsize=full'  # адрес запроса для получения данныхr = requests.get(url) #сделаем запрос к Alpha Vantage
    r = requests.get(url)  # сделаем запрос к Alpha Vantage
    content = r.content.decode('UTF-8')
    with open('/home/linac/Рабочий стол/data/happyDay/' + str(ticker) + '.csv', 'w') as f:  # запись в файл
        f.write(content)
    df = pd.read_csv('/home/linac/Рабочий стол/data/happyDay/' + str(ticker) + '.csv', parse_dates=True)  # прочитаем файл
    f.close()

    try:
        # основная формула здесь, в первой строке фильтруем, во второй расчет, здесь можно проверить любую дату
        stat1 = df.loc[(df["timestamp"].str.contains(day))]
        return 'Статистическая вероятность роста ' + ticker + ' в этот день ' + day + ': ' + str(
            int(stat1.query('close>open').shape[0] / stat1.shape[0] * 100)) + '%'
    except:
        return "Ошибка расчета дня"


'''
# эта часть для графика и отдельного фрейма
stat2 = df.loc[(df["timestamp"].str.contains('2019'))]  #выбираем год
stat2['happy_day'] = 0 # добавляем новую колонку

pd.options.mode.chained_assignment = None # далее в цикле будет предупреждение, этой строкой оно отключается
for i in stat2.index:
    myStat = df.loc[(df["timestamp"].str.contains(stat2.timestamp[i][4:]))]
    # myStat = myStat.reset_index(drop=True) #сброс индексов с 0
    stat2['happy_day'][i] = myStat.query('close>open').shape[0] / \
                            df.loc[(df["timestamp"].str.contains(myStat.timestamp[i][4:]))].shape[0] * 100

# stat1 = df.query('timestamp.str.contains("11-27")')
# int(stat1.query('close>open').shape[0]/stat1.shape[0]*100)
# в цикле объединена формула в одну строку, вместо stat1 - myStat

stat4 = stat2[['timestamp','happy_day']] #новый фрейм из двух колонок
stat4 = stat4.iloc[::-1] # реверс дата фрейма
stat4 = stat4.reset_index(drop=True) #сброс индексов с 0
stat4.index = stat4.timestamp #назначаем индекс как дату
stat4.drop(columns=['timestamp']) #убираем теперь уже не нужную колонку
print(stat4)
'''
