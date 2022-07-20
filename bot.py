# encoding: utf-8

import os
from apis.camara import *
from tlgrm.commands import *
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

PORT = int(os.environ['PORT'])
TOKEN = os.environ['TOKEN']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def inicio(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def ajuda(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')    
    
def botoes_deputados():
    keyboard = [
        [InlineKeyboardButton("Por Partido", callback_data='partido'),
         InlineKeyboardButton("Por Estado", callback_data='estado'),],
    ]
    return InlineKeyboardMarkup(keyboard)

def deputados(update, context: CallbackContext):

    ld = por_partido("PT")
    ld_nomes = nomes_deputados(ld)
    update.message.reply_text('Escolha um filtro:',
                              reply_markup = buttons_deputados())
    
def deputados_callback(update, context):
    query = update.callback_query
    print('UPDATE #####:', update, ' #####\n')
    print('QUERY #####:', query, '#####\n')
    if query.data == "partido":
        query.edit_message_text(text = "Escolha um partido:", reply_markup = botoes_partidos())
    if query.data == "estado":
        #query.message.edit("Escolha um estado:", reply_markup = botoes_estados() )
        query.edit_message_text(text = "Escolha um estado:", reply_markup = botoes_estados())
    
    print('query.data:', query.data)
    
    
def deputado(update, context):  
    #update.message.text
    update.message.reply_text(update.message.text[10:])

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("iniciar", inicio))
    dp.add_handler(CommandHandler("ajuda", ajuda))
    dp.add_handler(CommandHandler("deputados", deputados))
    dp.add_handler(CommandHandler("deputado", deputado))
    dp.add_handler(CallbackQueryHandler(deputados, pattern='main'))
    dp.add_handler(CallbackQueryHandler(deputados_callback))
    
    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    #updater.start_webhook(listen="0.0.0.0",
    #                        port=int(PORT),
    #                        url_path=TOKEN,
    #                        webhook_url = 'https://fiscal-bot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
