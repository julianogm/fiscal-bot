import logging
import re

from telegram.ext import CallbackContext

from .telegram_buttons import *

# Enable logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def errors(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def help_command(update, context):
    message = (
        "Comandos disponíveis: \n"
        "/deputados - Listar deputados.\n"
        "/senadores - Listar senadores.\n"
        "/parlamento - Informações sobre o parlamento brasileiro.\n"
        "/sobre - Informações sobre o bot.\n\n"
        "Você pode clicar nos links ao lado dos nomes dos parlamentares "
        "listados para ver as informações daquele parlamentar.\n\n"
        "Para pesquisar por nome, envie uma mensagem com o nome "
        "ou uma parte do nome do deputado ou senador desejado."
    )

    update.message.reply_text(message)


def deputies_command(update, context: CallbackContext):
    update.message.reply_text("Escolha um filtro:", reply_markup=deputies_buttons())


def senators_command(update, context: CallbackContext):
    update.message.reply_text("Escolha um filtro:", reply_markup=senators_buttons())


def parliament_command(update, context):
    message = (
        "O parlamento brasileiro é o Congresso Nacional, constituído pela Câmara dos Deputados e pelo Senado Federal.\n"
        "O Congresso Nacional é o órgão constitucional que exerce, no âmbito federal, as funções do poder legislativo, quais sejam, elaborar/aprovar leis e fiscalizar o Estado brasileiro (suas duas funções típicas), bem como administrar e julgar (funções atípicas).\n\n"
        "Gastos do Senado Federal e da Câmara do Deputados:\n"
        "https://www12.senado.leg.br/transparencia \n"
        "http://tiny.cc/gastos_parlamentares\n\n"
        "Sobre a CEAP (Cota para o Exercício da Atividade Parlamentar): \nhttp://tiny.cc/ceap \nhttp://tiny.cc/ceaps"
    )

    update.message.reply_text(message, disable_web_page_preview=True)


def about_command(update, context):
    message = (
        "Código fonte (ainda em desenvolvimento): \n"
        "https://github.com/julianogm/fiscal-bot \n\n"
    )
    update.message.reply_text(message, disable_web_page_preview=True)


def callback(update, context):
    query = update.callback_query

    data = query.data.split("_")
    political_type = data[0]
    request_type = data[1]

    if political_type == "deputado":
        if request_type == "partido":
            query.edit_message_text(
                text="Escolha um partido:",
                reply_markup=deputies_parties_buttons(),
            )

        elif request_type == "estado":
            query.edit_message_text(
                text="Escolha um estado:",
                reply_markup=state_buttons(political_type),
            )

        elif request_type == "voltar":
            query.edit_message_text(
                "Escolha um filtro:", reply_markup=deputies_buttons()
            )

        elif request_type in UF_SIGLAS:
            deputies_list = obj_deputy.by_state(request_type)
            message = (
                f"Deputados em exercício - {request_type}:\n"
                f"{obj_deputy.get_names_ids(deputies_list)}"
            )
            query.edit_message_text(message)

        elif request_type in obj_deputy.list_political_parties():
            deputies_list = obj_deputy.by_political_party(request_type)
            message = (
                f"Deputados eleitos pelo partido {request_type}:\n"
                f"{obj_deputy.get_names_ids(deputies_list)}"
            )
            query.edit_message_text(message)

    elif political_type == "senador":
        if request_type == "partido":
            query.edit_message_text(
                text="Escolha um partido:",
                reply_markup=senators_parties_buttons(),
            )

        elif request_type == "estado":
            query.edit_message_text(
                text="Escolha um estado:",
                reply_markup=state_buttons(political_type),
            )

        elif request_type == "voltar":
            query.edit_message_text(
                "Escolha um filtro:", reply_markup=senators_buttons()
            )

        elif request_type in UF_SIGLAS:
            senators_list = obj_senator.by_state(request_type)
            message = (
                f"Senadores em exercício - {request_type}:\n"
                f"{obj_senator.get_names_ids(senators_list)}"
            )
            query.edit_message_text(message)

        elif request_type in obj_senator.list_political_parties():
            senators_list = obj_senator.by_political_party(request_type)
            message = (
                f"Senadores eleitos pelo partido {request_type}:\n"
                f"{obj_senator.get_names_ids(senators_list)}"
            )
            query.edit_message_text(message)


def create_deputy_link(update, context):
    deputy_id = update.message.text.replace("/deputado_", "")

    deputy_data = obj_deputy.get_deputy_data(deputy_id)
    update.message.reply_photo(
        photo=deputy_data["photo"], caption=deputy_data["message"]
    )


def create_senator_link(update, context):
    senator_id = update.message.text.replace("/senador_", "")

    senator_data = obj_senator.get_senator_data(senator_id)
    update.message.reply_photo(
        photo=senator_data["photo"],
        caption=senator_data["message"],
    )
