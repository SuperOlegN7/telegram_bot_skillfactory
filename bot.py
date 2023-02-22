import telebot
from exceptions import APIException, Convertor
from conf import TOKEN, keys
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username}, и добро пожаловать, я бот призванный помочь тебе с информацией по текущему курсу валют. Для вызова раздела помощи набери команду /help")

@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Для того чтобы узнать текущий курс валют введите команду в следующем формате: "
                                      f"\n<интересующая валюта> \<в какую валюту перевести> \<сумма необходимой валюты>")

@bot.message_handler(commands=['currencies'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)

bot.polling()