# encoding: utf-8

from contextlib import nullcontext
import os
import camara
import senado
import logging
from constant import *
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

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
    update.message.reply_text('Bot iniciado, digite /ajuda para para listar os comandos.')

def ajuda(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Comandos disponíveis: \n"
                        + "/ajuda - Listar comandos do bot \n"
                        + "/deputados - Pesquisar deputados por filtros. \n"
                        + "/deputado 'nome do deputado' - Pesquisar dados de um deputado pelo nome. \n"
                        + "/estados - Listar deputados ou senadores por Estado-UF. \n"
                        + "/partidos - Listar deputados ou senadores por partidos. \n"
        )    

def deputados(update, context: CallbackContext):
    update.message.reply_text('Escolha um filtro:', reply_markup = camara.botoes_deputados())

def senadores(update, context: CallbackContext):
    update.message.reply_text('Escolha um filtro:', reply_markup = senado.botoes_senadores())
    
def callback(update, context):
    query = update.callback_query

    chamada = query.data[:3]
    condicao = query.data[4:]

    if chamada == 'dep':
        if condicao == "partido":
            query.edit_message_text(text = "Escolha um partido:", reply_markup = camara.botoes_partidos_deputados())
        if condicao == "estado":
            query.edit_message_text(text = "Escolha um estado:", reply_markup = camara.botoes_estados_deputados())
        if condicao == "voltar":
            query.edit_message_text('Escolha um filtro:', reply_markup = camara.botoes_deputados())
        if condicao in UF_SIGLAS:
            query.edit_message_text(f"Deputados eleitos por {condicao}:\n" + camara.nomes_deputados(camara.deputado_por_estado(condicao)))
        if condicao in camara.lista_partidos_deputados():
            query.edit_message_text(camara.nomes_deputados(camara.deputado_por_partido(condicao)))
    if chamada == 'sen':
        if condicao == 'partido':
            query.edit_message_text(text = "Escolha um partido:", reply_markup = senado.botoes_partidos_senadores())
        if condicao == 'estado':
            query.edit_message_text(text = "Escolha um estado:", reply_markup = senado.botoes_estados_senadores())
        if condicao == 'voltar':
            query.edit_message_text('Escolha um filtro:', reply_markup = senado.botoes_senadores())
        if condicao in UF_SIGLAS:
            query.edit_message_text(f"Senadores eleitos por {condicao}:\n" + senado.nomes_senadores(senado.senador_por_estado(condicao)))
        if condicao in senado.lista_partidos_senadores():
            query.edit_message_text(f"Senadores eleitos pelo partido {condicao}:\n" + senado.nomes_senadores(senado.senador_por_partido(condicao)))

def deputado(update, context):  
    nome_deputado = update.message.text[10:]
    
    if len(nome_deputado) < 3:
        update.message.reply_text("Nome muito curto")
        return
    
    lista_deputados = camara.deputado_por_nome(nome_deputado)
    deputado = None      
    
    deputado = lista_deputados[0] if len(lista_deputados) == 1 else None
    
    if len(lista_deputados) == 0:
        update.message.reply_text("Nome não encontrado")
    elif deputado == None:
        update.message.reply_text(camara.nomes_deputados(lista_deputados))
    else:
        update.message.bot.send_photo(update.message.chat.id, deputado['urlFoto'])
        update.message.reply_text(camara.dados_deputado(deputado))

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
def dep_nome_link(update, context):
    id = update.message.text.replace('/dep_', '')
    deputado = camara.deputado_por_id(id)
    update.message.bot.send_photo(update.message.chat.id, deputado['urlFoto'])
    update.message.reply_text(camara.dados_deputado(deputado))

def sen_nome_link(update, context):
    id = update.message.text.replace('/sen_', '')
    senador = senado.senador_por_id(id)
    update.message.bot.send_photo(update.message.chat.id, senador['IdentificacaoParlamentar']['UrlFotoParlamentar'])
    update.message.reply_text(senado.dados_senador(senador))

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
    dp.add_handler(CommandHandler("senadores", senadores))
    #dp.add_handler(CommandHandler("senador", senador))
    dp.add_handler(MessageHandler(Filters.regex(r'^(/dep_[\d]+)$'), dep_nome_link))
    dp.add_handler(MessageHandler(Filters.regex(r'^(/sen_[\d]+)$'), sen_nome_link))
    dp.add_handler(CallbackQueryHandler(deputados, pattern='main'))
    dp.add_handler(CallbackQueryHandler(callback))
    
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
