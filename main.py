from bot.bot import main
import os
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ENV = os.getenv("ENV")

    main(BOT_TOKEN, ENV)
