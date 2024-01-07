import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    hyperlink = f'<a href="tg://user?id={user_id}">{user_name}</a>'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Посты") #после /start
    markup.add(btn1)
    bot.send_message(message.chat.id, f"Приветствую тебя,{hyperlink}! Выбери один из нужных тебе пунктов.\n"
                     "Чтобы узнать мое назначение введи <code>/help</code>".format(message.from_user), reply_markup=markup, parse_mode='HTML')

@bot.message_handler(commands=["help"])
def helps(message):
    bot.reply_to(message, "Я могу создать форму на выдачу наказания. Пропиши /givepunish для дальнейших инструкций\n"
                          "Также я могу логировать блокировки, пропиши /info_log для подробной информации.")
    
bot.polling(none_stop=True) #обязательная для работы бота часть