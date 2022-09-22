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
from apis import politicos_org

load_dotenv()

PORT = int(os.environ['PORT'])
TOKEN = os.environ['TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']
MODE = os.environ['MODE']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def ajuda(update, context):
    msg = ("Comandos disponíveis: \n"
        + "/deputados - Listar deputados.\n"
        + "/senadores - Listar senadores.\n"
        + "/parlamento - Informações sobre o parlamento brasileiro.\n"
        + "/sobre - Informações sobre o bot.\n\n"
        + "Você pode clicar nos links ao lado dos nomes dos parlamentares "
        + "listados para ver as informações daquele parlamentar.\n\n"
        + "Para pesquisar por nome, envie uma mensagem com o nome "
        + "ou uma parte do nome do deputado ou senador desejado.")

    update.message.reply_text(msg)

def deputados(update, context: CallbackContext):
    update.message.reply_text('Escolha um filtro:', reply_markup = camara.botoes_deputados())

def senadores(update, context: CallbackContext):
    update.message.reply_text('Escolha um filtro:', reply_markup = senado.botoes_senadores())

def parlamento(update, context):
    msg = ("O parlamento brasileiro é o Congresso Nacional, constituído pela Câmara dos Deputados e pelo Senado Federal.\n"
        +  "O Congresso Nacional é o órgão constitucional que exerce, no âmbito federal, as funções do poder legislativo, quais sejam, elaborar/aprovar leis e fiscalizar o Estado brasileiro (suas duas funções típicas), bem como administrar e julgar (funções atípicas).\n\n"
        +  "Gastos do Senado Federal e da Câmara do Deputados:\n"
        +  "https://www12.senado.leg.br/transparencia \n"
        +  "http://tiny.cc/gastos_parlamentares\n\n"
        +  "Sobre a CEAP (Cota para o Exercício da Atividade Parlamentar): \nhttp://tiny.cc/ceap \nhttp://tiny.cc/ceaps")

    update.message.reply_text(msg, disable_web_page_preview=True)

def sobre(update, context):
    msg = ("Código fonte (ainda em desenvolvimento): \nhttps://github.com/julianogm/fiscal-bot \n\n")
    update.message.reply_text(msg, disable_web_page_preview=True)

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
            query.edit_message_text(f"Deputados em exercício - {condicao}:\n" + camara.nomes_deputados(camara.deputado_por_estado(condicao)))
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
            query.edit_message_text(f"Senadores em exercício - {condicao}:\n" + senado.nomes_senadores(senado.senador_por_estado(condicao)))
        if condicao in senado.lista_partidos_senadores():
            query.edit_message_text(f"Senadores eleitos pelo partido {condicao}:\n" + senado.nomes_senadores(senado.senador_por_partido(condicao)))

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def dep_nome_link(update, context):
    id = update.message.text.replace('/dep_', '')
    id = id.split('@', 1)[0]

    deputado = camara.deputado_por_id(id)
    update.message.reply_text(deputado['urlFoto'])
    update.message.reply_text(camara.dados_deputado(deputado))
    update.message.reply_text(text="<a href='https://t.me/avaliacao_fiscal_bot/4'>Clique aqui para avaliar sua experiência em 30 segundos e ajudar na minha pesquisa</a>", parse_mode=ParseMode.HTML)

def sen_nome_link(update, context):
    id = update.message.text.replace('/sen_', '')
    id = id.split('@', 1)[0]

    senador = senado.senador_por_id(id)
    update.message.reply_text(senador['IdentificacaoParlamentar']['UrlFotoParlamentar'])
    update.message.reply_text(senado.dados_senador(senador))
    update.message.reply_text(text="<a href='https://t.me/avaliacao_fiscal_bot/4'>Clique aqui para avaliar sua experiência em 30 segundos e ajudar na minha pesquisa</a>", parse_mode=ParseMode.HTML)

def p(update, context):
    nome = update.message.text.replace('/p_', '').lower()
    nome = nome.split('@', 1)[0]

    processos = politicos_org.get_processos(nome)

    if processos == False:
        update.message.reply_text("Não foram encontrados processos envolvendo o parlamentar.")
        return

    for item in processos:
        mensagem = ""
        mensagem += f"Dados do processo: {item['number']}\n"
        mensagem += f"Situação: {item['processStatus']}\n\n"
        mensagem += f"Descrição: {item['processText']}\n"
        mensagem += f"Mais informações: {item['processUrl']}"
        update.message.reply_text(text=mensagem)

def pesquisa_nome(update, context):
    nome = update.message.text

    if len(nome) < 4:
        update.message.reply_text("Nome muito curto")
        return

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
        if len(lista_senadores) > 0:
            update.message.reply_text("Senadores encontrados:\n" + senado.nomes_senadores(lista_senadores))
        if len(lista_deputados) > 0:
            update.message.reply_text("Deputados encontrados:\n" + camara.nomes_deputados(lista_deputados))

def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("deputados", deputados))
    dp.add_handler(CommandHandler("senadores", senadores))
    dp.add_handler(CommandHandler("parlamento", parlamento))
    dp.add_handler(CommandHandler("sobre", sobre))
    dp.add_handler(MessageHandler(Filters.regex(r'^(/dep_[\d@'+updater.bot.username+']+)$'), dep_nome_link))
    dp.add_handler(MessageHandler(Filters.regex(r'^(/sen_[\d@'+updater.bot.username+']+)$'), sen_nome_link))
    dp.add_handler(MessageHandler(Filters.regex(r'^(/p_[\D]+)$'), p))
    dp.add_handler(CallbackQueryHandler(callback))
    dp.add_handler(MessageHandler(Filters.command, ajuda))
    dp.add_handler(MessageHandler(Filters.text, pesquisa_nome))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if MODE == 'webhook':
        updater.start_webhook(listen="0.0.0.0",
                                port=int(PORT),
                                url_path=TOKEN,
                                webhook_url = WEBHOOK_URL + TOKEN)
    elif MODE == 'polling':
        updater.start_polling()
    else:
        print("--- Invalid MODE value. Set MODE to 'polling' or 'webhook'. ---")
        exit()

    updater.idle()

if __name__ == '__main__':
    main()
