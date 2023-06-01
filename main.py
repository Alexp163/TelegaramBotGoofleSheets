import telebot
from telebot import types

from connect_table_4 import recording_data
from connect_table_4 import data_collection_function
from connect_table_4 import data_delivery_fuction
from connect_table_4 import recording_delivery_address
from connect_table_4 import recording_transport_company

TOKEN = '5602662399:AAHIHYWPme7pp62rtzWeqasf3gSXEbGQeGSy6rAg'
bot = telebot.TeleBot(TOKEN)
dict_index_address = {}
dict_customer_data = {}
transport_company = ''


@bot.message_handler(commands=['start'])
def start(message):  # запуск приветствия бота и первых кнопок
    user_name = message.from_user.username
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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    my_orders = types.KeyboardButton('Мои заказы')
    track_order = types.KeyboardButton('Отследить заказ')
    my_details_for_delivery = types.KeyboardButton('Мои данные для доставки')
    goto_main_menu = types.KeyboardButton('Вернуться в основное меню')
    markup.add(my_orders, track_order, my_details_for_delivery, goto_main_menu)
    bot.send_message(message.chat.id, f'Здравствуйте пользователь, {message.from_user.username}', reply_markup=markup)


def work_cabinet(message):  # функция работы в личном кабинете
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


@bot.message_handler(content_types=['text'])
def all_messages(message):  # алгоритм работы и взаимодействия бота с пользователем
    user_name = message.from_user.username
    data_delivery = data_delivery_fuction(user_name)
    data_collection = data_collection_function(user_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Главное меню':
        bot.send_message(message.chat.id, 'Вы вошли в главное меню', reply_markup=markup)
    elif message.text == 'Почта России':
        transport_company = message.text
        recording_transport_company(user_name, transport_company)
        print(f'Ваша транспортная компания {transport_company}')
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
    dict_index_address[message.chat.id] = {}
    bot.send_message(message.chat.id, 'Введите индекс и адрес отделения')
    bot.register_next_step_handler(message, entering_index_address)


def entering_index_address(message):  # функция ввода индекса и адреса
    user_name = message.from_user.username
    index_address = message.text
    dict_index_address[message.chat.id]['Индекс и адрес'] = index_address
    recording_delivery_address(user_name, dict_index_address)
    welcome_cabinet(message)


def welcome_cabinet(message):  # функция перехода кнопки в "личный кабинет"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    my_cabinet = types.KeyboardButton('Перейти в личный кабинет')
    markup.add(my_cabinet)
    bot.send_message(message.from_user.id, 'Спасибо, что ввели данные!', reply_markup=markup)
    enter_cabinet(message)


def start_pro(message):  # функция запуска ввода данных юзера
    dict_customer_data[message.chat.id] = {}
    bot.send_message(message.from_user.id, 'Введите своё Ф.И.О.')
    bot.register_next_step_handler(message, get_name)


def get_name(message):  # функция ввода ФИО
    name = message.text
    dict_customer_data[message.chat.id]['Ф.И.О.'] = name
    bot.send_message(message.from_user.id, 'Введите номер телефона')
    bot.register_next_step_handler(message, get_telephone)


def get_telephone(message):  # функция ввода телефона
    telephone = message.text
    dict_customer_data[message.chat.id]['телефон'] = telephone
    bot.send_message(message.from_user.id, 'Введите индекс проживания')
    bot.register_next_step_handler(message, get_index)


def get_index(message):  # функция ввода адреса проживания
    index = message.text
    dict_customer_data[message.chat.id]['индекс'] = index
    bot.send_message(message.from_user.id, 'Введите адрес проживания')
    bot.register_next_step_handler(message, get_address)


def get_address(message):  # функция записи введенных данных пользователя из бота в таблицу
    address = message.text
    dict_customer_data[message.chat.id]['адрес'] = address
    user_name = message.from_user.username
    print(f'словарь с данными покупателя1{dict_customer_data}{user_name}')
    recording_data(user_name, dict_customer_data)
    get_transport_company(message)


def get_transport_company(message):  # функция фиксации данных о транспортной компании из бота в таблицу
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
