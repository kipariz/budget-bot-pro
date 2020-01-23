from __future__ import print_function
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence)
from telegram import (ReplyKeyboardMarkup, ParseMode)
import logging
import pickle
import time
import re

from style import updateNewSheetStyle
from config import *
from spredsheetAPI import *


service = None

#____ Bot ____#


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_AMOUNT, TYPING_CATEGORY, TYPING_NEW_CATEGORY, TYPING_NEW_TABLE, MAINMENU = range(6)

reply_keyboard = [['Добавить расходы'], [
    'Добавить доход'], ['Добавить новую категорию']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, 
                 text="Привет, *BudgetBotPro* создан для того чтобы облегчить тебе ведение своего собственного бюджета. \n\n" +
                "Если ты используешь его в первый раз, то советуем тебе начать с регистрации своей новой таблицы, куда будут записываться все твои расходы, доходы и остальная информация. \n\n" +
                "Просто нажми на /newtable и мы расскажем что нужно делать.", 
                 parse_mode=ParseMode.MARKDOWN,
                 reply_markup=markup)
                 
    return CHOOSING

SHEET_NAME = time.strftime("%m.%y", time.localtime())

def initSheet(update, context, spreadsheetId):
    update.message.reply_text("Начинаем настройку новой таблицы")

    mergeCells(getSheetId(SHEET_NAME, spreadsheetId), 0, 1, 1, 9, spreadsheetId)
    mergeCells(getSheetId(SHEET_NAME, spreadsheetId), 1, 2, 1, 5, spreadsheetId)
    mergeCells(getSheetId(SHEET_NAME, spreadsheetId), 1, 2, 5, 9, spreadsheetId)
    mergeCells(getSheetId(SHEET_NAME, spreadsheetId), 2, 3, 1, 3, spreadsheetId)
    mergeCells(getSheetId(SHEET_NAME, spreadsheetId), 2, 3, 3, 5, spreadsheetId)
    mergeCells(getSheetId(SHEET_NAME, spreadsheetId), 2, 3, 5, 7, spreadsheetId)
    mergeCells(getSheetId(SHEET_NAME, spreadsheetId), 2, 3, 7, 9, spreadsheetId)

    mergeCells(getSheetId(SHEET_NAME, spreadsheetId), 4, 5, 9, 11, spreadsheetId)

    current_month = time.strftime("%B", time.localtime())
    updateCell(current_month, f'{SHEET_NAME}!B1', spreadsheetId)

    update.message.reply_text("Уже скоро...")

    updateCell("ИТОГИ МЕСЯЦА", f'{SHEET_NAME}!J5', spreadsheetId)
    updateCell("ДОХОД", f'{SHEET_NAME}!J6', spreadsheetId)
    updateCell("РАСХОДЫ", f'{SHEET_NAME}!J7', spreadsheetId)
    updateCell("БАЛАНС", f'{SHEET_NAME}!J8', spreadsheetId)

    updateCell("=SUM(B5:B100)+SUM(D5:D100)", f'{SHEET_NAME}!K6', spreadsheetId)
    updateCell("=SUM(F5:F100)+SUM(H5:H100)", f'{SHEET_NAME}!K7', spreadsheetId)
    updateCell("=K6-K7", f'{SHEET_NAME}!K8', spreadsheetId)

    update.message.reply_text("Почти...")
    
    updateCell("ДОХОДЫ", f'{SHEET_NAME}!B2', spreadsheetId)
    updateCell("РАСХОДЫ", f'{SHEET_NAME}!F2', spreadsheetId)
    updateCell("Категории", f'{SHEET_NAME}!B3', spreadsheetId)
    updateCell("Уникальные", f'{SHEET_NAME}!D3', spreadsheetId)
    updateCell("Категории", f'{SHEET_NAME}!F3', spreadsheetId)
    updateCell("Покупки/Услуги", f'{SHEET_NAME}!H3', spreadsheetId)
    updateCell("Сумма", f'{SHEET_NAME}!B4', spreadsheetId)
    updateCell("Откуда", f'{SHEET_NAME}!C4', spreadsheetId)
    updateCell("Сумма", f'{SHEET_NAME}!D4', spreadsheetId)
    updateCell("Откуда", f'{SHEET_NAME}!E4', spreadsheetId)
    updateCell("Сумма", f'{SHEET_NAME}!F4', spreadsheetId)
    updateCell("Куда", f'{SHEET_NAME}!G4', spreadsheetId)
    updateCell("Сумма", f'{SHEET_NAME}!H4', spreadsheetId)
    updateCell("Куда", f'{SHEET_NAME}!I4', spreadsheetId)

    updateNewSheetStyle(getSheetId(SHEET_NAME, spreadsheetId), service=service,
                        spreadsheetId=spreadsheetId)

    update.message.reply_text("Готово")


def get_user_categories(name_column, spreadsheetId):
    range_name = f'{SHEET_NAME}!{name_column}{VALUES_START_ROW}:{name_column}100'
    respond = getFormulaData(range_name, spreadsheetId)

    return respond


def add_money(update, context):
    text = update.message.text
    user_data = context.user_data
    user_data['choice'] = text

    if(text == 'Добавить расходы'):
        update.message.reply_text(
            'Пожалуйста, введите сумму которую вы потратили:')
        return TYPING_AMOUNT
    elif(text == 'Добавить доход'):
        update.message.reply_text(
            'Пожалуйста, введите сумму которую вы получили:')
        return TYPING_AMOUNT
    elif(text == 'Добавить уникальную покупку/услугу'):
        update.message.reply_text(
            'Пожалуйста, введите название покупки/услуги:')
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

    amount = amount.replace('.', ',')
    amount = re.sub("[^0-9,]", "", amount)

    user_data['amount'] = amount

    if (user_data['choice'] == 'Добавить расходы'):
        user_categories = get_user_categories('G', user_data['tableid'])
        reply_keyboard = [['Добавить уникальную покупку/услугу']]
    elif (user_data['choice'] == 'Добавить доход'):
        user_categories = get_user_categories('C', user_data['tableid'])
        reply_keyboard = [['Добавить уникальный доход']]

    if (not user_categories):
        pass
    elif (len(user_categories) < 4):
        for i in user_categories:
            reply_keyboard.append([str(i)])
    else:
        for i in range(len(user_categories)-1):
            if (i % 2 == 0):
                reply_keyboard.append(
                    [str(user_categories[i]), str(user_categories[i+1])])
            elif (i == (len(user_categories)-2)):
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
        user_categories = get_user_categories(categories_column, user_data['tableid'])
    elif(user_data['choice'] == 'Добавить доход'):
        categories_column = 'C'
        values_column = 'B'
        user_categories = get_user_categories(categories_column, user_data['tableid'])

    if (user_data['choice'] == 'Добавить уникальную покупку/услугу' or user_data['choice'] == 'Добавить уникальный доход'):
        createCellsCouple(SHEET_NAME, user_data['category'], user_data['amount'], categories_column, values_column, user_data['tableid'])
        update.message.reply_text("Добавлено {} на сумму {}.".format(user_data['category'], user_data['amount']),
                                  reply_markup=markup)

    elif (category in user_categories):
        for i in range(len(user_categories)):
            if (category == str(user_categories[i])):
                range_name = f'{SHEET_NAME}!{values_column}{i+5}'
                respond = getFormulaData(range_name, user_data['tableid'])

                if (respond == []):
                    updateCell('=' + user_data['amount'], f'{SHEET_NAME}!{values_column}{i+VALUES_START_ROW}', user_data['tableid'])
                else:
                    updateCell(respond[0] + '+' + user_data['amount'],
                               f'{SHEET_NAME}!{values_column}{i+VALUES_START_ROW}', user_data['tableid'])

                respond = getValueData(range_name, user_data['tableid'])
                update.message.reply_text("Добавлено {} в категорию {}.\nВсего {} потрачено на {}".format(user_data['amount'], user_data['category'], respond[0], user_data['category']),
                                          reply_markup=markup)

    return CHOOSING

def add_new_category(update, context):
    text = update.message.text
    user_data = context.user_data
    user_data['choice'] = text

    reply_keyboard = [['Добавить категорию расходов'],
                      ['Добавить категорию доходов']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    if(text == 'Добавить новую категорию'):
        update.message.reply_text(
            "Какую категорию вы желаете добавить?", reply_markup=markup)
        return CHOOSING
    elif(text == 'Добавить категорию расходов' or text == 'Добавить категорию доходов'):
        update.message.reply_text(
            'Пожалуйста, введите название новой категории:')
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

    respond = getFormulaData(range_name, user_data['tableid'])
    current_row_number = VALUES_START_ROW+len(respond)

    updateCell(category, f'{SHEET_NAME}!{category_column}{current_row_number}', user_data['tableid'])

    update.message.reply_text("Добавлено новая категория {} - {}".format(reply_string, user_data['category']),
                              reply_markup=markup)
    return CHOOSING


def newtable(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, 
                 text="Для того чтобы зарегистрировать новую таблицу: \n\n" +
                 "*1.* Пройди по ссылке *sheet.new* \n" +
                 "*2.* Скопируй ссылку из адресной строки своего браузера\n" +
                 "*3.* Отправь ссылку на таблицу нашему боту\n" +
                 "*4.* Готово! \n\n" +
                 "Ждём от тебя *ссылку*...", 
                 parse_mode=ParseMode.MARKDOWN)

    context.bot.send_photo(chat_id=chat_id, photo=open('img/addressbar.png', 'rb'))

    return CHOOSING

def add_new_table(update, context):
    text = update.message.text
    user_data = context.user_data
    text = re.search(r'spreadsheets/d/(.*?)/', text).group(1)
    user_data['tableid'] = text

    if(user_data['tableid']):
        currentMonth = time.strftime("%m.%y", time.localtime())
        renameFirstSheet(user_data['tableid'], currentMonth)

        initSheet(update, context, user_data['tableid'])

        update.message.reply_text("Таблица успешно сохранена!\n")

    return MAINMENU


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text("Произошла какая-то ошибка, попробуйте ещё раз", reply_markup=markup)

    return CHOOSING

def runbot():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    my_persistence = PicklePersistence(filename='data.pickle')

    updater = Updater(TOKEN, persistence=my_persistence, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CATEGORY and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Добавить расходы|Добавить доход|Добавить уникальную покупку/услугу|Добавить уникальный доход)$'),
                                      add_money),
                       MessageHandler(Filters.regex('^(Добавить новую категорию|Добавить категорию расходов|Добавить категорию доходов)$'),
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

            TYPING_NEW_TABLE: [MessageHandler(Filters.text,
                                                 add_new_table)
                                  ],
        },
        fallbacks=[]

    )

    new_sheet_handler = ConversationHandler(
        entry_points=[CommandHandler('newtable', newtable)],

        states={
            CHOOSING: [
                       MessageHandler(Filters.text,
                                                 add_new_table)
                       ],
            MAINMENU: [conv_handler]
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(new_sheet_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    
    service = initCreds()
    
    
    runbot()
