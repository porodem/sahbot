#telegram bot MUP SAH non-official test
#bot name:  sahbot
#bot username: mupsah_bot


import telebot
import re
from telebot import types

bot = telebot.TeleBot("TOKEN", parse_mode=None)

#print(bot.get_me())
#print(bot.get_chat('@tbros'))
#bot.send_message('@tbros','aaa')

types.MenuButtonDefault('default')

#commands
@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message, "\U0001F916Добро пожаловать!")

@bot.message_handler(regexp=".*регистр.*")
def echo_rex(message):
    bot.reply_to(message, '''Вы хотите зарегистрировать ЛК!''')

@bot.message_handler(regexp=".*ицевой.*")
def echo_rex(message):
    bot.reply_to(message, '''Вы хотите узнать ЛС!''')

#regexp example 3
@bot.message_handler(regexp=".*(рикрепи|обавить).*")
def echo_rex(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton('send shit'))
    msg = bot.send_message(message.chat.id, "choose type shit", reply_markup=markup)

#anything other messages
#@bot.message_handler(func=lambda m:True)
#def echo_all(message):
#    bot.reply_to(message, message.text)

bot.infinity_polling()
