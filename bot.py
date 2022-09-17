# encoding: utf-8

from contextlib import nullcontext
import os
import camara
import senado
import logging
from constant import *
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram import ParseMode

load_dotenv()

PORT = int(os.environ['PORT'])
TOKEN = os.environ['TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def ajuda(update, context):
    msg = ("Comandos disponíveis: \n"
        + "/deputados - Listar deputados. \n"
        + "/senadores - Listar senadores.")

    update.message.reply_text(msg)

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
    elif chamada == 'sen':
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

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def dep_nome_link(update, context):
    id = update.message.text.replace('/dep_', '')
    deputado = camara.deputado_por_id(id)
    update.message.reply_text(deputado['urlFoto'])
    update.message.reply_text(camara.dados_deputado(deputado))
    update.message.reply_text(text="<a href='https://t.me/avaliacao_fiscal_bot/4'>Clique aqui para avaliar sua experiência em 30 segundos e ajudar na minha pesquisa</a>", parse_mode=ParseMode.HTML)

def sen_nome_link(update, context):
    id = update.message.text.replace('/sen_', '')
    senador = senado.senador_por_id(id)
    update.message.reply_text(senador['IdentificacaoParlamentar']['UrlFotoParlamentar'])
    update.message.reply_text(senado.dados_senador(senador))
    update.message.reply_text(text="<a href='https://t.me/avaliacao_fiscal_bot/4'>Clique aqui para avaliar sua experiência em 30 segundos e ajudar na minha pesquisa</a>", parse_mode=ParseMode.HTML)

def nomes(update, context):
    nome = update.message.text

    if len(nome) < 4:
        update.message.reply_text("Nome muito curto")
        return

    lista = []
    lista_deputados = camara.deputado_por_nome(nome)

    lista_senadores = senado.senador_por_nome(nome)

    if len(lista_senadores) == 0 and len(lista_deputados) == 0:
        update.message.reply_text("Nome não encontrado")
        return
    elif len(lista_deputados) == 1 and len(lista_senadores) == 0:
        update.message.reply_text(lista_deputados[0]['urlFoto'])
        update.message.reply_text(camara.dados_deputado(lista_deputados[0]))
        update.message.reply_text(text="<a href='https://t.me/avaliacao_fiscal_bot/4'>Clique aqui para avaliar sua experiência em 30 segundos e ajudar na minha pesquisa</a>", parse_mode=ParseMode.HTML)
    elif len(lista_senadores) == 1 and len(lista_deputados) == 0:
        update.message.reply_text(lista_senadores[0]['IdentificacaoParlamentar']['UrlFotoParlamentar'])
        update.message.reply_text(senado.dados_senador(lista_senadores[0]))
        update.message.reply_text(text="<a href='https://t.me/avaliacao_fiscal_bot/4'>Clique aqui para avaliar sua experiência em 30 segundos e ajudar na minha pesquisa</a>", parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text("Senadores encontrados:\n" + senado.nomes_senadores(lista_senadores))
        update.message.reply_text("Deputados encontrados:\n" + camara.nomes_deputados(lista_deputados))

def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("ajuda", ajuda))
    dp.add_handler(CommandHandler("deputados", deputados))
    dp.add_handler(CommandHandler("senadores", senadores))
    dp.add_handler(MessageHandler(Filters.regex(r'^(/dep_[\d]+)$'), dep_nome_link))
    dp.add_handler(MessageHandler(Filters.regex(r'^(/sen_[\d]+)$'), sen_nome_link))
    dp.add_handler(CallbackQueryHandler(callback))
    dp.add_handler(MessageHandler(Filters.command, ajuda))
    dp.add_handler(MessageHandler(Filters.text, nomes))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=TOKEN,
                            webhook_url = WEBHOOK_URL + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
