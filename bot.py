import telebot
from telebot import types
import sqlite3
import config

bot = telebot.TeleBot(config.token)


# начальный запуск
@bot.message_handler(commands=["start"])
def start(message):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                   user_id INTEGER,
                   nickname TEXT,
                   super_user INTEGER)""")
    conn.commit()
    conn.close()

    if user_exists(message.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Посты")
        item2 = types.KeyboardButton("Шаблоны")

        markup.add(item1, item2)

        bot.send_message(message.chat.id,
                         "Привет, {0.first_name}, нажми на необходимую тебе кнопку".format(message.from_user),
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "❌ Доступ закрыт.")


@bot.message_handler(commands=["wlist"])
def wlist(message):
    if len(message.text.split()) >= 4:
        user_id = message.from_user.id
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            if row[2] == 1:
                user_id = int(message.text.split()[1])
                nickname = message.text.split()[2]
                super_user = int(message.text.split()[3])
                cursor.execute("INSERT INTO Users (user_id, nickname, super_user) VALUES (?, ?, ?)",
                               (user_id, nickname, super_user))
                bot.send_message(message.chat.id, "Пользователь успешно добавлен в Базу данных!")
            else:
                bot.send_message(message.chat.id, "Вы не можете выдавать WhiteList.")
        else:
            bot.send_message(message.chat.id, "У вас нет доступа к использованию данного бота.")
        conn.commit()
        conn.close()
    else:
        bot.send_message(message.chat.id, f'Неправильный формат ввода.\n'
                                          'Для добавления пользователя используйте\n /wlist ID пользователя,ник нейм и 1-0\n'
                                          'Где 1 - супер пользователь, 0 обычный пользователь')


@bot.message_handler(commands=["delwlist"])
def delwlist(message):
    if len(message.text.split()) >= 2:
        user_id = message.from_user.id
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            if row[2] == 1:
                user_id = int(message.text.split()[1])
                cursor.execute("DELETE FROM user WHERE user_id = ?", (user_id,))
                bot.send_message(message.chat.id, "Пользователь удалён из Базы данных.")
            else:
                bot.send_message(message.chat.id, "Вы не можете снимать WhiteList.")
        else:
            bot.send_message(message.chat.id, "У вас нет доступа к использованию данного бота.")
        conn.commit()
        conn.close()
    else:
        bot.send_message(message.chat.id, "Неправильный формат ввода.")


# идем по постам
@bot.message_handler(content_types=['text'])
def get_text_messages(message):  # переменная для 2 сцены
    if user_exists(message.from_user.id):
        markup = ''
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True)  # создаем и не нужно будет указывать её постоянно в if (создание кнопок)
        if message.text == 'Посты':
            btn1 = types.KeyboardButton('Музыка')
            btn2 = types.KeyboardButton('Опрос')
            btn3 = types.KeyboardButton('Лучший адм')
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, btn3, back)
            bot.send_message(message.chat.id,
                             "Привет, {0.first_name}, нажми на необходимую тебе кнопку".format(message.from_user),
                             reply_markup=markup)

        elif message.text == 'Музыка':
            btn1 = types.KeyboardButton('Готовый шаблон')
            btn2 = types.KeyboardButton('Чистый шаблон')
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, back)
            bot.send_message(message.chat.id,
                             '{0.first_name}, Выбери нужную тебе кнопку.'.format(message.from_user),
                             reply_markup=markup)

        elif (message.text == "Вернуться в главное меню"):
            item1 = types.KeyboardButton("Посты")
            item2 = types.KeyboardButton("Шаблоны")
            markup.add(item1, item2)
            bot.send_message(message.chat.id,
                             "Привет, {0.first_name}, нажми на необходимую тебе кнопку".format(message.from_user),
                             reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "❌ Доступ закрыт.")


def user_exists(user_id):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
    count = cursor.fetchone()[0]
    return count > 0


@bot.callback_query_handler(func=lambda call: call.data == "accept")
def handle_form_accept(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


if __name__ == '__main__':
    bot.polling()
