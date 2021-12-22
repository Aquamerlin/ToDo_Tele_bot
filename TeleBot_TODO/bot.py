import sqlite3
from random import choice
import telebot

########################################################################################################################
__conection = None

# Фунция для подключения к БД
def get_connection():
    global __conection
    if __conection is None:
        __conection = sqlite3.connect('db.db')
    return __conection


########################################################################################################################

# Подключение к телеграмм боту по токену
token = '1929963901:AAFnCoJEqd4gm6orqL92M3yFQQlhu9jVdZg'
bot = telebot.TeleBot(token)

# Список рандомных задач
random_list = ['Спросить как дела у родителей', 'Выучить Python', 'Прибраться', 'Посмотреть 4 сезон Рик и Морти',
               'Выйти на пробежку', 'Присесть 10 раз', 'Зарядить телефон', 'Почистить зубы', 'Подтянуться 10 раз',
               'Выгулять собаку', 'Зайти к бабушке', 'Купить тетрадь', 'Прочитать книгу', 'Приготовить что-то',
               'Погладить кота','Улыбнуться']
#Словарь
list = dict()

# Инструкция при вводе "/help"
help_list = """
Список доступных команд:
/print <Дата>  - Вывести все задачи на эту Дату
/add <Дата> <Задача> - Добавить задачу
"""

# Фунция для обработки команды /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row("/help")
    keyboard.row("/random")
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=keyboard)


# Функция для добавления задачи
def add_task(date, task):
    date = date.lower()# делает все символы с нижним регистром
    if list.get(date) is not None:
        list[date].append(task)
    else:
        list[date] = [task]


# Ответ бота на команду "/help"
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, help_list)


# Ответ бота на команду "/random"
@bot.message_handler(commands=['random'])
def random(message):
    task = choice(random_list)
    add_task('сегодня', task)
    bot.send_message(message.chat.id, 'Задача ' + task + ' добавлена успешно')


# Ответ бота на команду "/add"
@bot.message_handler(commands=['add'])
def add(message):
    try:
        print(message.text)
        broken_command = message.text.split(maxsplit=2) # разделитель строк с максимальным разбииением 2
        # Защита от дурака, в дальнейшем можно будет заменить на другое условие
        if len(broken_command) < 3:
            bot.send_message(message.chat.id, 'Введите правильно каманду /add ДАТА ЗАДАЧА')
        else:
            date = broken_command[1]
            task = broken_command[2]
            add_task(date, task)
            add_message(user_id=message.chat.id, cash=task)
            bot.send_message(message.chat.id, 'Задача ' + task + ' добавлена на ' + date)


    except:
        bot.send_message(message.chat.id, 'Ошибка в команде /add ')


# Ответ бота на команду "/print"
@bot.message_handler(commands=['print'])
def print_(message):
    try:
        broken_command = message.text.split()
        date = broken_command[1]
        if date in list:
            text = date.upper() + '\n'# Переход к верхнему регистру
            for task in list[date]:
                text = text + '[ ]' + task + f'\n'
        else:
            text = 'Задач на эту дату нет'
        bot.send_message(message.chat.id, text)

    except:
        bot.send_message(message.chat.id, 'Ошибка в команде /print  ')


########################################################################################################################
# Функция, которая добавляет в таблицу "Cash" id пользователя и его записанную задачу
def add_message(user_id: int, cash: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO 'Cash' ('user_id', 'cash') VALUES (?,?)", (user_id, cash))
    conn.commit()
    

########################################################################################################################

# Постоянное обращение к боту
bot.polling(none_stop=True)
