# import config
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)

logs = {}
log_status = {}


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет, я бот помощник для технических специалистов проекта Black Russia! Напиши /help, "
                          "чтобы узнать мои команды")


@bot.message_handler(commands=["report"])
def report(message):
    msg = bot.reply_to(message, "Вы находитесь в меню создания репорта. Выберите, что вы хотите сделать:\n"
                                "1. Написать предложение по улучшению бота\n"
                                "2. Отправить отчёт о найденном баге.\n"
                                "Для выбора напишите номер нужно вам варианта.\n"
                                "Для возврата назад введите 'break'")
    bot.register_next_step_handler(msg, reg_report)


def reg_report(message):
    if message.text == "break":
        msg = bot.reply_to(message, "Вы вернулись назад.")
        bot.register_next_step_handler(msg, helps)
    elif message.text == "1":
        msg = bot.reply_to(message, "Вы выбрали написать предложение по улучшению. Следующим сообщением отправьте "
                                    "своё предложение. Чтобы вернуться в меню /help напишите 'break'")
        bot.register_next_step_handler(msg, write_report_predl)
    elif message.text == "2":
        msg = bot.reply_to(message, "Вы выбрали сообщить о найденном баге. Следующим сообщением напишите "
                                    "ваш баг-репорт."
                                    "\nЧтобы вернуться в меню /help напишите 'break'")
        bot.register_next_step_handler(msg, write_bug_report)


def write_bug_report(message):
    if message.text == "break":
        msg = bot.reply_to(message, "Вы вернулись назад.")
        bot.register_next_step_handler(msg, helps)
    else:
        chat_id = -1002062388148
        bug_report = types.InlineKeyboardMarkup()
        callback = types.InlineKeyboardButton(text="Исправлено", callback_data="fix")
        bug_report.add(callback)
        bot.send_message(chat_id, f"БАГ РЕПОРТ ОТ ПОЛЬЗОВАТЕЛЯ {message.from_user.first_name}.\n"
                                  f"{message.text}", reply_markup=bug_report)
        bot.reply_to(message, "Сообщение о баге было отправлено.\n"
                              "Вам придёт уведомление, если баг будет исправлен.")


def write_report_predl(message):
    if message.text == "break":
        msg = bot.reply_to(message, "Вы вернулись назад.")
        bot.register_next_step_handler(msg, helps)
    else:
        chat_id = -1002062388148
        predl = types.InlineKeyboardMarkup()
        callback = types.InlineKeyboardButton(text="Реализовано", callback_data="realize")
        predl.add(callback)
        bot.send_message(chat_id, f"Улучшение от пользователя {message.from_user.first_name}. "
                                  f"\n"
                                  f"{message.text}", reply_markup=predl)
        bot.reply_to(message, "Ваше предложение успешно отправлено!\n"
                              " Если вашу идею реализуют, то вам придёт уведомление.")
        # predlog = open("C:\\Users\\Никита Породько\\PycharmProjects\\bot_for_tech\\venv\\buff_predlogneiya.txt", "r+")
        # predlog.write(f"\n{message}-{message.chat.id}")
        # predlog.close()


@bot.message_handler(commands=["help"])
def helps(message):
    bot.reply_to(message, "Я могу создать форму на выдачу наказания. Пропиши /givepunish для дальнейших инструкций\n"
                          "Также я могу логировать блокировки, пропиши /info_log для подробной информации.")


@bot.message_handler(commands=["info_log"])
def info_log(message):
    bot.reply_to(message, "Здесь описана работа системы логирования выдачи наказаний.\n"
                          "Все ники, которые вы введёте на выдачу наказаний будут автоматически записаны в лог.\n"
                          "Учтите, что логирование ведётся сразу после отправки формы на выдачу бана ботом.\n"
                          "Для активации функции логирования пропишите /use_log\n"
                          "Посмотреть свои логи можно по команде /mylogs\n"
                          "Для очистки логов введите /log_clear")
    if message.chat.id not in logs:
        logs[message.chat.id] = []


@bot.message_handler(commands=["mylogs"])
def mylogs(message):
    if message.chat.id in logs:
        if len(logs[message.chat.id]) > 0:
            logi = "\n".join(logs[message.chat.id])
            bot.reply_to(message, logi)
        else:
            bot.reply_to(message, "Ваши логи пусты.")
    else:
        bot.reply_to(message, "Вы не разу не использовали логи. Пропишите /info_log для подключения к системе.")


# запрашиваю у пользователя нужную ему команду и причину
@bot.message_handler(commands=["givepunish"])
def commands(message):
    msg = bot.reply_to(message, "Вы активировали режим создания форм.\n"
                                "Введите в одну строку:\n"
                                "команда(без слэша) [причина наказания]\n"
                                "Чтобы вернуться назад введите 'break'")
    bot.register_next_step_handler(msg, settings)


# распаковываю причину и наказание
def extract_reason(reason):
    return str(reason).split()[1:]


def extract_punishment(punishment):
    return str(punishment).split()[0]


@bot.message_handler(commands=["use_log"])
def use_log(message):
    if message.chat.id in log_status:
        if not log_status[message.chat.id]:
            log_status[message.chat.id] = True
            bot.reply_to(message, "Ситема логирования активирована.")
        else:
            log_status[message.chat.id] = False
            bot.reply_to(message, "Система логирования отключена.")
    elif message.chat.id not in logs:
        logs[message.chat.id] = []
        log_status[message.chat.id] = True
        bot.reply_to(message, "Ситема логирования активирована.")


@bot.message_handler(commands=["log_clear"])
def log_clear(message):
    if len(logs[message.chat.id]) > 0:
        logs[message.chat.id].clear()
        bot.reply_to(message, "Ваши логи были очищены!")
    else:
        bot.reply_to(message, "Ваши логи пусты, очистка не требуется.")


def settings(message):
    global reason
    # наказание настроено, запрашиваю список ников
    global punishment
    if message.text == "break":
        msg = bot.reply_to(message, "Вы вернулись назад.")
        bot.register_next_step_handler(msg, helps)
    elif len(message.text.split()) > 1:
        reason = extract_reason(message.text)
        punishment = extract_punishment(message.text)
        msg = bot.reply_to(message, "Вы ввели требуемое действие и причину наказания.\n"
                                    "Теперь введите список ников, на которые нужно сделать форму для выдачи наказания.")
        bot.register_next_step_handler(msg, bans_nick)
    else:
        bot.reply_to(message, "Неправильный формат ввода. Попробуйте снова.\nВведите /givepunish заново.")


# для работы всё готово, начинаю отправлять формы
def bans_nick(message):
    chat_id = message.chat.id
    ban_list = message.text.split()
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="ПРИНЯТО", callback_data="del")
    keyboard.add(callback_button)
    for i in ban_list:
        ban = " ".join(reason[0:])
        bot.send_message(chat_id, f"`\n/{punishment} {i} {ban}`", parse_mode="MARKDOWN",
                         reply_markup=keyboard)
        if message.chat.id in log_status and message.chat.id in logs:
            if log_status[message.chat.id]:
                logs[message.chat.id].append(i)


# обрабатываю удаление сообщения
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "del":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        elif call.data == "realize":
            # bot.send_message(call.message.message_id.text.split()[-1], "Реализовано.")
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


bot.infinity_polling(none_stop=True)
