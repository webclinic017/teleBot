import configBot as configBot
import translateTime as myTime
import happyDay as happyDay
from turnAround.manager import startTurnaroundPattern as tz2
import telebot
import os
import re
import time
from keyboa import keyboa_maker

bot = telebot.TeleBot(configBot.token)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    turnarounds = [['День', 'Час'], ['30', '15', '5'],['Все']]

    if re.search(r"=[в|В]ремя\s", message.text):
        t = str(re.search(r"\d{1,}:\d\d\s\w\w\s\w\w\w", str(message.text)).string)
        bot.send_message(message.chat.id, myTime.translateTime(re.sub(r"=[в|В]ремя\s", "", t)))
    elif re.search(r"=[д|Д]ень\s", message.text):
        bot.send_message(message.chat.id, "Я получил запрос расчета дня, анализирую: " + message.text)
        ticker = re.search(r"[a-zA-Z]+", str(message.text)).group(0)
        date = str(re.search(r"\d+-\d+", str(message.text)).group(0))
        answer = happyDay.calcDay(ticker,date)
        bot.send_message(message.chat.id, answer)
    elif re.search(r"=[р|Р]азворот", message.text):
        #kb_turnaround = keyboa_maker(items=turnarounds, copy_text_to_callback=True, front_marker='&time=',back_marker='$')#, back_marker=answer1)
        #bot.send_message(message.chat.id, reply_markup=kb_turnaround, text='Выберете тайм фрейм:')
        #answer1 = call.data
        if True:#bot.register_next_step_handler(kb_turnaround):#call.data !='':
            #print(message.text)
            timeStart = time.time()
            #bot.register_next_step_handler(bot,kb_turnaround)
            bot.send_message(message.chat.id, "Я получил запрос на поиск разворотного паттерна, это займет время, ищу... " , message.text)
            tf = str(re.search(r"(\S+$)", str(message.text)).group(0))
            allFolders = tz2(tf)
            for i in allFolders:
                pngs = list(filter(lambda x: x.endswith('.png'), os.listdir(i)))
                for j in pngs:
                    img = open(i + j,'rb')
                    bot.send_photo(message.chat.id, img)
                    img.close()
                    time.sleep(.25)
            lost = int((time.time() - timeStart) / 60)
            bot.send_message(message.chat.id, "Закончил поиск (" + message.text + "), на это ушло " + str(lost) + " минут")
        else:
            #bot.send_message(message.chat.id, "(4T_Bot) Привет, я получил сообщение: " + message.text)
            pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
