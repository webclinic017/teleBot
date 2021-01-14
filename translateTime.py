import datetime as dt

'''
Принимает строку формата 2:00 PM PDT и возвращает строку - 1 day, 0:00 по Москве, PDT отстает на 10 часов от МСК
Общая команда для Бота имеет формат - Время 2:00 PM PDT
'''
def translateTime(inputString):
    dictZonesInSeconds = {"edt": [25200, "по Москве, EDT отстает на 7 часов от МСК"],
                          "pdt": [36000, "по Москве, PDT отстает на 10 часов от МСК"],
                          "est": [28800, "по Москве, EST отстает на 8 часов от МСК"]}
    listInput = list(inputString.split())
    time = listInput[0].split(":")
    days = 0
    if listInput[1].lower() == "pm":
        time[0] = int(time[0]) + 12
    text = dictZonesInSeconds.get(listInput[2])[1]
    return str(dt.timedelta(days, dictZonesInSeconds.get(listInput[2])[0] + int(time[0]) * 3600 + int(time[1]) * 60))[
           :-3] + " " + text
