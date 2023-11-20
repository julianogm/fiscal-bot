import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
grandparent = os.path.dirname(parent)
sys.path.append(parent)
sys.path.append(grandparent)

from datetime import date

import lxml.html
import requests

from constant import *

CSS_CEAP = "#collapse-ceaps > div:nth-child(1) > table:nth-child(1) > tfoot:nth-child(4) > tr:nth-child(1) > td:nth-child(2)"
CSS_TELEFONE = ".dl-horizontal > dd:nth-child(10)"


class Senators:
    def __init__(self):
        pass

    def _get_data(self, url):
        response = requests.get(url, headers={"Accept": "application/json"})
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(
                f"Request failed with status {response.status_code}: {response.json()['title']}"
            )

    def list_senators(self):
        url = f"{API_SENADO}senador/lista/atual"
        senators = self._get_data(url)["ListaParlamentarEmExercicio"]["Parlamentares"][
            "Parlamentar"
        ]
        return senators

    def by_state(self, state_acronym):
        senators = self.list_senators()
        senators_by_state = [
            senator
            for senator in senators
            if senator["IdentificacaoParlamentar"]["UfParlamentar"] == state_acronym
        ]

        return senators_by_state

    def by_political_party(self, party_acronym):
        senators = self.list_senators()
        senators_by_party = [
            senator
            for senator in senators
            if senator["IdentificacaoParlamentar"]["SiglaPartidoParlamentar"]
            == party_acronym
        ]

        return senators_by_party

    def list_political_parties(self):
        senators = self.list_senators()
        political_parties = [
            senator["IdentificacaoParlamentar"]["SiglaPartidoParlamentar"]
            for senator in senators
        ]

        return list(set(political_parties))

    def get_names_ids(self, senators=None):
        if senators == None:
            senators = self.list_senators()
        name_ids = "\n".join(
            [
                f"{senator['IdentificacaoParlamentar']['NomeParlamentar']} - /senador_{senator['IdentificacaoParlamentar']['CodigoParlamentar']}"
                for senator in senators
            ]
        )
        return name_ids

    def get_senator_data(self, senator_id):
        senator_data = self._reply_data(senator_id)
        return senator_data

    # fetch data from federal senate website via webscraping
    def _senator_info(self, senator_id):
        current_year = date.today().year
        url = f"{SITE_SENADO}{senator_id}?ano={current_year}"
        response = requests.get(url)

        tree = lxml.html.fromstring(response.text)
        site_info = {}

        if tree.cssselect(CSS_CEAP):
            ceap_spending = tree.cssselect(CSS_CEAP)[0].text_content()
            site_info["ceap"] = f"R$ {ceap_spending}"
        else:
            site_info["ceap"] = "Ainda não há gasto registrado nesse ano"

        if tree.cssselect(CSS_TELEFONE):
            phone = tree.cssselect(CSS_TELEFONE)[0].text_content()
            site_info["telefone"] = phone[:14]
        else:
            site_info["telefone"] = "Número não encontrado"

        return site_info

    # build the response message to the user
    def _reply_data(self, senator_id):
        current_year = date.today().year
        url = f"{API_SENADO}senador/{senator_id}"
        senator = self._get_data(url)["DetalheParlamentar"]["Parlamentar"]

        senator_api_data = senator["IdentificacaoParlamentar"]
        senator_site_data = self._senator_info(senator_id)

        full_name = senator_api_data["NomeCompletoParlamentar"]
        name_search_jusbrasil = (
            full_name.replace(" ", "+").translate(NORMALIZAR).lower()
        )

        senator_email = (
            senator_api_data.get("EmailParlamentar")
            if senator_api_data.get("EmailParlamentar") != None
            else "Sem email cadastrado"
        )

        message = (
            f"Nome civil: {full_name}\n"
            f"Partido: {senator_api_data['SiglaPartidoParlamentar']} | Estado: {senator_api_data['UfParlamentar']}\n"
            f"Email: {senator_email}\n"
            f"Telefone: {senator_site_data['telefone']}\n\n"
            f"Gastos de {senator_api_data['NomeParlamentar']} em {current_year}\n"
            f"CEAPS: {senator_site_data['ceap']}\n\n"
            f"Mais sobre o senador(a): {senator_api_data['UrlPaginaParlamentar']}\n"
            f"https://www.jusbrasil.com.br/artigos-noticias/busca?q={name_search_jusbrasil}\n"
        )

        data_dict = {}
        data_dict["message"] = message
        data_dict["photo"] = senator_api_data["UrlFotoParlamentar"]
        return data_dict


obj_senator = Senators()
