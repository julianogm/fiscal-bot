from datetime import date

import cssselect
import lxml.html
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from constant import *


def get_data_from_camara_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["dados"]
    else:
        raise Exception(
            f"Request failed with status {response.status_code}: {response.json()['title']}"
        )


def lista_deputados():
    try:
        url = f"{API_CAMARA}deputados"
        return get_data_from_camara_api(url)
    except (KeyError, TypeError):
        return []


def get_deputados_by_filter(filter_name, filter_value):
    url = (
        API_CAMARA + f"deputados?{filter_name}={filter_value}&ordem=ASC&ordenarPor=nome"
    )
    return get_data_from_camara_api(url)


def deputado_por_estado(siglaUf):
    return get_deputados_by_filter("siglaUf", siglaUf)


def deputado_por_partido(siglaPartido):
    return get_deputados_by_filter("siglaPartido", siglaPartido)


def deputado_por_nome(nome):
    id_legis = get_data_from_camara_api(LEGISLATURA)[0]["id"]
    url = (
        API_CAMARA
        + f"deputados?nome={nome}&idLegislatura={id_legis}&ordem=ASC&ordenarPor=nome"
    )
    return get_data_from_camara_api(url)


def lista_partidos_deputados():
    ld = lista_deputados()
    lista_partidos = list(set([dep["siglaPartido"] for dep in ld]))
    return lista_partidos


def deputado_por_id(id):
    deputado = get_data_from_camara_api(API_CAMARA + f"deputados/{id}")
    if isinstance(deputado, dict):
        return deputado["ultimoStatus"]
    return DEP_INVALIDO


def nomes_deputados(lista=lista_deputados()):
    nomes = "\n".join([f"{d['nome']} - /dep_{d['id']}" for d in lista])
    return nomes


def dados_deputado(deputado):
    dados = get_data_from_camara_api(API_CAMARA + f"deputados/{deputado['id']}")
    return montar_mensagem(deputado, dados)


def info_deputado(id):
    resposta = requests.get(f"https://www.camara.leg.br/deputados/{id}")
    arv = lxml.html.fromstring(resposta.text)
    csspath_ceap = "#percentualgastocotaparlamentar > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)"
    csspath_verba_gab = "#percentualgastoverbagabinete > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)"
    csspath_email = ".email"

    info = []

    if arv.cssselect(csspath_email):
        info.append(arv.cssselect(csspath_email)[0].text_content())
    else:
        info.append("Email não encontrado")

    # valor gasto com cota parlamentar
    if arv.cssselect(csspath_ceap):
        info.append("R$ " + arv.cssselect(csspath_ceap)[0].text_content())
    else:
        info.append("Ainda não há gasto registrado nesse ano")

    # valor gasto com verba de gabinete
    if arv.cssselect(csspath_verba_gab):
        info.append("R$ " + arv.cssselect(csspath_verba_gab)[0].text_content())
    else:
        info.append("Ainda não há gasto registrado nesse ano")
    return info


def montar_mensagem(deputado, dados):
    info = info_deputado(deputado["id"])
    nome_lower = dados["nomeCivil"].replace(" ", "_").translate(NORMALIZAR).lower()
    nome_par_lower = dados["nomeCivil"].replace(" ", "+").translate(NORMALIZAR).lower()

    mensagem = ""
    mensagem += f"Nome civil: {dados['nomeCivil']} \n"
    # mensagem += f"CPF: {dados['cpf']} \n"
    mensagem += f"Partido: {deputado['siglaPartido']} | "
    mensagem += f"Estado: {deputado['siglaUf']} \n"
    mensagem += f"Email: {info[0]} \n"
    mensagem += f"Telefone: (61) {dados['ultimoStatus']['gabinete']['telefone']} \n\n"
    mensagem += f"Gastos de {deputado['nome']} em {date.today().year} \n"
    mensagem += f"CEAP: {info[1]} \n"
    mensagem += f"Verba de Gabinete: {info[2]} \n\n"
    # mensagem += "Verificar processos envolvendo o parlamentar:\n"
    # mensagem += f"/p_{nome_lower} \n\n"
    mensagem += f"Mais sobre o deputado(a): https://www.camara.leg.br/deputados/{deputado['id']} \n"
    mensagem += (
        f"https://www.jusbrasil.com.br/artigos-noticias/busca?q={nome_par_lower}"
    )

    return mensagem


def botoes_estados_deputados():
    keyboard = []
    i = 0
    while i < 26:
        keyboard.append(
            [
                InlineKeyboardButton(UF_NOME[i], callback_data="dep_" + UF_SIGLAS[i]),
                InlineKeyboardButton(
                    UF_NOME[i + 1], callback_data="dep_" + UF_SIGLAS[i + 1]
                ),
            ]
        )
        i += 2
    keyboard.append(
        [
            InlineKeyboardButton(UF_NOME[i], callback_data="dep_" + UF_SIGLAS[i]),
            InlineKeyboardButton("<< Voltar", callback_data="dep_voltar"),
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def botoes_partidos_deputados():
    siglas = list(set([dep["siglaPartido"] for dep in lista_deputados()]))
    siglas.sort()
    tam = len(siglas)
    keyboard = []
    i = 0
    ultima_sigla = None

    if tam % 2 == 1:
        ultima_sigla = siglas.pop()
        tam -= 1

    while i < tam:
        keyboard.append(
            [
                InlineKeyboardButton(siglas[i], callback_data="dep_" + siglas[i]),
                InlineKeyboardButton(
                    siglas[i + 1], callback_data="dep_" + siglas[i + 1]
                ),
            ]
        )
        i += 2

    if ultima_sigla != None:
        keyboard.append(
            [
                InlineKeyboardButton(ultima_sigla, callback_data="dep_" + ultima_sigla),
                InlineKeyboardButton("<< Voltar", callback_data="dep_voltar"),
            ],
        )
    else:
        keyboard.append([InlineKeyboardButton("<< Voltar", callback_data="dep_voltar")])

    return InlineKeyboardMarkup(keyboard)


def botoes_deputados():
    keyboard = [
        [
            InlineKeyboardButton("Por Partido ", callback_data="dep_partido"),
            InlineKeyboardButton("Por Estado", callback_data="dep_estado"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
