import requests

def get_processos(nome):
    nome = nome.replace("_", "+")
    url = f"https://apirest.politicos.org.br/api/parliamentarianranking?Year=0&Position=&Name={nome}&Take=9&Skip=0&OrderBy=scoreProcess&Include=Parliamentarian.State,Parliamentarian.Party,Parliamentarian.Organ,Parliamentarian.Processes&OnlyWithProcess=true&StatusId=1&SearchProcess="
    response = requests.get(url, headers = {'Accept':'application/json'})

    dados = response.json()['data']
    if not dados:
        return False

    processos = dados[0]['parliamentarian']['processes']
    return processos
