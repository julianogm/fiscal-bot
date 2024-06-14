import logging

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
        "Mais detalhes sobre os gastos do parlamento brasileiro: \n"
        "[Câmara dos Deputados](https://www.camara.leg.br/transparencia/) \n"
        "[Senado Federal](https://www12.senado.leg.br/transparencia) \n"
        "\n"
        "Sobre a CEAP (Cota para o Exercício da Atividade Parlamentar): \n"
        "[Câmara dos Deputados](https://www2.camara.leg.br/comunicacao/assessoria-de-imprensa/guia-para-jornalistas/cota-parlamentar)\n"
        "[Senado Federal](https://www12.senado.leg.br/perguntas-frequentes/perguntas-frequentes/canais-de-atendimento/senadores/o-que-pode-ser-ressarcido-a-conta-da-ceaps)"
    )

    update.message.reply_text(
        message, disable_web_page_preview=True, parse_mode="Markdown"
    )


def about_command(update, context):
    message = "Código fonte: https://github.com/julianogm/fiscal-bot \n\n"
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


def search_name(update, context):
    parliamentarian_name = update.message.text

    if len(parliamentarian_name) < 4:
        message = "Nome muito curto. Tente novamente com um nome maior."
        update.message.reply_text(message)
        return

    # if " " in parliamentarian_name:
    #     message = "Insira um nome sem espaços em branco."
    #     update.message.reply_text(message)
    #     return

    deputies_list = obj_deputy.by_name(parliamentarian_name)
    senators_list = obj_senator.by_name(parliamentarian_name)

    if len(senators_list) == 0 and len(deputies_list) == 0:
        message = "Não foi encontrado parlamentar com o nome inserido."
        update.message.reply_text(message)
        return

    elif len(senators_list) == 0 and len(deputies_list) == 1:
        deputy_data = obj_deputy.get_deputy_data(deputies_list[0]["id"])
        update.message.reply_photo(
            photo=deputy_data["photo"], caption=deputy_data["message"]
        )

    elif len(senators_list) == 1 and len(deputies_list) == 0:
        senator_data = obj_senator.get_senator_data(
            senators_list[0]["IdentificacaoParlamentar"]["CodigoParlamentar"]
        )
        update.message.reply_photo(
            photo=senator_data["photo"],
            caption=senator_data["message"],
        )

    else:
        senators_names_ids = obj_senator.get_names_ids(senators_list)
        deputies_names_ids = obj_deputy.get_names_ids(deputies_list)

        message_senators = f"Senadores encontrados:\n{senators_names_ids}"
        message_deputies = f"Deputados encontrados:\n{deputies_names_ids}"
        message = ""

        if len(senators_names_ids) > 0:
            message = f"{message}{message_senators}\n\n"
        if len(deputies_names_ids) > 0:
            message = f"{message}{message_deputies}"

        update.message.reply_text(message)
