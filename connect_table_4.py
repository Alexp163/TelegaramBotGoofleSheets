import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from  id_sheet import id_table

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = id_table # здесь вводиться ссылка на вашу гугл таблицу
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'creds_130523.json') # здесь вы получаете json-файл для доступа к гугл таблице
SAMPLE_RANGE_NAME = 'Sheet1'

def definition_credentials(): # даёт права доступа для работы с гугл-таблицей
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    sheets = service.spreadsheets()
    result = sheets.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Sheet1!C1:C20').execute()
    values = result.get('values', []) # список пользователей в столбце "С"
    return values, service, sheets, result, credentials



def recording_transport_company(user_name, transport_company): # запись названия транспортной компании в таблицу
    values, service, sheets, result, credentials = definition_credentials()
    count = 0
    for i in values:
        count += 1
        if i[0] == user_name:
            range_ = f'Sheet1!J{count}'
            array = {'values': [[transport_company]]}
            service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_,
                                                   valueInputOption='USER_ENTERED',
                                                   body=array).execute()


def recording_data(user_name, dict_customer_data):  # запись данных о покупателе(фио, адрес...)
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
            service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_,
                                                   valueInputOption='USER_ENTERED',
                                                   body=array).execute()


def recording_delivery_address(user_name, dict_index_address):  # запись адреса доставки в таблицу
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
            service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_,
                                                   valueInputOption='USER_ENTERED',
                                                   body=array).execute()


def data_collection_function(user_name):  # выводит (user_name, товар, стоимость, статус заказа)в бот
    values, service, sheets, result, credentials = definition_credentials()
    report1 = ""
    count = 0
    count_2 = 0
    for i in values:
        count += 1
        if i[0] == user_name:
            count_2 += 1
            result = sheets.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Sheet1!D{count}:M{count}').execute()
            values_ = result.get('values')
            report1 += f'Покупатель - {user_name} ,\nзаказ номер - {values_[0][8]} \nваш товар - {values_[0][0]}\nстоимостью - {values_[0][1]}\nстоимость доставки - {values_[0][3]}\nстатус - {values_[0][9]}\n\n'

    return report1


def data_delivery_fuction(user_name):  # выводит данные доставки в бот
    values, service, sheets, result, credentials = definition_credentials()
    report2 = ""
    count = 0
    for i in values:
        count += 1
        if i[0] == user_name:
            result = sheets.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Sheet1!I{count}:K{count}').execute()
            values_ = result.get('values')
    report2 += f'{values_[0][0]}\nтранспортная компания - {values_[0][1]}\nАдрес отделения - {values_[0][2]}\n\nЕсли вы хотите поменять свои данные, напишите администратору\n\n\n'

    return report2


