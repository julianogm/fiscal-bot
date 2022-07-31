import requests
from camara import montar_mensagem
import lxml.html
import cssselect
from datetime import date
from constant import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_senado(url):
    response = requests.get(url, headers = {'Accept':'application/json'})
    return response.json()

def lista_senadores():
    ls = get_senado(API_SENADO + "senador/lista/atual")['ListaParlamentarEmExercicio']['Parlamentares']['Parlamentar']
    return ls

def botoes_senadores():
    keyboard = [
        [InlineKeyboardButton("Por Partido ", callback_data='sen_partido'),
         InlineKeyboardButton("Por Estado", callback_data='sen_estado'),],
    ]
    return InlineKeyboardMarkup(keyboard)

def nomes_senadores(lista = lista_senadores):
    nomes = "\n".join([ f"{sen['IdentificacaoParlamentar']['NomeParlamentar']} - /sen_{sen['IdentificacaoParlamentar']['CodigoParlamentar']}" for sen in lista])
    return nomes

def senador_por_estado(siglaUF):
    lf = get_senado(API_SENADO + f"senador/lista/atual?uf={siglaUF}")['ListaParlamentarEmExercicio']['Parlamentares']['Parlamentar']
    return lf

def senador_por_partido(siglaPartido):
    ls = lista_senadores()
    lf = [sen for sen in ls if sen['IdentificacaoParlamentar']['SiglaPartidoParlamentar'] == siglaPartido]
    return lf

def senador_por_id(id):
    senador = get_senado(API_SENADO + f"senador/{id}")['DetalheParlamentar']['Parlamentar']
    return senador

def dados_senador(senador):
    dados = get_senado(API_SENADO + f"senador/{senador['IdentificacaoParlamentar']['CodigoParlamentar']}")
    return montar_mensagem(senador, dados)

def lista_partidos_senadores():
    ls = lista_senadores()
    lista_partidos = [item['IdentificacaoParlamentar']['SiglaPartidoParlamentar'] for item in ls]
    return lista_partidos

def montar_mensagem(senador, dados):
    mensagem = ""
    info_senador = senador['IdentificacaoParlamentar']

    mensagem += f"Nome civil: {info_senador['NomeCompletoParlamentar']}\n"
    mensagem += f"Partido: {info_senador['SiglaPartidoParlamentar']}\n"
    mensagem += f"Estado: {info_senador['UfParlamentar']}\n"

    return mensagem


def botoes_partidos_senadores():
    ls = lista_senadores()
    siglas = list(set([item['IdentificacaoParlamentar']['SiglaPartidoParlamentar'] for item in ls]))
    siglas.sort()
    tam = len(siglas)
    keyboard = []
    i = 0
    ultima_sigla = None

    if tam%2==1:
        ultima_sigla = siglas.pop()

    while i < tam:
        keyboard.append(
                [InlineKeyboardButton(siglas[i], callback_data='sen_'+siglas[i]),
                InlineKeyboardButton(siglas[i+1], callback_data='sen_'+siglas[i+1]),]
            )
        i+=2
    
    if ultima_sigla != None:
        keyboard.append([InlineKeyboardButton(ultima_sigla, callback_data=ultima_sigla),
                        InlineKeyboardButton('<< Voltar', callback_data='sen_voltar')],)
    else:
        keyboard.append([InlineKeyboardButton('<< Voltar', callback_data='sen_voltar')])

    return InlineKeyboardMarkup(keyboard)

def botoes_estados_senadores():
    keyboard = []
    i = 0
    while i < 26:
        keyboard.append( [InlineKeyboardButton(UF_NOME[i], callback_data='sen_'+UF_SIGLAS[i]),
                         InlineKeyboardButton(UF_NOME[i+1], callback_data='sen_'+UF_SIGLAS[i+1]),] )
        i+=2
    keyboard.append( [InlineKeyboardButton(UF_NOME[i], callback_data='sen_'+UF_SIGLAS[i]),
                     InlineKeyboardButton('<< Voltar', callback_data='sen_voltar')] )
    
    return InlineKeyboardMarkup(keyboard)