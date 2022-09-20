import requests
import lxml.html
import cssselect
from datetime import date
from constant import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_camara(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['dados']
    else:
        return response.json()['title']

def lista_deputados():
    lista = get_camara(API_CAMARA + "deputados")
    return lista

def deputado_por_estado(siglaUf):
    lf = get_camara(API_CAMARA + f"deputados?siglaUf={siglaUf}&ordem=ASC&ordenarPor=nome")
    return lf

def deputado_por_partido(siglaPartido):
    lf = get_camara(API_CAMARA + f"deputados?siglaPartido={siglaPartido}&ordem=ASC&ordenarPor=nome")
    return lf

def deputado_por_nome(nome):
    id_legis = get_camara(LEGISLATURA)[0]['id']
    url = API_CAMARA + f"deputados?nome={nome}&idLegislatura={id_legis}&ordem=ASC&ordenarPor=nome"
    lista = get_camara(url)
    return lista

def lista_partidos_deputados():
    ld = lista_deputados()
    lista_partidos = list(set([dep['siglaPartido'] for dep in ld]))
    return lista_partidos

def deputado_por_id(id):
    deputado = get_camara(API_CAMARA + f"deputados/{id}")
    if isinstance(deputado, dict):
        return deputado['ultimoStatus']
    return DEP_INVALIDO

def nomes_deputados(lista = lista_deputados()):
    nomes = "\n".join([ f"{d['nome']} - /dep_{d['id']}" for d in lista ])
    return nomes

def dados_deputado(deputado):
    dados = get_camara(API_CAMARA + f"deputados/{deputado['id']}")
    return montar_mensagem(deputado, dados)

def info_deputado(id):
    resposta = requests.get(f"https://www.camara.leg.br/deputados/{id}")
    arv = lxml.html.fromstring(resposta.text)
    csspath_ceap = "#percentualgastocotaparlamentar > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)"
    csspath_verba_gab = "#percentualgastoverbagabinete > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)"
    csspath_email = ".email"

    info = [arv.cssselect(csspath_email)[0].text_content()]

    #valor gasto com cota parlamentar
    info.append(arv.cssselect(csspath_ceap)[0].text_content())

    #valor gasto com verba de gabinete
    info.append(arv.cssselect(csspath_verba_gab)[0].text_content())
    return info

def montar_mensagem(deputado, dados):
    info = info_deputado(deputado["id"])
    nome_lower = dados['nomeCivil'].replace(' ','_').translate(NORMALIZAR).lower()

    mensagem = ""
    mensagem += f"Nome civil: {dados['nomeCivil']} \n"
    mensagem += f"CPF: {dados['cpf']} \n"
    mensagem += f"Partido: {deputado['siglaPartido']} | "
    mensagem += f"Estado: {deputado['siglaUf']} \n"
    mensagem += f"Email: {info[0]} \n"
    mensagem += f"Telefone: (61) {dados['ultimoStatus']['gabinete']['telefone']} \n\n"
    mensagem += f"Gastos de {deputado['nome']} em {date.today().year} \n"
    mensagem += f"CEAP: R$ {info[1]} \n"
    mensagem += f"Verba de Gabinete: R$ {info[2]} \n\n"
    mensagem += "Verificar Processos:\n"
    mensagem += f"/p_{nome_lower} \n\n"
    mensagem += f"Mais sobre o deputado(a): https://www.camara.leg.br/deputados/{deputado['id']} \n"

    return mensagem

def botoes_estados_deputados():
    keyboard = []
    i = 0
    while i < 26:
        keyboard.append( [InlineKeyboardButton(UF_NOME[i], callback_data='dep_'+UF_SIGLAS[i]),
                         InlineKeyboardButton(UF_NOME[i+1], callback_data='dep_'+UF_SIGLAS[i+1]),] )
        i+=2
    keyboard.append( [InlineKeyboardButton(UF_NOME[i], callback_data='dep_'+UF_SIGLAS[i]),
                     InlineKeyboardButton("<< Voltar", callback_data="dep_voltar")] )

    return InlineKeyboardMarkup(keyboard)

def botoes_partidos_deputados():
    siglas = list(set([dep['siglaPartido'] for dep in lista_deputados()]))
    siglas.sort()
    tam = len(siglas)
    keyboard = []
    i = 0
    ultima_sigla = None

    if tam%2==1:
        ultima_sigla = siglas.pop()
        tam-=1

    while i < tam:
        keyboard.append(
            [InlineKeyboardButton(siglas[i], callback_data='dep_'+siglas[i]),
             InlineKeyboardButton(siglas[i+1], callback_data='dep_'+siglas[i+1]),]
        )
        i+=2

    if ultima_sigla != None:
        keyboard.append([InlineKeyboardButton(ultima_sigla, callback_data='dep_'+ultima_sigla),
                        InlineKeyboardButton('<< Voltar', callback_data='dep_voltar')],)
    else:
        keyboard.append([InlineKeyboardButton('<< Voltar', callback_data='dep_voltar')])

    return InlineKeyboardMarkup(keyboard)

def botoes_deputados():
    keyboard = [
        [InlineKeyboardButton("Por Partido ", callback_data='dep_partido'),
         InlineKeyboardButton("Por Estado", callback_data='dep_estado'),],
    ]
    return InlineKeyboardMarkup(keyboard)
