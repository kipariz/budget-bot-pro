from __future__ import print_function
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from style import updateNewSheetStyle
from config import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.

VALUES_START_ROW = 5

service = None

def initCreds():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    global service
    service = build('sheets', 'v4', credentials=creds)
    
def mergeCells(sheetId,startRowIndex,endRowIndex,startColumnIndex,endColumnIndex):
    requests = [
        {
        "mergeCells": {
            "range": {
            "sheetId": sheetId,
            "startRowIndex": startRowIndex,
            "endRowIndex": endRowIndex,
            "startColumnIndex": startColumnIndex,
            "endColumnIndex": endColumnIndex
            },
            "mergeType": "MERGE_ALL"
            }
        }
    ]

    body = {
        'requests': requests
    }

    request = service.spreadsheets().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body)
    response = request.execute()

    

def updateCell(values, range_name):
    values = [
        [
            f"{values}"
        ],
    ]

    body = {
        'values': values
    }
    
    sheet = service.spreadsheets()

    result = sheet.values().update(valueInputOption='USER_ENTERED', spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                       range=range_name, body=body).execute()


def getFormulaData(range_name):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=range_name, valueRenderOption='FORMULA').execute()
    values = result.get('values', [])

    result = []
    if not values:
        result = []
    else:
        
        for row in values:
            if (row != []):
                result.append(str(row[0]))
            else:
                break 

    return result

def getValueData(range_name):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=range_name).execute()
    values = result.get('values', [])

    result = []
    if not values:
        result = ['']
    else:
        for row in values:
            result.append(row[0])

    return result


def createCellsCouple(current_sheet, name_data, value_data, name_column, value_column):
    """found row id for new values"""
    range_name = f'{current_sheet}!{name_column}{VALUES_START_ROW}:{name_column}100'

    respond = getFormulaData(range_name)
    
    current_row_number = VALUES_START_ROW+len(respond)

    updateCell(value_data, f'{current_sheet}!{value_column}{current_row_number}')
    
    updateCell(name_data, f'{current_sheet}!{name_column}{current_row_number}')
    


def getSheetId(sheet_name):
    spreadsheet = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    sheet_id = None
    for _sheet in spreadsheet['sheets']:
        if _sheet['properties']['title'] == sheet_name:
            sheet_id = _sheet['properties']['sheetId']

    return sheet_id

SHEET_NAME = 'TEST'
def initSheet():
    mergeCells(getSheetId(SHEET_NAME),0,1,1,9)
    mergeCells(getSheetId(SHEET_NAME),1,2,1,5)
    mergeCells(getSheetId(SHEET_NAME),1,2,5,9)
    mergeCells(getSheetId(SHEET_NAME),2,3,1,3)
    mergeCells(getSheetId(SHEET_NAME),2,3,3,5)
    mergeCells(getSheetId(SHEET_NAME),2,3,5,7)
    mergeCells(getSheetId(SHEET_NAME),2,3,7,9)

    mergeCells(getSheetId(SHEET_NAME),4,5,9,11)

    mydate = datetime.datetime.now()
    current_month = mydate.strftime("%B")
    updateCell(current_month, f'{SHEET_NAME}!B1')
    
    updateCell("ИТОГИ МЕСЯЦА", f'{SHEET_NAME}!J5')
    updateCell("ДОХОД", f'{SHEET_NAME}!J6')
    updateCell("РАСХОДЫ", f'{SHEET_NAME}!J7')
    updateCell("БАЛАНС", f'{SHEET_NAME}!J8')
    
    updateCell("=SUM(B5:B100)+SUM(D5:D100)", f'{SHEET_NAME}!K6')
    updateCell("=SUM(F5:F100)+SUM(H5:H100)", f'{SHEET_NAME}!K7')
    updateCell("=K6-K7", f'{SHEET_NAME}!K8')

    updateCell("ДОХОДЫ", f'{SHEET_NAME}!B2')
    updateCell("РАСХОДЫ", f'{SHEET_NAME}!F2')
    updateCell("Категории", f'{SHEET_NAME}!B3')
    updateCell("Уникальные", f'{SHEET_NAME}!D3')
    updateCell("Категории", f'{SHEET_NAME}!F3')
    updateCell("Покупки/Услуги", f'{SHEET_NAME}!H3')
    updateCell("Сумма", f'{SHEET_NAME}!B4')
    updateCell("Откуда", f'{SHEET_NAME}!C4')
    updateCell("Сумма", f'{SHEET_NAME}!D4')
    updateCell("Откуда", f'{SHEET_NAME}!E4')
    updateCell("Сумма", f'{SHEET_NAME}!F4')
    updateCell("Куда", f'{SHEET_NAME}!G4')
    updateCell("Сумма", f'{SHEET_NAME}!H4')
    updateCell("Куда", f'{SHEET_NAME}!I4')
    
    updateNewSheetStyle(getSheetId(SHEET_NAME), service=service, SAMPLE_SPREADSHEET_ID=SAMPLE_SPREADSHEET_ID)








#____ Bot ____#

import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_AMOUNT, TYPING_CATEGORY, TYPING_NEW_CATEGORY = range(4)

reply_keyboard = [['Добавить расходы'],['Добавить доход'],['Добавить новую категорию']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(update, context):
    update.message.reply_text(
        "Hi! Bot has been started",
        reply_markup=markup)

    return CHOOSING
    
def get_user_categories(name_column,):
    range_name = f'{SHEET_NAME}!{name_column}{VALUES_START_ROW}:{name_column}100'
    respond = getFormulaData(range_name)
    
    return respond


def add_money(update, context):
    text = update.message.text
    user_data = context.user_data
    user_data['choice'] = text
    
    if(text == 'Добавить расходы'):
        update.message.reply_text('Пожалуйста, введите сумму которую вы потратили:')
        return TYPING_AMOUNT
    elif(text == 'Добавить доход'):
        update.message.reply_text('Пожалуйста, введите сумму которую вы получили:')
        return TYPING_AMOUNT
    elif(text == 'Добавить уникальную покупку/услугу'):
        update.message.reply_text('Пожалуйста, введите название покупки/услуги:')
        return TYPING_CATEGORY
    elif(text == 'Добавить уникальный доход'):
        update.message.reply_text('Пожалуйста, введите источник дохода:')
        return TYPING_CATEGORY
    else:
        update.message.reply_text('Произошла ошибка.')
        return CHOOSING    

def received_amount(update, context):
    user_data = context.user_data
    amount = update.message.text

    amount = amount.replace('.',',')
    import re
    amount = re.sub("[^0-9,]", "", amount)

    user_data['amount'] = amount


    if (user_data['choice'] == 'Добавить расходы'):
        user_categories = get_user_categories('G')
        reply_keyboard = [['Добавить уникальную покупку/услугу']]
    elif (user_data['choice'] == 'Добавить доход'):
        user_categories = get_user_categories('C')
        reply_keyboard = [['Добавить уникальный доход']] 

    if (not user_categories):
        pass
    elif (len(user_categories)<4):
        for i in user_categories:
            reply_keyboard.append([str(i)])
    else:
        for i in range(len(user_categories)-1):
            if (i%2==0):
                reply_keyboard.append([str(user_categories[i]), str(user_categories[i+1])])  
            elif (i==(len(user_categories)-2)):
                reply_keyboard.append([str(user_categories[i+1])])  
        
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    update.message.reply_text("Введённая сумма - {}.\n"
                              "Выберите желаемую категорию.".format(amount),
                              reply_markup=markup)

    return CHOOSING
    
def received_category(update, context):
    user_data = context.user_data
    category = str(update.message.text)
    user_data['category'] = category

    if(user_data['choice'] == 'Добавить уникальную покупку/услугу'):
        categories_column = 'I'
        values_column = 'H'
    elif(user_data['choice'] == 'Добавить уникальный доход'):
        categories_column = 'E'
        values_column = 'D'
    elif(user_data['choice'] == 'Добавить расходы'):
        categories_column = 'G'
        values_column = 'F'
        user_categories = get_user_categories(categories_column)
    elif(user_data['choice'] == 'Добавить доход'):
        categories_column = 'C'
        values_column = 'B'
        user_categories = get_user_categories(categories_column)
 
                              
    if (user_data['choice'] == 'Добавить уникальную покупку/услугу' or user_data['choice'] == 'Добавить уникальный доход'):
        createCellsCouple(SHEET_NAME, user_data['category'], user_data['amount'], categories_column, values_column)
        update.message.reply_text("Добавлено {} на сумму {}.".format(user_data['category'],user_data['amount']),
                              reply_markup=markup)
    
    elif (category in user_categories):
        for i in range(len(user_categories)):
            if (category == str(user_categories[i])):
                range_name = f'{SHEET_NAME}!{values_column}{i+5}'
                respond = getFormulaData(range_name)

                if (respond == []):
                    updateCell('=' + user_data['amount'], f'{SHEET_NAME}!{values_column}{i+5}')
                else:
                    updateCell(respond[0] + '+' + user_data['amount'], f'{SHEET_NAME}!{values_column}{i+5}')

                respond = getValueData(range_name)
                update.message.reply_text("Добавлено {} в категорию {}.\nВсего {} потрачено на {}".format(user_data['amount'],user_data['category'],respond[0],user_data['category']),
                              reply_markup=markup)

    return CHOOSING


def add_new_category(update, context):
    text = update.message.text
    user_data = context.user_data
    user_data['choice'] = text
        
    reply_keyboard = [['Добавить категорию расходов'],['Добавить категорию доходов']]      
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    if(text == 'Добавить новую категорию'):
        update.message.reply_text("Какую категорию вы желаете добавить?", reply_markup=markup)
        return CHOOSING
    elif(text == 'Добавить категорию расходов' or text == 'Добавить категорию доходов'):
        update.message.reply_text('Пожалуйста, введите название новой категории:')
        return TYPING_NEW_CATEGORY
    else:
        update.message.reply_text('Произошла ошибка.')
        return CHOOSING    

def received_new_category(update, context):
    user_data = context.user_data
    category = update.message.text
    user_data['category'] = category

    if (user_data['choice'] == 'Добавить категорию расходов'):
        category_column = 'G'
        reply_string = 'расходов'
    elif (user_data['choice'] == 'Добавить категорию доходов'):
        category_column = 'C'
        reply_string = 'доходов'
        
    range_name = f'{SHEET_NAME}!{category_column}{VALUES_START_ROW}:{category_column}100'

    respond = getFormulaData(range_name)
    current_row_number = VALUES_START_ROW+len(respond)

    updateCell(category, f'{SHEET_NAME}!{category_column}{current_row_number}')

    update.message.reply_text("Добавлено новая категория {} - {}".format(reply_string, user_data['category']),
                              reply_markup=markup)
    return CHOOSING   
        


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END

def runbot():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CATEGORY and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Добавить расходы|Добавить доход|Добавить уникальную покупку/услугу|Добавить уникальный доход)$'),
                                      add_money),
                        MessageHandler(Filters.regex('^(Добавить новую категорию)$'),
                                      add_new_category),
                        MessageHandler(Filters.regex('^(Добавить категорию расходов|Добавить категорию доходов)$'),
                                      add_new_category),
                        MessageHandler(Filters.text,
                                          received_category)
                       ],

            TYPING_AMOUNT: [MessageHandler(Filters.text,
                                          received_amount),
                           ],
                           
            TYPING_CATEGORY: [MessageHandler(Filters.text,
                                          received_category)
                            ],

            TYPING_NEW_CATEGORY: [MessageHandler(Filters.text,
                                          received_new_category)
                            ],
        },
        fallbacks=[]

    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()




if __name__ == '__main__':
    initCreds()
    initSheet()
    runbot()

    #createCellsCouple("TEST", "gay", 777, "C", "B")
    #createCellsCouple("TEST", "gey", 228, "C", "B")
    
 