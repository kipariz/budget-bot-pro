import logging
import os
from configs.config import ENV

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from parse.processing import parse_input
from sheets_api import finance
from sheets_api.api import update_or_write


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет!\n Для добавления информации в таблицу напиши сообщение в формате:\n'
                              'название покупки сумма категория [опционально].\n'
                              'Нельзя использовать числа (кроме суммы). \n'
                              'детальнее - /help')


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('просто число для расходов\n'
                              '+ для доходов\n'
                              '? для планируемых доходов.расходов\n\n'
                              'Например:\n'
                              '"мак 100 eat outside" - добаивт расход "мак" в категорию "eat outside"\n'
                              '"зарплата +1000 - добаивт доход "зарплата" в общую категорию \n'
                              '"зубы ?1000 здоровье - добаивт потенциальный расход "зубы" в категорию "здоровье"\n')


def parse_operation(update: Update, context: CallbackContext) -> None:
    data = update.message.text
    logger.info(f"data from user {data}")

    try:
        parsed = parse_input(data)
        logger.info(f"parsed data {parsed}")
        data = []

        if 'expense' in parsed['source']:
            finance_type = finance.expenses
        else:
            finance_type = finance.income

        amount = int(parsed['amount'][0])
        if 'planning' in parsed['source']:
            data.extend([parsed['name'], parsed['category'], "", amount])
        else:
            data.extend([parsed['name'], parsed['category'], amount])

        update_or_write(finance_type, [data])
        update.message.reply_text(str(parsed))

    except:
        update.message.reply_text("Проверьте формат вводимых данных")


def main(TOKEN):
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, parse_operation))

    if ENV == 'HEROKU':
        NAME = os.environ.get("HEROKU_APP_NAME")
        TOKEN = os.environ["TOKEN"]

        # Port is given by Heroku
        PORT = int(os.environ.get("PORT", "8443"))
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))

    elif ENV == 'DEV':
        updater.start_polling()

    updater.idle()



