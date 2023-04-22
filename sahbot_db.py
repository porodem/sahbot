#telegram bot MUP SAH non-official test
#bot name:  sahbot
#bot username: mupsah_bot


import telebot
import re
from telebot import types

import psycopg
#from telebot.service_utils import quick_markup

#DB
def get_ls_from_db(adrs):
    split_adrs = adrs.split(',')

    ls_result = ''

    q = '''select * from ls_adr_split a
    where a.str ~* %s
    and house ~* %s
    and kv = %s
    '''

    p_street = split_adrs[0]
    p_house = split_adrs[1].strip()
    kv = split_adrs[2].strip()
    
    with psycopg.connect('dbname=x user=x host=x password=x')as conn:
        with conn.cursor() as cur:
            cur.execute(q, (p_street,('^' + p_house + '$'),kv,))
            b = cur.fetchall()
            cnt = cur.description
            #print(cnt[0].name)
            for record in b:
                #print(record[1])
                ls_result = record[1] + ' : ' + record[3] 
            conn.commit()
    return ls_result


bot = telebot.TeleBot("x:AAHaeCL-x", parse_mode=None)

print(bot.get_me())
print(types.BotCommandScope)
#print(bot.get_chat('@tbros'))
#bot.send_message('@tbros','aaa')

bc = types.BotCommand('start','начать диалог')
bc_a = types.BotCommand('fun','anekdot')
bc_q = types.BotCommand('question','ask smt')
bot.set_my_commands([bc,bc_a,bc_q])
#bot.set_my_commands([bc,bc_a,bc_q], types.BotCommandScope())



#types.MenuButtonDefault('default')

#commands
@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message, "\U0001F916Добро пожаловать!")
    #Inline Keyboards (don't send msg to the chat)
    k_btn = types.InlineKeyboardButton(text='iLbtn', callback_data='yess')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(k_btn)
    #show lnline keyboard in bot's chat
    bot.send_message(message.from_user.id, text="select", reply_markup=keyboard)
    #start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    #start_markup.row('/start', '/help', '/hide')

#Inline handler (action for bress inline buttons)
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yess": #call.data it's callback_data which we add when initialise button
        #code for saving or processing data
        bot.send_message(call.message.chat.id, 'Got it!')
    elif call.data == "noo":
        bot.send_message(call.message.chat.id, 'oh no!')



@bot.message_handler(regexp=".*регистр.*")
def echo_rex(message):
    bot.reply_to(message, '''Вы хотите зарегистрировать ЛК!''')

@bot.message_handler(regexp=".*ицевой.*")
def echo_rex(message):
    #bot.reply_to(message, '''Хотите узнать новый ЛС в МУП САХ?''')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('мой ЛС'))
    msg = bot.send_message(message.chat.id, "Хотите узнать новый ЛС в МУП САХ?", reply_markup=markup)

#regexp example 3
@bot.message_handler(regexp=".*(рикрепи|обавить).*")
def attach_ls(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('send shit'))
    msg = bot.send_message(message.chat.id, "choose type shit", reply_markup=markup)
    

#anything other messages
@bot.message_handler(func=lambda m:True)
def echo_all(message):
    if message.text == 'send shit':
        bot.reply_to(message,'Take shit')
    elif message.text == 'мой ЛС':
        bot.reply_to(message,'Here your new LS')
    elif message.text == 'ls':
        person_ls = get_ls_from_db('владимировская,3,1')
        bot.reply_to(message,person_ls)

bot.infinity_polling()


    
