import requests
from constant import *

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
    dados = API_CAMARA + f"deputados/{deputado['id']}"
    montar_mensagem(deputado, dados)
    
def montar_mensagem(deputado, dados):
    
