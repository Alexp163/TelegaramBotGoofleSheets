import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES: [str] = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID: str = '1wgZRhyKNsZEXfm2fumy1xDeGi2fZXasq32--Fx0dzu_8'
# здесь вводиться ссылка на вашу гугл таблицу

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE: str = os.path.join(BASE_DIR, 'creds_130523.json')
# здесь вы получаете json-файл для доступа к гугл таблице

SAMPLE_RANGE_NAME: str = 'Sheet1'


def definition_credentials():
    """
    Реализует выдачу доступа к гугл-таблице

    Функция не принимает никаких аргументов.
    Обрабатывает данные, полученные из колонки 'С', в которой прописаны
    имена пользователей из телеграмма, которые вносит самостоятельно оператор
    работы с таблицей.

    Args:
    Аргументы отсутствуют.
    Returns:
    Функция возвращает: values-список имен пользователей, result- список с
    вложенным словарем, в котором сохранен список пользователей,
    credentials, servis, sheets - ссылка на адрес в оперативной памяти данных
    API таблицы
    """

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    sheets = service.spreadsheets()
    result = sheets.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                 range='Sheet1!C1:C20').execute()
    values = result.get('values', [])  # список пользователей в столбце "С"
    print(
        f'values - {values} \nresult - {result} \nsheets - {sheets}\n servis - '
        f'{service} \ncredentials - {credentials}')
    return values, service, sheets, result, credentials


def recording_transport_company(user_name: str, transport_company: str):
    """
    Реализует запись данных о транспортной компании в таблицу.

    Функция, которая принимает на вход два аргумента user_name и
    transport_company, которые будут получены от пользователя
    телеграм-бота. user_name будет идентифицирован перебором через цикл for
    данных из колонки 'C' подключенной гугл-таблицы.
    user_name пользователя будет автоматически распознан телеграмм-ботом,
    user_name из колонки 'C' будет введено оператором таблицы.
    Одновременно с работой цикла for включиться счетчик, который зафиксирует
    номер колонки в которой будет находиться необходимый нам user_name.
    Возможно один и тот же user_name будет встречаться несколько раз, если
    обращение за товаром к оператору таблицу(заказ товара)
    было неоднократным. После идентифи кации user_name и определения номеров
    строк в колонку 'J'(транспортная компания) вносятся данные
    о, выбранной пользователем, транспортной компании.

    Args:
    user_name: str - Имя пользователя телеграмм, получается в каждой функции
    файла main.py
    transport_company: str - транспортная компания, которую выбрал
    пользователь(из функции get_transport_company(message) файл main.py)
    Returns:
    Функция ничего не возвращает
    """
    values, service, sheets, result, credentials = definition_credentials()
    count = 0
    for i in values:
        count += 1
        if i[0] == user_name:
            range_ = f'Sheet1!J{count}'
            array = {'values': [[transport_company]]}
            service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_,
                valueInputOption='USER_ENTERED',
                body=array).execute()


def recording_data(user_name: str, dict_customer_data: dict):
    """
    Реализует запись данных о пользователе.

    Функция, которая принимает на вход два аргумента user_name и
    dict_customer_data, которые будут получены от пользователя
    телеграм-бота. user_name будет идентифицирован перебором через цикл for
    данных из колонки 'C' подключенной гугл-таблицы.
    user_name пользователя будет автоматически распознан телеграмм-ботом,
    user_name из колонки 'C' будет введено оператором таблицы.
    Одновременно с работой цикла for включиться счетчик, который зафиксирует
    номер колонки в которой будет находиться необходимый нам user_name.
    Возможно один и тот же user_name будет встречаться несколько раз, если
    обращение за товаром к оператору таблицу(заказ товара)
    было неоднократным.
    Для лучшей визуализации данных о пользователе через цикл for перебираем
    словарь(i, j)и перебираем их еще одним циклом и полученные key и keys,
    добавляем переменную result. Полученные данные в переменной result добавляем
    в переменную str_data_user, данные из которой,
    после идентификации user_name и определения номеров строк в колонке
    'I'(Данные получателя), вносим данные о покупателе(ФИО, телефон, индекс,
    адрес).

    Args:
    user_name: str - Имя пользователя телеграмм, получается в каждой функции
    файла main.py
    dict_customer_data: dict - данные, которые пользователь ввел о себе и
    добавленные в словарь(из функции start_pro(message), get_name(message),
    get_telephone(message), get_index(message) из файла main.py.
    Returns:
    Функция ничего не возвращает
    """
    values, service, sheets, result, credentials = definition_credentials()
    for i, j in dict_customer_data.items(): pass
    str_data_user = ''
    for key, keys in j.items():
        result = f' {key} - {keys}\n'
        str_data_user += result
    count = 0
    for i in values:
        count += 1
        if i[0] == user_name:
            range_ = f'Sheet1!I{count}'
            array = {'values': [[str_data_user]]}
            service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_,
                valueInputOption='USER_ENTERED',
                body=array).execute()


def recording_delivery_address(user_name: str, dict_index_address: dict):
    """
    Реализует запись данных об адрессе доставки товара.

    Функция, которая принимает на вход два аргумента user_name и
    dict_index_address, которые будут получены от пользователя
    телеграм-бота. user_name будет идентифицирован перебором через цикл for
    данных из колонки 'C' подключенной гугл-таблицы.
    user_name пользователя будет автоматически распознан телеграмм-ботом,
     user_name из колонки 'C' будет введено оператором таблицы.
    Одновременно с работой цикла for включиться счетчик, который зафиксирует
    номер колонки в которой будет находиться необходимый нам user_name.
    Возможно один и тот же user_name будет встречаться несколько раз, если
    обращение за товаром к оператору таблицу(заказ товара)
    было неоднократным.
    Для лучшей визуализации данных о пользователе через цикл for перебираем
    словарь(i, j)и перебираем их еще одним циклом и полученные key и keys,
    добавляем переменную result. Полученные данные в переменной result добавляем
    в переменную str_data_user, данные из которой,
    после идентификации user_name и определения номеров строк в колонке
    'K'(Адрес отделения доставки), вносим адрес доставки(индекс и адрес доставки).

    Args:
    user_name: str - Имя пользователя телеграмм, получается в каждой функции
    файла main.py
    dict_index_address: dict - данные, которые пользователь ввел о себе и
    добавленные в словарь(из функции get_index_address(message),
    entering_index_address(message) из файла main.py)
    Returns:
    Функция ничего не возвращает
    """
    values, service, sheets, result, credentials = definition_credentials()
    for i, j in dict_index_address.items(): pass
    str_index_address = ''
    for key, keys in j.items():
        result = f' {key} - {keys}\n'
        str_index_address += result
    count = 0
    for i in values:
        count += 1
        if i[0] == user_name:
            range_ = f'Sheet1!K{count}'
            array = {'values': [[str_index_address]]}
            service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_,
                valueInputOption='USER_ENTERED',
                body=array).execute()


def data_collection_function(user_name: str):
    """
    Реализует вывод данных о заказе в бот.

    Функция, которая принимает на вход один аргумента user_name, которые будут
    получены от пользователя
    телеграм-бота. user_name будет идентифицирован перебором через цикл for
    данных из колонки 'C' подключенной гугл-таблицы.
    user_name пользователя будет автоматически распознан телеграмм-ботом,
    user_name из колонки 'C' будет введено оператором таблицы.
    Одновременно с работой цикла for включиться счетчик, который зафиксирует
    номер колонки в которой будет находиться необходимый нам user_name.
    Возможно один и тот же user_name будет встречаться несколько раз, если
    обращение за товаром к оператору таблицу(заказ товара)
    было неоднократным.
    В результате будет отфильтруем список из целого ряда данных, в котором
    расположен необходимый нам user_name, из этого
    списка(по индексу) мы выберем необходимые нам колонки с данными:
    'C'- покупатель, 'L' - номер заказа, 'D' -товар, 'E' - цена, 'G' - стоимость
    доставки,
    'M' - статус заказа.
    И при помощи функции entering_index_address(message)(расположена в main.py)
    выведем данные в бот пользователю.

    Args:
    user_name: str - Имя пользователя телеграмм, получается в каждой функции
    файла main.py
    Returns:
    Функция вернет значение report1, в которой у нас будет отфильтрованный
    список с данными о доставке из таблицы
    """
    values, service, sheets, result, credentials = definition_credentials()
    report1 = ""
    count = 0
    count_2 = 0
    for i in values:
        count += 1
        if i[0] == user_name:
            count_2 += 1
            result = sheets.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                         range=f'Sheet1!D{count}:M{count}').execute()
            values_ = result.get('values')
            report1 += f'Покупатель - {user_name} ,\nзаказ номер - {values_[0][8]} ' \
                       f'\nваш товар - {values_[0][0]}\nстоимостью - {values_[0][1]}' \
                       f'\nстоимость доставки - {values_[0][3]}\nстатус - ' \
                       f'{values_[0][9]}\n\n'

    return report1


def data_delivery_fuction(user_name: str):
    """
    Реализует вывод данных о заказчике в бот.

    Функция, которая принимает на вход один аргумента user_name, которые будут
    получены от пользователя
    телеграм-бота. user_name будет идентифицирован перебором через цикл for
    данных из колонки 'C' подключенной гугл-таблицы.
    user_name пользователя будет автоматически распознан телеграмм-ботом,
    user_name из колонки 'C' будет введено оператором таблицы.
    Одновременно с работой цикла for включиться счетчик, который зафиксирует
    номер колонки в которой будет находиться необходимый нам user_name.
    Возможно один и тот же user_name будет встречаться несколько раз, если
    обращение за товаром к оператору таблицу(заказ товара)
    было неоднократным.
    В результате будет отфильтруем список из целого ряда данных, в котором
    расположен необходимый нам user_name, из этого
    списка(по индексу) мы выберем необходимые нам колонки с данными:
    'C'- покупатель, 'J' - транспортная компания, 'K' -адрес отделения доставки.

    Args:
    user_name: str - Имя пользователя телеграмм, получается в каждой функции
    файла main.py
    Returns:
    Функция вернет значение report2, в которой у нас будет отфильтрованный
    список с данными о пользователе из таблицы
    """
    values, service, sheets, result, credentials = definition_credentials()
    report2 = ""
    count = 0
    for i in values:
        count += 1
        if i[0] == user_name:
            result = sheets.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                         range=f'Sheet1!I{count}:K{count}').execute()
            values_ = result.get('values')
    report2 += f'{values_[0][0]}\nтранспортная компания - {values_[0][1]}\n' \
               f'Адрес отделения - {values_[0][2]}\n\n' \
               f'Если вы хотите поменять свои данные, напишите администратору' \
               f'\n\n\n'

    return report2
