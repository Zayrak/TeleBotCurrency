import traceback
import telebot
from extensions import APIException, Converter
from Config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = f"Добро пожаловать! \nВас приветсвует конвертер валют. \nДля того чтобы получить список доступных валют \
           нажмитe /values \nДля того чтобы получить конвертируемую валюту введите в одну строчку запрос в формате:\
           \n<имя валюты, цену которой необходимо узнать> \n<имя валюты, в которую необходимо конвертировать> \
           \n<количество валюты> \nпример: <доллар рубль 777>"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys:
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    value = message.text.split(' ')
    try:
        if len(value) != 3:
            raise APIException("Неверное количество параметров, должно быть три парамета!")

        answer = Converter.get_price(*value)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()
