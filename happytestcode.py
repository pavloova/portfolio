import telebot
from telebot import types
import pymysql
from telebot.handler_backends import State, StatesGroup
import datetime

bot = telebot.TeleBot("6106587330:AAEK30s90WNyolU_7v2wLhF3ehI2mQkadNw")

conn = pymysql.connect(
      host="rc1b-nygyxijaphvk1bh3.mdb.yandexcloud.net",
      port=3306,
      db="dbhappy0",
      user="ilya",
      passwd="password",
      ssl={'ca': 'root.crt'})


cur = conn.cursor()
cur.execute('SELECT version()')


class stat(StatesGroup):
    name = State()
    category = State()
    spends = State()
    happy = State()

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.KeyboardMarkup()
    btn1 = types.KeyboardButton("➕ Добавить расход")
    btn2 = types.KeyboardButton("➖ Убрать последний расход")
    btn3 = types.KeyboardButton("🟰 Сводка по расходам")
    btn4 = types.KeyboardButton("😃 Уровень счастья")
    btn5 = types.KeyboardButton(text = "📑 Методичка")
    
   
  
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я тестовый бот для счастьеметра".format(
                         message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "➕ Добавить расход"):
        bot.set_state(message.from_user.id, stat.name, message.chat.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🛒 Продукты")
        btn2 = types.KeyboardButton("🚕 Транспорт")
        btn3 = types.KeyboardButton("👚 Одежда")
        btn4 = types.KeyboardButton("🍽️ Ресторан")
        btn5 = types.KeyboardButton("🏠 Аренда")
        btn6 = types.KeyboardButton("🎓 Образование")
        btn7 = types.KeyboardButton("🏆 Спорт")
        btn8 = types.KeyboardButton("⚪️ Остальное")
        back = types.KeyboardButton("Вернуться в главное меню")
        bot.register_next_step_handler(message, get_category)
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8,back)
        bot.send_message(message.chat.id, text="Выберите категорию", reply_markup=markup)
    elif (message.text == "🟰 Сводка по расходам"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Расходы за месяц")
        btn2 = types.KeyboardButton("Расходы за неделю")
        btn3 = types.KeyboardButton("Расходы за день")
        back = types.KeyboardButton("Вернуться в главное меню")
        bot.register_next_step_handler(message, summary_of_expenses)
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(message.chat.id, text="За какой период?", reply_markup=markup)
    elif (message.text == "➖ Убрать последний расход"):
      username = message.from_user.username
      cur.execute("SELECT category from spends WHERE username = %s ORDER BY time DESC LIMIT 1", (username))
      show_category = cur.fetchone()[0] or 0
      cur.execute("SELECT spends from spends WHERE username = %s ORDER BY time DESC LIMIT 1", (username))
      show_spends = cur.fetchone()[0] or 0
      message_text = f"{show_category}: {show_spends} руб. \n"
      cur.execute("DELETE FROM spends WHERE username = %s ORDER BY time DESC LIMIT 1",(username))
      bot.send_message(message.chat.id, text=message_text)
    elif (message.text == "😃 Уровень счастья"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Счастье за месяц")
        btn2 = types.KeyboardButton("Счастье за неделю")
        btn3 = types.KeyboardButton("Счастье за день")
        back = types.KeyboardButton("Вернуться в главное меню")
        bot.register_next_step_handler(message, summary_of_happiness)
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(message.chat.id, text="За какой период?", reply_markup=markup)
    elif(message.text == "📑 Методичка"):
      bot.send_media_group(message.chat.id,[telebot.types.InputMediaPhoto(open(photo,'rb')) for photo in['p1.png','p2.png','p3.png']])   
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("➕ Добавить расход")
        btn2 = types.KeyboardButton("➖ Убрать последний расход")
        btn3 = types.KeyboardButton("🟰 Сводка по расходам")
        btn4 = types.KeyboardButton("😃 Уровень счастья")
        btn5 = types.KeyboardButton("📑 Методичка")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text="Мне пока рано до этой функции", reply_markup=markup)

@bot.message_handler(state=stat.category)
def get_category(message):
    if (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("➕ Добавить расход")
        btn2 = types.KeyboardButton("➖ Убрать последний расход")
        btn3 = types.KeyboardButton("🟰 Сводка по расходам")
        btn4 = types.KeyboardButton("😃 Уровень счастья")
        btn5 = types.KeyboardButton("📑 Методичка")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text="Чем я могу помочь?", reply_markup=markup)
    elif (message.text == "🛒 Продукты" or message.text == "🚕 Транспорт" or message.text == "👚 Одежда" or message.text == "🍽️ Ресторан" or message.text == "🏠 Аренда" or message.text == "🎓 Образование" or message.text == "🏆 Спорт" or message.text == "⚪️ Остальное"):
        remove = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите сумму", reply_markup=remove)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['category'] = message.text
        bot.register_next_step_handler(message, get_spends)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🛒 Продукты")
        btn2 = types.KeyboardButton("🚕 Транспорт")
        btn3 = types.KeyboardButton("👚 Одежда")
        btn4 = types.KeyboardButton("🍽️ Ресторан")
        btn5 = types.KeyboardButton("🏠 Аренда")
        btn6 = types.KeyboardButton("🎓 Образование")
        btn7 = types.KeyboardButton("🏆 Спорт")
        btn8 = types.KeyboardButton("⚪️ Остальное")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, back)
        bot.send_message(message.chat.id, text="Пожалуйста, выберите среди предложенных категорий", reply_markup=markup)
        bot.register_next_step_handler(message, get_category)

@bot.message_handler(state=stat.spends)
def get_spends(message):
    try:
        message.text = int(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1⭐️")
        btn2 = types.KeyboardButton("2⭐️")
        btn3 = types.KeyboardButton("3⭐️")
        btn4 = types.KeyboardButton("4⭐️")
        btn5 = types.KeyboardButton("5⭐️")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text="Введите уровень счастья", reply_markup=markup)
        bot.register_next_step_handler(message, get_happy)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['spends'] = message.text
    except Exception:
        bot.send_message(message.from_user.id, 'Пожалуйста, введите сумму, на которую была совершена покупка')
        bot.register_next_step_handler(message, get_spends)


def get_happy(message):
    if (message.text == "1⭐️"):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            msg = ("Расход записан:\n"
               f"<b>Категория: </b> {data['category']}\n"
               f"<b>Сумма: </b> {data['spends']}\n"
               f"<b>Уровень счастья: </b> {message.text}")
        username = message.from_user.username
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total = 1 * data['spends']
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("➕ Добавить расход")
        btn2 = types.KeyboardButton("➖ Убрать последний расход")
        btn3 = types.KeyboardButton("🟰 Сводка по расходам")
        btn4 = types.KeyboardButton("😃 Уровень счастья")
        btn5 = types.KeyboardButton("📑 Методичка")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text=msg, reply_markup=markup, parse_mode="html")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            cur.execute("INSERT INTO spends (user_id, time, username, category, happy, spends, total) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, time, username, data['category'], 1, data['spends'], total))
            conn.commit()
    elif (message.text == "2⭐️"):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            msg = ("Расход записан:\n"
               f"<b>Категория: </b> {data['category']}\n"
               f"<b>Сумма: </b> {data['spends']}\n"
               f"<b>Уровень счастья: </b> {message.text}")
        username = message.from_user.username
        total = 2 * data['spends']
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("➕ Добавить расход")
        btn2 = types.KeyboardButton("➖ Убрать последний расход")
        btn3 = types.KeyboardButton("🟰 Сводка по расходам")
        btn4 = types.KeyboardButton("😃 Уровень счастья")
        btn5 = types.KeyboardButton("📑 Методичка")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text=msg, reply_markup=markup, parse_mode="html")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            cur.execute("INSERT INTO spends (user_id, time, username, category, happy, spends, total) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, time, username, data['category'], 2, data['spends'], total))
            conn.commit()
    elif (message.text == "3⭐️"):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            msg = ("Расход записан:\n"
               f"<b>Категория: </b> {data['category']}\n"
               f"<b>Сумма: </b> {data['spends']}\n"
               f"<b>Уровень счастья: </b> {message.text}")
        username = message.from_user.username
        total = 3 * data['spends']
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("➕ Добавить расход")
        btn2 = types.KeyboardButton("➖ Убрать последний расход")
        btn3 = types.KeyboardButton("🟰 Сводка по расходам")
        btn4 = types.KeyboardButton("😃 Уровень счастья")
        btn5 = types.KeyboardButton("📑 Методичка")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text=msg, reply_markup=markup, parse_mode="html")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            cur.execute("INSERT INTO spends (user_id, time, username, category, happy, spends, total) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, time, username, data['category'], 3, data['spends'], total))
            conn.commit()
    elif (message.text == "4⭐️"):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            msg = ("Расход записан:\n"
               f"<b>Категория: </b> {data['category']}\n"
               f"<b>Сумма: </b> {data['spends']}\n"
               f"<b>Уровень счастья: </b> {message.text}")
        username = message.from_user.username
        total = 4 * data['spends']
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("➕ Добавить расход")
        btn2 = types.KeyboardButton("➖ Убрать последний расход")
        btn3 = types.KeyboardButton("🟰 Сводка по расходам")
        btn4 = types.KeyboardButton("😃 Уровень счастья")
        btn5 = types.KeyboardButton("📑 Методичка")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text=msg, reply_markup=markup, parse_mode="html")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            cur.execute("INSERT INTO spends (user_id, time, username, category, happy, spends, total) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, time, username, data['category'], 4, data['spends'], total))
            conn.commit()
    elif (message.text == "5⭐️"):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            msg = ("Расход записан:\n"
               f"<b>Категория: </b> {data['category']}\n"
               f"<b>Сумма: </b> {data['spends']}\n"
               f"<b>Уровень счастья: </b> {message.text}")
        total = 5*data['spends']
        username = message.from_user.username
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("➕ Добавить расход")
        btn2 = types.KeyboardButton("➖ Убрать последний расход")
        btn3 = types.KeyboardButton("🟰 Сводка по расходам")
        btn4 = types.KeyboardButton("😃 Уровень счастья")
        btn5 = types.KeyboardButton("📑 Методичка")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text=msg, reply_markup=markup, parse_mode="html")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            cur.execute("INSERT INTO spends (user_id, time, username, category, happy, spends, total) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, time, username, data['category'], 5, data['spends'], total))
            conn.commit()
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1⭐️")
        btn2 = types.KeyboardButton("2⭐️")
        btn3 = types.KeyboardButton("3⭐️")
        btn4 = types.KeyboardButton("4⭐️")
        btn5 = types.KeyboardButton("5⭐️")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text="Пожалуйста, введите значение от 1 до 5", reply_markup=markup)
        bot.register_next_step_handler(message, get_happy)

def summary_of_expenses(message):
    user_id = message.from_user.id
    if message.text == "Расходы за месяц":
        message_text = "Сводка за последний месяц:\n\n"
        for category in ["🛒 Продукты", "🚕 Транспорт", "👚 Одежда", "🍽️ Ресторан", "🏠 Аренда", "🎓 Образование", "🏆 Спорт", "⚪️ Остальное"]:
            sql = "SELECT SUM(spends) FROM spends WHERE user_id = %s AND category = %s AND time >= ( CURDATE() - INTERVAL 30 DAY )"
            cur.execute(sql, (user_id, category))
            conn.commit()
            total = cur.fetchone()[0] or 0
            message_text += f"{category}: {total} руб. \n"
        bot.send_message(message.chat.id, text=message_text)
        bot.register_next_step_handler(message, summary_of_expenses)
    elif message.text == "Расходы за неделю":
        message_text = "Сводка за последнюю неделю:\n\n"
        for category in ["🛒 Продукты", "🚕 Транспорт", "👚 Одежда", "🍽️ Ресторан", "🏠 Аренда", "🎓 Образование", "🏆 Спорт", "⚪️ Остальное"]:
            sql = "SELECT SUM(spends) FROM spends WHERE user_id = %s AND category = %s AND time >= ( CURDATE() - INTERVAL 7 DAY )"
            cur.execute(sql, (user_id, category))
            conn.commit()
            total = cur.fetchone()[0] or 0
            message_text += f"{category}: {total} руб. \n"
        bot.send_message(message.chat.id, text=message_text)
        bot.register_next_step_handler(message, summary_of_expenses)
    elif message.text == "Расходы за день":
        message_text = "Сводка за сегодня:\n\n"
        for category in ["🛒 Продукты", "🚕 Транспорт", "👚 Одежда", "🍽️ Ресторан", "🏠 Аренда", "🎓 Образование", "🏆 Спорт", "⚪️ Остальное"]:
            sql = "SELECT SUM(spends) FROM spends WHERE user_id = %s AND category = %s AND time >= CURDATE()"
            cur.execute(sql, (user_id, category))
            conn.commit()
            total = cur.fetchone()[0] or 0
            message_text += f"{category}: {total} руб. \n"
        bot.send_message(message.chat.id, text=message_text)
        bot.register_next_step_handler(message, summary_of_expenses)
    elif message.text == "Вернуться в главное меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("➕ Добавить расход")
            btn2 = types.KeyboardButton("➖ Убрать последний расход")
            btn3 = types.KeyboardButton("🟰 Сводка по расходам")
            btn4 = types.KeyboardButton("😃 Уровень счастья")
            btn5 = types.KeyboardButton("📑 Методичка")
            markup.add(btn1, btn2, btn3, btn4, btn5)
            bot.send_message(message.chat.id, text="Чем я могу помочь?", reply_markup=markup)

def summary_of_happiness(message):
    user_id = message.from_user.id
    if message.text == "Счастье за месяц":
        message_text = "Сводка за последний месяц:\n\n"
        for category in ["🛒 Продукты", "🚕 Транспорт", "👚 Одежда", "🍽️ Ресторан", "🏠 Аренда", "🎓 Образование", "🏆 Спорт", "⚪️ Остальное"]:
            lvl_happy = "SELECT SUM(total) FROM spends WHERE user_id = %s AND category = %s AND time >= ( CURDATE() - INTERVAL 30 DAY )"
            cur.execute(lvl_happy, (user_id, category))
            total_happy = cur.fetchone()[0] or 0
            lvl_spends = "SELECT SUM(spends) FROM spends WHERE user_id = %s AND category = %s AND time >= ( CURDATE() - INTERVAL 30 DAY )"
            cur.execute(lvl_spends, (user_id, category))
            conn.commit()
            total_spends = cur.fetchone()[0] or 0
            try:
                show_level = round((total_happy/total_spends), 1)
            except ZeroDivisionError:
                show_level = 0
            message_text += f"{category}: {show_level} ⭐️ \n"
        bot.send_message(message.chat.id, text=message_text)
        bot.register_next_step_handler(message, summary_of_happiness)
    elif message.text == "Счастье за неделю":
        message_text = "Сводка за последнюю неделю:\n\n"
        for category in ["🛒 Продукты", "🚕 Транспорт", "👚 Одежда", "🍽️ Ресторан", "🏠 Аренда", "🎓 Образование", "🏆 Спорт",
                         "⚪️ Остальное"]:
            lvl_happy = "SELECT SUM(total) FROM spends WHERE user_id = %s AND category = %s AND time >= ( CURDATE() - INTERVAL 7 DAY )"
            cur.execute(lvl_happy, (user_id, category))
            total_happy = cur.fetchone()[0] or 0
            lvl_spends = "SELECT SUM(spends) FROM spends WHERE user_id = %s AND category = %s AND time >= ( CURDATE() - INTERVAL 7 DAY )"
            cur.execute(lvl_spends, (user_id, category))
            conn.commit()
            total_spends = cur.fetchone()[0] or 0
            try:
                show_level = round((total_happy/total_spends), 1)
            except ZeroDivisionError:
                show_level = 0
            message_text += f"{category}: {show_level} ⭐️ \n"
        bot.send_message(message.chat.id, text=message_text)
        bot.register_next_step_handler(message, summary_of_happiness)
    elif message.text == "Счастье за день":
        message_text = "Сводка за сегодня:\n\n"
        for category in ["🛒 Продукты", "🚕 Транспорт", "👚 Одежда", "🍽️ Ресторан", "🏠 Аренда", "🎓 Образование", "🏆 Спорт", "⚪️ Остальное"]:
            lvl_happy = "SELECT SUM(total) FROM spends WHERE user_id = %s AND category = %s AND time >= CURDATE()"
            cur.execute(lvl_happy, (user_id, category))
            total_happy = cur.fetchone()[0] or 0
            lvl_spends = "SELECT SUM(spends) FROM spends WHERE user_id = %s AND category = %s AND time >= CURDATE()"
            cur.execute(lvl_spends, (user_id, category))
            conn.commit()
            total_spends = cur.fetchone()[0] or 0
            try:
                show_level = round((total_happy/total_spends), 1)
            except ZeroDivisionError:
                show_level = 0
            message_text += f"{category}: {show_level} ⭐️ \n"
        bot.send_message(message.chat.id, text=message_text)
        bot.register_next_step_handler(message, summary_of_happiness)
    elif message.text == "Вернуться в главное меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("➕ Добавить расход")
            btn2 = types.KeyboardButton("➖ Убрать последний расход")
            btn3 = types.KeyboardButton("🟰 Сводка по расходам")
            btn4 = types.KeyboardButton("😃 Уровень счастья")
            btn5 = types.KeyboardButton("📑 Методичка")
            markup.add(btn1, btn2, btn3, btn4, btn5)
            bot.send_message(message.chat.id, text="Чем я могу помочь?", reply_markup=markup)


def menu(message):
    if (message.text == "Меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("➕ Добавить расход")
        btn2 = types.KeyboardButton("➖ Убрать последний расход")
        btn3 = types.KeyboardButton("🟰 Сводка по расходам")
        btn4 = types.KeyboardButton("😃 Уровень счастья")
        btn5 = types.KeyboardButton("📑 Методичка")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text="Чем я могу помочь?", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("➕ Добавить расход")
        btn2 = types.KeyboardButton("➖ Убрать последний расход")
        btn3 = types.KeyboardButton("🟰 Сводка по расходам")
        btn4 = types.KeyboardButton("😃 Уровень счастья")
        btn5 = types.KeyboardButton("📑 Методичка")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text="Выберите категорию", reply_markup=markup)


bot.polling(none_stop=True)
conn.close()
