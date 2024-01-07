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
    btn1 = types.KeyboardButton("Меню 1") #после /start
    btn2 = types.KeyboardButton("Меню 2") #после /start
    markup.add(btn1,btn2)
    bot.send_message(message.chat.id, f"Привет, {hyperlink}! Выбери пункт из предложенных на экране вашего устройства".format(message.from_user), reply_markup=markup, parse_mode='HTML')
    
@bot.message_handler(content_types=['text'])
def get_text_messages(message): #переменная для 2 сцены

    if message.text == 'Меню 1':
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        hyperlink = f'<a href="tg://user?id={user_id}">{user_name}</a>'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('тест 1') 
        btn2 = types.KeyboardButton('тест2')
        btn3 = types.KeyboardButton('тест ссылка')
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3,back)
        bot.send_message(message.chat.id, f'{hyperlink},нажми на кнопку снизу'.format(message.from_user), reply_markup=markup, parse_mode='HTML') #ответ бота

    if message.text == 'Меню 2':
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        hyperlink = f'<a href="tg://user?id={user_id}">{user_name}</a>'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn4 = types.KeyboardButton('тест3')
        btn5 = types.KeyboardButton('тест4')
        btn6 = types.KeyboardButton('тест ссылка2')
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn4, btn5, btn6,back)
        bot.send_message(message.chat.id, f'{hyperlink},нажми на кнопку снизу'.format(message.from_user), reply_markup=markup, parse_mode='HTML') #ответ бота
#ответ при переходе на 3 сцену
    elif message.text == 'тест 1':
        bot.send_message(message.from_user.id, 'тест')

    elif message.text == 'тест2':
        bot.send_message(message.from_user.id, 'тест2')
    elif message.text == 'тест3':
        bot.send_message(message.from_user.id, 'тест2')
    elif message.text == 'тест4':
        bot.send_message(message.from_user.id, 'тест2')

    elif message.text == 'тест ссылка':
        bot.send_message(message.from_user.id, 'ВК ' + 'по [ссылке](vk.com/im)', parse_mode='Markdown')
    elif message.text == 'тест ссылка2':
        bot.send_message(message.from_user.id, 'ВК ' + 'по [ссылке](vk.com/im)', parse_mode='Markdown')

    elif (message.text == "Вернуться в главное меню"):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        hyperlink = f'<a href="tg://user?id={user_id}">{user_name}</a>'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Меню 1") #после /start
        btn2 = types.KeyboardButton("Меню 2") #после /start
        markup.add(btn1,btn2)
        bot.send_message(message.chat.id, text=f'{hyperlink},Вы вернулись в главное меню.' .format(message.from_user), reply_markup=markup, parse_mode='HTML')

bot.polling(none_stop=True) #обязательная для работы бота часть
