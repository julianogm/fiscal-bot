import os

from dotenv import load_dotenv
from telegram import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from config import set_path
from constant import *
from modules.telegram_commands import *

load_dotenv()
set_path()

MODE = os.environ["MODE"]
TOKEN = os.environ["TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
PORT = int(os.environ["PORT"])


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_error_handler(errors)

    dp.add_handler(CallbackQueryHandler(callback))
    dp.add_handler(CommandHandler("deputados", deputies_command))
    dp.add_handler(CommandHandler("senadores", senators_command))
    dp.add_handler(CommandHandler("parlamento", parliament_command))
    dp.add_handler(CommandHandler("sobre", about_command))

    dp.add_handler(
        MessageHandler(
            Filters.regex(r"^(/deputado_[\d@" + updater.bot.username + "]+)$"),
            create_deputy_link,
        )
    )
    dp.add_handler(
        MessageHandler(
            Filters.regex(r"^(/senador_[\d@" + updater.bot.username + "]+)$"),
            create_senator_link,
        )
    )
    dp.add_handler(MessageHandler(Filters.command, help_command))
    dp.add_handler(MessageHandler(Filters.text, search_name))

    # Start the Bot
    if MODE == "webhook":
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=TOKEN,
            webhook_url=WEBHOOK_URL + TOKEN,
        )
    elif MODE == "polling":
        updater.start_polling()
    else:
        print("--- Invalid MODE value. Set MODE to 'polling' or 'webhook'. ---")
        exit()

    updater.idle()


if __name__ == "__main__":
    main()
