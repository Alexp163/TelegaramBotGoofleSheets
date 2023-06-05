import telebot
from telebot import types

from connect_table_4 import recording_data
from connect_table_4 import data_collection_function
from connect_table_4 import data_delivery_fuction
from connect_table_4 import recording_delivery_address
from connect_table_4 import recording_transport_company

TOKEN = '5602947799:AAHIHYWPme7pp62rtz3LUZXEbGQeGSy6rAg'
bot = telebot.TeleBot(TOKEN)
dict_index_address = {}
dict_customer_data = {}
transport_company = ''


@bot.message_handler(commands=['start']) # декоратор, который реагирует на входящие сообщения и запускает работу бота командой start
def start(message):  # запуск приветствия бота и первых кнопок
    """
    1. Функция запускает работу телеграм-бота
    2. Функция, которая запускает работу бота, после ввода сообщения start и подгружает
    меню с 5-ю кнопками, а так же выводит приветствие пользователя.
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.chat.id выводит сообщение пользователю в бот
    4. функция ничего не возвращает
    """
    user_name = message.from_user.username # автоопределение имени пользователя запросом в бот
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu = types.KeyboardButton('Главное меню')
    calculator = types.KeyboardButton('Калькулятор')
    personal_account = types.KeyboardButton('Личный кабинет')
    frequent_questions = types.KeyboardButton('Частые вопросы')
    contact_us = types.KeyboardButton('Связь с нами')
    markup.add(main_menu)
    markup.add(calculator)
    markup.add(personal_account)
    markup.add(frequent_questions)
    markup.add(contact_us)
    bot.send_message(message.chat.id, f'Привет! {user_name}', reply_markup=markup)


def enter_cabinet(message):
    """
    1. Функция запускает работу личного кабинета
    2. Функция, которая запускает работу личного кабинета, после того как пользователь ввел свои личные данные(или пропустил этот шаг)
    , а так же выводит приветствие пользователя(в личном кабинете). Когда пользователь оказывается в личном кабинете запускается меню из 4-х пунктов,
    для дальнейшей работы в кабинете.
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.chat.id выводит сообщение пользователю в бот.
    4. функция ничего не возвращает
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    my_orders = types.KeyboardButton('Мои заказы')
    track_order = types.KeyboardButton('Отследить заказ')
    my_details_for_delivery = types.KeyboardButton('Мои данные для доставки')
    goto_main_menu = types.KeyboardButton('Вернуться в основное меню')
    markup.add(my_orders, track_order, my_details_for_delivery, goto_main_menu)
    bot.send_message(message.chat.id, f'Здравствуйте пользователь, {message.from_user.username}', reply_markup=markup)


def work_cabinet(message):  # функция работы в личном кабинете
    """
    1. Функция ответов на запросы пользователя
    2. Функция, которая выполняет логику взаимодействия непосредственно внутри бота. Обеспечивает взаимодействие между разделами бота
    при использовании кнопок меню личного кабинета.
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.chat.id выводит сообщение пользователю в бот.
    4. функция ничего не возвращает
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Мои заказы':
        bot.send_message(message.chat.id, 'Ваши заказы', reply_markup=markup)
    elif message.text == 'Отследить заказ':
        bot.send_message(message.chat.id, 'Ваш заказ отслеживается', reply_markup=markup)
    elif message.text == 'Мои данные для доставки':
        bot.send_message(message.chat.id, 'Ваши данные для доставки', reply_markup=markup)
    elif message.text == 'Вернуться в основное меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        main_menu = types.KeyboardButton('Главное меню')
        calculator = types.KeyboardButton('Калькулятор')
        personal_account = types.KeyboardButton('Личный кабинет')
        frequent_questions = types.KeyboardButton('Частые вопросы')
        markup.add(main_menu)
        markup.add(calculator)
        markup.add(personal_account)
        markup.add(frequent_questions)
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню', reply_markup=markup)


@bot.message_handler(content_types=['text']) # декоратор, который будет обрабатывать входящие сообщения
def all_messages(message):  # алгоритм работы и взаимодействия бота с пользователем
    """
    1. Функция обработки ответов на запросы пользователя
    2. Функция, которая отображает взаимодействие и работу пользователя с кнопками бота.
    Из этой функции выполняется вызов функции recording_transport_company(user_name, transport_company),
    которая выполняет запись введенных данных в таблицу. Функция recording_transport_company(user_name, transport_company)
    запустится после выбора пользователем названия транспортной компании.
    При нажатии кнопки "ввести личные данные" произойдет вызов функции start_pro(message) -функция начала записи данных пользователя.
    При нажатии кнопки "пропустить ввод данных" произойдет вызов функции get_transport_company(message) - функция фиксации данных о транспортировке в гугл-таблицу.

    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.chat.id выводит сообщения пользователю в бот.
    4. функция ничего не возвращает
    """
    user_name = message.from_user.username # автоопределение имени пользователя запросом в бот
    data_delivery = data_delivery_fuction(user_name)
    data_collection = data_collection_function(user_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Главное меню':
        bot.send_message(message.chat.id, 'Вы вошли в главное меню', reply_markup=markup)
    elif message.text == 'Почта России':
        transport_company = message.text
        recording_transport_company(user_name, transport_company)
        bot.send_message(message.chat.id, 'Вы выбрали "Почту России" как транспортную компанию', reply_markup=markup)
        get_index_address(message)
    elif message.text == 'Сдек':
        transport_company = message.text
        recording_transport_company(user_name, transport_company)
        bot.send_message(message.chat.id, 'Вы выбрали "Сдек" как транспортную компанию:', reply_markup=markup)
        get_index_address(message)
    elif message.text == 'Боксбери':
        transport_company = message.text
        recording_transport_company(user_name, transport_company)
        bot.send_message(message.chat.id, 'Вы выбрали "Боксбери" как транспортную компанию', reply_markup=markup)
        get_index_address(message)
    elif message.text == 'Калькулятор':
        bot.send_message(message.chat.id, 'Вы запустили калькулятор', reply_markup=markup)
    elif message.text == 'Личный кабинет':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        enter_personal_data = types.KeyboardButton('Ввести личные данные')
        skip_data_entry = types.KeyboardButton('Пропустить ввод данных')
        markup.add(enter_personal_data)
        markup.add(skip_data_entry)
        bot.send_message(message.chat.id,
                         'Здравствуйте! Выберите дальнейшее действие',
                         reply_markup=markup)
    elif message.text == 'Ввести личные данные':
        start_pro(message)
    elif message.text == 'Пропустить ввод данных':
        get_transport_company(message)
    elif message.text == 'Частые вопросы':
        bot.send_message(message.chat.id, 'Вы в разделе: частые вопросы', reply_markup=markup)
    elif message.text == 'Связь с нами':
        bot.send_message(message.chat.id, 'Вы в разделе: связь с нами', reply_markup=markup)
    elif message.text == 'Мои заказы':
        bot.send_message(message.chat.id, 'Ваши заказы', reply_markup=markup)
        bot.send_message(message.from_user.id, data_collection)
    elif message.text == 'Отследить заказ':
        bot.send_message(message.chat.id, 'Ваш заказ отслеживается', reply_markup=markup)
    elif message.text == 'Мои данные для доставки':
        bot.send_message(message.chat.id, 'Ваши данные для доставки', reply_markup=markup)
        bot.send_message(message.chat.id, data_delivery)
    elif message.text == 'Вернуться в основное меню':
        main_menu = types.KeyboardButton('Главное меню')
        calculator = types.KeyboardButton('Калькулятор')
        personal_account = types.KeyboardButton('Личный кабинет')
        frequent_questions = types.KeyboardButton('Частые вопросы')
        markup.add(main_menu)
        markup.add(calculator)
        markup.add(personal_account)
        markup.add(frequent_questions)
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню', reply_markup=markup)


def get_index_address(message):
    """
    1. Функция запуска ввода индекса и адреса отделения для доставки товара
    2. Функция, которая запустит начало работы по сбору данных(индекс и адрес отделения) о доставке товара для пользователя. 
    Передаёт управление в функцию entering_index_address(message), в которой будет введен индекс и адрес отделения доставки товара.
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.chat.id выводит сообщение пользователю в бот.
    4. функция ничего не возвращает
    """
    dict_index_address[message.chat.id] = {}
    bot.send_message(message.chat.id, 'Введите индекс и адрес отделения')
    bot.register_next_step_handler(message, entering_index_address)


def entering_index_address(message):  # функция ввода индекса и адреса
    """
    1. Функция ввода индекса и адреса отделения для доставки товара
    2. Функция, которая произведет действие по сбору данных(индекс и адрес отделения) о доставке товара для пользователя. 
    Передаёт управление в функцию welcome_cabinet(message), для перехода в личный кабинет.
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.chat.id выводит сообщение пользователю в бот.
    4. функция ничего не возвращает
    """
    user_name = message.from_user.username # автоопределение имени пользователя запросом в бот
    index_address = message.text
    dict_index_address[message.chat.id]['Индекс и адрес'] = index_address
    recording_delivery_address(user_name, dict_index_address)
    welcome_cabinet(message)


def welcome_cabinet(message):  # функция перехода кнопки в "личный кабинет"
    """
    1. Функция перехода в личный кабинет
    2. Функция, которая создаст кнопку, при нажатии которой, произойдет вызов функции enter_cabinet(message) и пользователя перенаправит в личный кабинет.
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.from_user.id выводит сообщение пользователю в бот.
    4. функция ничего не возвращает
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    my_cabinet = types.KeyboardButton('Перейти в личный кабинет')
    markup.add(my_cabinet)
    bot.send_message(message.from_user.id, 'Спасибо, что ввели данные!', reply_markup=markup)
    enter_cabinet(message)


def start_pro(message):  # функция запуска ввода данных юзера
    """
    1. Функция подготовки к запуску ввода данных пользователя
    2. Функция запустит сбор данных о пользователе, для дальнейшего сбора данных в гугл -таблицу. 
    Отправит запрос на запуск следующей функции get_name(message) с помощью метода 
    bot.register_next_step_handler(message, get_name), для ввода ФИО пользователя. 
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.from_user.id выводит сообщение пользователю в бот.
    4. функция ничего не возвращает
    """
    dict_customer_data[message.chat.id] = {}
    bot.send_message(message.from_user.id, 'Введите своё Ф.И.О.')
    bot.register_next_step_handler(message, get_name)


def get_name(message):  # функция ввода ФИО
    """
    1. Функция принимает данные о ФИО пользователя, с последующей обработкой.
    2. Функция выполнит сбор и обработку данных о ФИО пользователя,
    с добавлением полученных данных в переменную dict_customer_data. 
    Отправит запрос на запуск следующей функции get_telephone(message), при помощи метода 
    bot.register_next_step_handler(message, get_name), для ввода телефона пользователя. 
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.from_user.id выводит сообщение пользователю в бот.
    4. функция ничего не возвращает
    """
    name = message.text
    dict_customer_data[message.chat.id]['Ф.И.О.'] = name
    bot.send_message(message.from_user.id, 'Введите номер телефона')
    bot.register_next_step_handler(message, get_telephone)


def get_telephone(message):  # функция ввода телефона
    """
    1. Функция принимает данные о телефоне пользователя, с последующей обработкой.
    2. Функция выполнит сбор и обработку данных о телефоне пользователя,
    с добавлением полученных данных в переменную dict_customer_data. 
    Отправит запрос на запуск следующей функции get_index(message) при помощи метода 
    bot.register_next_step_handler(message, get_name), для ввода индекса пользователя. 
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.from_user.id выводит сообщение пользователю в бот.
    4. функция ничего не возвращает
    """
    telephone = message.text
    dict_customer_data[message.chat.id]['телефон'] = telephone
    bot.send_message(message.from_user.id, 'Введите индекс проживания')
    bot.register_next_step_handler(message, get_index)


def get_index(message):  # функция ввода индекса проживания
    """
    1. Функция принимает данные о индексе проживания пользователя, с последующей обработкой.
    2. Функция выполнит сбор и обработку данных о индексе проживания пользователя,
    с добавлением полученных данных в переменную dict_customer_data. 
    Отправит запрос на запуск следующей функции get_address(message)при помощи метода 
    bot.register_next_step_handler(message, get_name), для ввода адреса проживания пользователя. 
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.from_user.id выводит сообщение пользователю в бот.
    4. функция ничего не возвращает
    """
    index = message.text
    dict_customer_data[message.chat.id]['индекс'] = index
    bot.send_message(message.from_user.id, 'Введите адрес проживания')
    bot.register_next_step_handler(message, get_address)


def get_address(message):  # функция записи введенных данных пользователя из бота в таблицу
    """
    1. Функция принимает данные о адресе проживания пользователя, с последующей обработкой.
    2. Функция выполнит сбор и обработку данных о адресе проживания пользователя,
    с добавлением полученных данных в переменную dict_customer_data. 
    После обработки всех полученных данных из функций(start_pro(message),get_name(message),get_telephone(message),
    get_index(message),get_address(message)) происходит вызов функции recording_data(user_name, dict_customer_data)-которая
    запишет полученные данные в гугл-таблицу(колонка "I"-данные получателя).
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.from_user.id выводит сообщение пользователю в бот.
    4. функция ничего не возвращает
    """
    address = message.text
    dict_customer_data[message.chat.id]['адрес'] = address
    user_name = message.from_user.username # автоопределение имени пользователя запросом в бот
    print(f'словарь с данными покупателя1{dict_customer_data}{user_name}')
    recording_data(user_name, dict_customer_data)
    get_transport_company(message)


def get_transport_company(message):  # функция фиксации данных о транспортной компании из бота в таблицу
    """
    1. Функция запускает блок кнопок о транспортной компании пользователя
    2. Функция выполнит запуск блока кнопок, для выбора пользователем транспортной компании. 
    Выбор пользователя будет обработан в функции all_messages(message) и отправлен на запись в таблицу при помощи функции
    recording_transport_company(user_name, transport_company).
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.from_user.id выводит сообщение пользователю в бот.
    4. функция ничего не возвращает
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    russian_post = types.KeyboardButton('Почта России')
    sdek = types.KeyboardButton('Сдек')
    boxbery = types.KeyboardButton('Боксбери')
    markup.add(russian_post)
    markup.add(sdek)
    markup.add(boxbery)
    bot.send_message(message.from_user.id, 'Выберите транспортную компанию', reply_markup=markup)


if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()
