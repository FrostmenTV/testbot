import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start']) #при вводе команды /start
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    hyperlink = f'<a href="tg://user?id={user_id}">{user_name}</a>'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Посты") #после /start
    markup.add(btn1)
    bot.send_message(message.chat.id, f"Приветствую тебя,{hyperlink}! Выбери один из нужных тебе пунктов.\n"
                     "Чтобы узнать мое назначение введи <code>/help</code>".format(message.from_user), reply_markup=markup, parse_mode='HTML')

@bot.message_handler(commands=["help"]) #при вводе команды /help
def helps(message):
    bot.reply_to(message, "Я создан для помощи <u>Ректорам Группы ВК Black Russia</u>\n"
                 "А именно: помощь в находении творческих идей для создания постов и копирования готовых шаблонов для ускорения работы в трудные моменты.")

bot.message_handler(commands=["button"])
def button(message): 
    global reason
    if message.chat.type == "private":   
        if message.text == "Посты":
            markup = types.InlineKeyboardMarkup(row_with=1) #создание новых кнопок
            btn1 = types.KeyboardButton('й') 
            btn2 = types.KeyboardButton('й')
            btn3 = types.KeyboardButton('й')
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, btn3,back)
            bot.send_message(message.chat.id, f'{hyperlink},нажми на кнопку снизу'.format(message.from_user), reply_markup=markup, parse_mode='HTML') #ответ бота



    elif (message.text == "Вернуться в главное меню"):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        hyperlink = f'<a href="tg://user?id={user_id}">{user_name}</a>'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Посты") #после /start
        # btn2 = types.KeyboardButton("") #после /start
        markup.add(btn1,btn2)
        bot.send_message(message.chat.id, text=f'{hyperlink},Вы вернулись в главное меню.' .format(message.from_user), reply_markup=markup, parse_mode='HTML')    
bot.polling(none_stop=True) #обязательная для работы бота часть