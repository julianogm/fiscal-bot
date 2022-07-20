import requests
import lxml.html
import cssselect
from datetime import date
from constant import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_request(url):
    response = requests.get(url)
    return response.json()['dados']

def lista_deputados():
    lista = get_request(API_CAMARA + "deputados")
    #list(map(lambda x: x.update({'nome':x['nome'].lower()}), lista))
    return lista

def por_estado(estado):
    ld = lista_deputados()
    lf = [dep for dep in ld if dep['siglaUf'] == estado]
    return lf

def por_partido(partido):
    ld = lista_deputados()
    lf = [dep for dep in ld if dep['siglaPartido'] == partido]
    return lf

def por_nome(nome):
    id_legis = get_request(LEGISLATURA)[0]['id']
    url = API_CAMARA + f"deputados?nome={nome}&idLegislatura={id_legis}&ordem=ASC&ordenarPor=nome"
    lista = get_request(url)
    return lista

def nomes_deputados(lista = lista_deputados()):
    nomes = "\n".join([d['nome'] for d in lista])
    return nomes

def dados_deputado(deputado):
    dados = get_request(API_CAMARA + f"deputados/{deputado['id']}")
    return montar_mensagem(deputado, dados)
    
def montar_mensagem(deputado, dados):
    gastos_deputado = gastos(deputado["id"])
    
    mensagem = ""
    mensagem += f"Nome civil: {dados['nomeCivil']}\n"
    mensagem += f"CPF: {dados['cpf']}\n"
    mensagem += f"Partido: {deputado['siglaPartido']}\n"
    mensagem += f"Estado: {deputado['siglaUf']}\n"
    mensagem += f"Email: {deputado['email']}\n"
    mensagem += f"Telefone: (61) {dados['ultimoStatus']['gabinete']['telefone']}\n\n"
    mensagem += f"Gastos do deputado(a) {deputado['nome']} em {date.today().year}\n"
    mensagem += f"Cota de Atividade Parlamentar (CEAP): R$ {gastos_deputado[0]}\n"
    mensagem += f"Verba de Gabinete utilizada: R$ {gastos_deputado[1]}\n\n"
    mensagem += f"Mais sobre o deputado(a): https://www.camara.leg.br/deputados/{deputado['id']}\n"
    mensagem += f"Detalhes dos gastos da camara: http://tiny.cc/gastos_parlamentares\n\n"
    mensagem += f"Sobre o CEAP: http://tiny.cc/ceap"
    
    return mensagem
      
def gastos(id):
    resposta = requests.get(f"https://www.camara.leg.br/deputados/{id}")
    arv = lxml.html.fromstring(resposta.text)
    csspath_ceap = "#percentualgastocotaparlamentar > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)"
    csspath_verba_gab = "#percentualgastoverbagabinete > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)"
    
    #valor gasto com cota parlamentar
    valores = [arv.cssselect(csspath_ceap)[0].text_content()]
    
    #valor gasto com verba de gabinete
    valores.append(arv.cssselect(csspath_verba_gab)[0].text_content())
    return valores

def botoes_estados():
    keyboard = []
    i = 0
    while i < 27:
        keyboard.append(
                        [InlineKeyboardButton(list(UF.values())[i], callback_data=list(UF.keys())[i]),
                        InlineKeyboardButton(list(UF.values())[i+1], callback_data=list(UF.keys())[i+1]),
                        InlineKeyboardButton(list(UF.values())[i+2], callback_data=list(UF.keys())[i+2]),]
                        )
        i+=3
    #keyboard.append([InlineKeyboardButton(list(UF.values())[i], callback_data=list(UF.keys())[i])])
    return InlineKeyboardMarkup(keyboard)

def botoes_partidos():
    siglas = list(set([dep['siglaPartido'] for dep in lista_deputados()]))
    tam = len(siglas)
    keyboard = []
    i = 0
    if tam%2==1:
        keyboard.append([InlineKeyboardButton(siglas[i], callback_data=siglas[i])])
        i+=1
    
    while i < tam:
        keyboard.append(
            [InlineKeyboardButton(siglas[i], callback_data=siglas[i]),
             InlineKeyboardButton(siglas[i+1], callback_data=siglas[i+1]),]
        )
        i+=2
    return InlineKeyboardMarkup(keyboard)